from BaseClasses import Item, Location, MultiWorld, Tutorial, Region, CollectionState
from worlds.AutoWorld import World, WebWorld

from .Client import CTJoTSNIClient
from .Items import CTJoTItemManager
from .Locations import CTJoTLocationManager
from .Options import Locations, Items, Rules, Victory, GameMode, \
    ItemDifficulty, TabTreasures, BucketFragments, FragmentCount

import threading
from typing import Callable


class CTJoTWebWorld(WebWorld):
    settings_page = "https://multiworld.ctjot.com/"
    # TODO: Figure out these fields
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Jets of Time multiworld.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Anguirel"]
    )]


class CTJoTWorld(World):
    """
    TODO: Game description here.
    """

    _item_manager = CTJoTItemManager()
    _location_manager = CTJoTLocationManager()

    game = "Chrono Trigger Jets of Time"
    # option_definitions: Union[OptionList, OptionDict] = {
    option_definitions = {
        "game_mode": GameMode,
        "item_difficulty": ItemDifficulty,
        "tab_treasures": TabTreasures,
        "bucket_fragments": BucketFragments,
        "fragment_count": FragmentCount,
        "items": Items,
        "locations": Locations,
        "rules": Rules,
        "victory": Victory
    }

    item_name_to_id = _item_manager.get_item_name_to_id_mapping()
    location_name_to_id = _location_manager.get_location_name_to_id_mapping()

    web = CTJoTWebWorld()

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.rom_name_available_event = threading.Event()

    def create_item(self, name: str) -> Item:
        """
        Create a CTJoT multiworld item.

        Overridden from World
        """
        return self._item_manager.create_item(name, self.player)

    def create_items(self) -> None:
        """
        Create items for the player from the passed in
        config data and append them to the multiworld item pool.

        Overridden from World
        """
        items_from_config = getattr(self.multiworld, "items")[self.player]
        items = []

        # This handles the key items from the yaml.
        for item in items_from_config.value:
            items.append(self._item_manager.create_item_by_id(item["id"], self.player))

        # Now add filler/useful items to spots that didn't roll key items
        items.extend(
            self._item_manager.select_filler_items(
                self._location_manager.get_filler_location_ids(self.multiworld, self.player),
                self.multiworld,
                self.player))

        self.multiworld.itempool += items

    def create_regions(self) -> None:
        """
        Set up the locations and rules for this player.

        Overridden from World
        """
        locations_from_config = getattr(self.multiworld, "locations")[self.player]
        rules_from_config = getattr(self.multiworld, "rules")[self.player].value
        menu_region = Region("Menu", self.player, self.multiworld)
        menu_region.multiworld = self.multiworld

        # Create Location objects from yaml location data and add them to the menu region.
        for location_entry in locations_from_config.value:
            if location_entry["classification"] == "event":
                # Create event locations/items (character pickup locations)
                location = Location(self.player, location_entry["name"], None, menu_region)
                location.event = True
                # Add character here as a locked item.
                location.place_locked_item(
                    self._item_manager.create_event_item(location_entry["character"], self.player))
            else:
                # Create normal locations
                location = self._location_manager.get_location(self.player, location_entry, menu_region)

            location.access_rule = self._get_access_rule(rules_from_config[location_entry["name"]])
            menu_region.locations.append(location)

        # Add filler locations for non-progression items
        self._location_manager.add_filler_locations(self.multiworld, self.player, menu_region)

        # Add victory condition event
        victory_rules_from_config = getattr(self.multiworld, "victory")[self.player].value
        victory_location = Location(self.player, "Victory", None, menu_region)
        victory_location.event = True
        victory_location.access_rule = self._get_access_rule(victory_rules_from_config)
        victory_location.place_locked_item(self._item_manager.create_event_item("Victory", self.player))
        menu_region.locations.append(victory_location)

        self.multiworld.regions += [menu_region]

    def get_filler_item_name(self) -> str:
        """
        Get a random filler item.

        Overridden from World
        """
        return self.multiworld.random.choice(self._item_manager.get_junk_fill_items())

    def modify_multidata(self, multidata: dict):
        import base64
        player_name = self.multiworld.player_name[self.player]
        if player_name and player_name != "":
            new_name = base64.b64encode(bytes(player_name.encode("ascii"))).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def _get_access_rule(self, access_rules: list[list[str]]) -> Callable[[CollectionState], bool]:
        """
        Create an access rule function from yaml location data.
        """
        def can_access(state: CollectionState) -> bool:
            # No access rules means this is sphere 0
            if len(access_rules) == 0:
                return True

            # loop through each access rule for this location
            for rule in access_rules:
                has_access = True
                for item in rule:
                    if not state.has(item, self.player):
                        has_access = False
                        break
                # Check if we have all the items from the rule
                if has_access:
                    return True

            # We didn't satisfy any of the access rules
            return False

        return can_access
