from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
import os

# Archipelago imports
from BaseClasses import CollectionState, Entrance, EntranceType, Item, \
    ItemClassification, Location, Multiworld, Region, Tutorial

from worlds.AutoWorld import WebWorld, World


# APWorld imports
from .Options import CTRandoOptions

# Randomizer imports
from ctrando import randomizer
from ctrando.arguments import arguments
from ctrando.common import ctenums, ctrom, randostate
from ctrando.common.ctenums import LocID, RecruitID, ShopID, TreasureID as TID
from ctrando.entranceshuffler import entrancefiller
from ctrando.entranceshuffer.locregions import LocRegion
from ctrando.objectives import objectivetypes
from ctrando.entranceshuffer.owregions import OWRegion
from ctrando.entranceshuffer.regionmap import ExitConnector, RegionConnector
from ctrando.treasures.treasuretypes import Gold


# TODO task list:
#  - Create settings class
#  - Add Options handing
#  - Finish definitions for characer items/events
#  - Victory condition
#  - Create client
#  - Create tutorial docs
#  - General organization/cleanup pass, add helper classes, etc


# TODO: Pick a real item ID offset
# Offset to give CTRando items a unique item range in AP
ITEM_ID_BASE = 50_350_000


class CTRandoWebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "Setup guide for CTRando multiworld",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Pseudoarc", "Anguirel"]
    )]


@dataclass
class RegionData:
    """Store corresponding RDI and AP region definitions"""
    rdi_region: LocRegion | OWRegion
    ap_region: Region


