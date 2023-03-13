from BaseClasses import Item, Location, MultiWorld, Tutorial, Region, CollectionState
from Options import OptionDict, OptionList
from ..AutoWorld import World, WebWorld

from .Items import CTJoTItemManager
from .Locations import CTJoTLocationManager
from .Options import Locations, Items, Rules, Victory

from typing import Callable, Union


class CTJoTWebWorld(WebWorld):
    settings_page = "https://ctjot.com/"
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
    option_definitions: Union[OptionList, OptionDict] = {
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
        self._item_manager = CTJoTItemManager()

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
        for item in items_from_config.value:
            for i in range(item["count"]):
                items.append(self.create_item(item["name"]))

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
                location = Location(self.player, location_entry["name"], location_entry["id"], menu_region)

            location.access_rule = self._get_access_rule(rules_from_config[location_entry["name"]])
            menu_region.locations.append(location)

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