class CTRandoWorld(World):
    """
    TODO: CTRando description here
    """
    game: str = "Chrono Trigger"
    topology_present = True
    options_dataclass = CTRandoOptions
    Options: CTRandoOptions

    web = CTRandoWebWorld()

    rando_settings: arguments.Settings = None
    rando_config: randostate.ConfigState = None

    def __init__(self, world: Multiworld, player: int):
        super().__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, multiworld: Multiworld):
        """
        Verify that the ROM exists?
        """
        pass

    def generate_early(self):
        """
        Set up the ctrando settings/config objects that will be used
        in subsequent stages to create items/regions/etc for the multiworld.
        """
        # TODO: Maybe convert yaml options so we can use the built-in
        #       extract_settings function in the randomizer?
        self._translate_settings()
        ct_rom = ctrom.CTRom.from_file(self._get_rom_path())
        self.rando_config = randomizer.get_random_config(self.settings, ct_rom)

    def create_items(self) -> None:
        """
        Create the multiworld items for this player
        """
        items = []
        for value in self.rando_config.treasure_assignment.values():
            if isinstance(value, Gold):
                # TODO: Handle gold rewards
                #       I'm not sure it's possible to send arbitrary numbers
                #       for gold rewards, so maybe leave gold chests local?
                pass
            else:
                items.append(self._create_AP_item(value))

        self.multiworld.itempool += items

        # TODO: Create event items for characters and memory flags

    def create_regions(self) -> None:
        """
        Create regions and locations for this player
        """
        # Create regions and connecting exits
        region_dict = self._create_region_map()

        # Create treasure locations
        self._create_locations_for_regions(region_dict)

        # Create event locations for character recruit pickups
        self._create_recruit_events(region_dict)

        # Create objective events
        obj_item_names = self._create_objective_events(region_dict)

        # Create victory rule

    _objective_items = [
        ctenums.ItemID.OBJECTIVE_1, ctenums.ItemID.OBJECTIVE_2,
        ctenums.ItemID.OBJECTIVE_3, ctenums.ItemID.OBJECTIVE_4,
        ctenums.ItemID.OBJECTIVE_5, ctenums.ItemID.OBJECTIVE_6,
        ctenums.ItemID.OBJECTIVE_7, ctenums.ItemID.OBJECTIVE_8]

    def _create_objective_events(self, region_dict: dict[str, RegionData]) -> list[str]:
        """
        Create event locations and event items for objective completion.
        Return a list of objective item names that can be used for
        the victory rule
        """
        objective_dict: dict[ctenums.ItemID, objectivetypes.ObjectiveType] = {}
        for item in zip(self._objective_items, self.config.objectives):
            objective_dict[item[0]] = item[1]

        obj_item_names: list[str] = []
        for name, loc_region in self.region_map.loc_region_dict.items():
            for reward in loc_region.reward_spots:
                if reward in self._objective_items:
                    # Create an event item/location pair for this objective
                    # TODO: Name conversion based on type?
                    obj_name = str(self.config.recruit_dict[reward])
                    ap_region = region_dict[loc_region.name].ap_region
                    item = Item(obj_name,
                                ItemClassification.progression,
                                None,
                                self.player)
                    loc = Location(self.player, obj_name, None, ap_region)
                    loc.event = True
                    loc.place_locked_item(item)
                    ap_region.locations.append(loc)
                    obj_item_names.append(obj_name)

        return obj_item_names

    def _create_recruit_events(self, region_dict: dict[str, RegionData]):
        """
        Create event locations and event items for character recruitment.
        """
        for name, loc_region in self.region_map.loc_region_dict.items():
            for reward in loc_region.reward_spots:
                if isinstance(reward, RecruitID):
                    # Found a recruit spot
                    if self.config.recruit_dict[reward] is not None:
                        char_name = str(self.config.recruit_dict[reward])
                        ap_region = region_dict[loc_region.name].ap_region
                        item = Item(char_name,
                                    ItemClassification.progression,
                                    None,
                                    self.player)
                        loc = Location(self.player, char_name, None, ap_region)
                        loc.event = True
                        loc.place_locked_item(item)
                        ap_region.locations.append(loc)

    def _create_locations_for_regions(
            self, region_dict: dict[str, RegionData]):
        """
        Create corresponding locations for each RDI location and
        attach them to the appropriate regions.
        """
        for name, region_data in region_dict.items():
            if isinstance(region_data.rdi_region, LocRegion):
                for loc in region_data.rdi_region.reward_spots:
                    if isinstance(loc, TID):
                        # TODO: Filter out locations with gold rewards
                        location = Location(
                            self.player, str(loc), None, region_data.ap_region)
                        region_data.ap_region.locations.append(location)

    def _create_region_map(self) -> dict[str, RegionData]:
        """
        Create a corresponding AP Region definition for every RDI region
        and wire up the exits
        """
        region_dict: dict[str, RegionData] = {}

        for name in self.config.region_map.name_connector_dict.keys():
            if name in self.config.region_map.ow_region_dict:
                rdi_region = self.config.region_map.ow_region_dict[name]
            elif name in self.config.region_map.loc_region_dict:
                rdi_region = self.config.region_map.loc_region_dict[name]
            else:
                raise Exception(f"Region not found: {name}")

            ap_region = Region(name, self.player, self.multiworld)
            region_dict[name] = RegionData(
                rdi_region=rdi_region, ap_region=ap_region)

        # Now that all regions are created, connect them up
        # based on the exit layout in the rando config
        for name, connectors in self.config.region_map.name_connector_dict.items():

            for connector in connectors:
                from_region = region_dict[connector.from_region]
                to_region = region_dict[connector.to_region]
                entrance_type = EntranceType.TWO_WAY if connector.reversible else EntranceType.ONE_WAY

                # Create the entrance and set up its rule
                entrance = Entrance(
                    self.player,
                    connector.link_name,
                    from_region.ap_region,
                    0,
                    entrance_type)
                entrance.access_rule = self._create_access_rule(connector)
                entrance.connect(to_region)

        return region_dict

    def get_filler_item_name(self) -> str:
        """
        Get a random filler item
        """
        # TODO: Real filler items - Ideally this will never be needed
        return self._create_AP_item(ctenums.ItenID.MOP)

    def modify_multidata(self, multidata: dict):
        pass

    # TODO: Finish defining this
    # def generate_output(self,

    def _create_access_rule(
        self,
        connector: RegionConnector | ExitConnector
    ) -> Callable[[CollectionState], bool]:
        """
        Get an AP access rule from a RDI connector object
        """
        # Trivial case, always available
        if not connector.get_access_rule():
            return lambda state: True

        # Convert the RDI rule to an AP rule
        def can_access(state: CollectionState) -> bool:
            for single_rule in connector.get_access_rule():

                satisfies_rule = True
                for item in single_rule:
                    if not state.has(str(item), self.player):
                        # At least one condition of this rule isn't met
                        satisfies_rule = False

                if satisfies_rule:
                    return True

            return False

        return can_access

    def _create_AP_item(self, item: ctenums.ItemID) -> Item:
        """
        Create an AP item from a CTRando ItemID
        """
        # TODO: Handle item classification for additional key items
        if item in entrancefiller.get_forced_key_items():
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler
        # TODO: Additional classifications? Useful?

        item_code = ITEM_ID_BASE + item
        return Item(str(item), classification, item_code, self.player)

    def _translate_settings(self):
        """
        Set up a randomizer Settings object with the user's chosen AP options
        """
        self.setting = arguments.Settings()
        # TODO: Convert AP yaml options to equivalent settings here
        # TODO: Add rom location to settings

    @staticmethod
    def _get_rom_path() -> str:
        """
        Get the path to the Chrono Trigger ROM
        """
        file_name = CTRandoWorld.settings.rom_file

        if not os.path.exists(file_name):
            # TODO: Refine error text
            raise ValueError("No Chrono Trigger ROM specified")

        return file_name
