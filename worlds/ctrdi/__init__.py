from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
import typing
from typing import Callable

# Archipelago imports
import settings
import worlds

from BaseClasses import CollectionState, Item, \
    ItemClassification, Location, MultiWorld, Region, Tutorial

from Options import Choice, Range, Toggle

from Utils import read_snes_rom

from worlds.AutoWorld import WebWorld, World

# Local APWorld imports
from .Options import CTRDIOptions, option_groups

# RDI randomizer imports
from ctrando import randomizer
from ctrando.arguments import arguments, argumenttypes, tomloptions
from ctrando.bosses.bosstypes import BossSpotID
from ctrando.common import ctenums, ctrom, memory, randostate
from ctrando.common.ctenums import (
    ItemID, RecruitID,  TreasureID as TID)
from ctrando.entranceshuffler import entrancefiller
from ctrando.entranceshuffler.locregions import LocRegion
from ctrando.entranceshuffler.owregions import OWRegion
from ctrando.entranceshuffler.regionmap import ExitConnector, RegionConnector
from ctrando.logic import logictypes
from ctrando.objectives import objectivetypes as objty
import ctrando.treasures.treasuretypes as tty


# TODO task list:
#  - Add Options handing
#  - Create tutorial docs
#  - General organization/cleanup pass, add helper classes, etc


# TODO: Pick a real item ID offset
# Offset to give CTRDI items a unique item range in AP
ITEM_ID_BASE = 50_350_000
CTUSA_MD5_HASH = "a2bc447961e52fd2227baed164f729dc"


class CTRDIDeltaPatch(worlds.Files.APDeltaPatch):
    hash = CTUSA_MD5_HASH
    game = "Chrono Trigger: Rando-Dalton Imperial"
    patch_file_ending = ".apctrdi"

    @classmethod
    def get_source_data(cls) -> bytes:
        return CTRDIWorld.get_base_rom_bytes()


class CTRDISettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the CT ROM"""
        description = "Chrono Trigger (USA) ROM"
        copy_to = "Chrono Trigger (USA).sfc"
        md5s = [CTRDIDeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class CTRDIWebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "Setup guide for CTRDI multiworld",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Pseudoarc", "Anguirel"]
    )]
    option_groups = option_groups


@dataclass
class RegionData:
    """Store corresponding RDI and AP region definitions"""
    rdi_region: LocRegion | OWRegion
    ap_region: Region


_locs_to_skip: dict[TID] = [
    TID.TRADING_POST_PETAL_FANG_BASE,
    TID.TRADING_POST_PETAL_FANG_UPGRADE,
    TID.TRADING_POST_PETAL_FANG_UPGRADE,
    TID.TRADING_POST_PETAL_HORN_BASE,
    TID.TRADING_POST_PETAL_HORN_UPGRADE,
    TID.TRADING_POST_PETAL_FEATHER_BASE,
    TID.TRADING_POST_PETAL_FEATHER_UPGRADE,
    TID.TRADING_POST_FANG_HORN_BASE,
    TID.TRADING_POST_FANG_HORN_UPGRADE,
    TID.TRADING_POST_FANG_FEATHER_BASE,
    TID.TRADING_POST_FANG_FEATHER_UPGRADE,
    TID.TRADING_POST_HORN_FEATHER_BASE,
    TID.TRADING_POST_HORN_FEATHER_UPGRADE,
    TID.TRADING_POST_SPECIAL
]


class CTRDIWorld(World):
    """
    TODO: CTRDI description here
    """
    game: str = "Chrono Trigger: Rando-Dalton Imperial"
    topology_present = True
    origin_region_name = "starting_rewards"
    options_dataclass = CTRDIOptions
    Options: CTRDIOptions
    settings_key = "ctrdi_options"
    settings: typing.ClassVar[CTRDISettings]

    web = CTRDIWebWorld()

    rdi_settings: arguments.Settings = None
    config: randostate.ConfigState = None

    item_name_to_id = {str(item): ITEM_ID_BASE +
                       item for item in ItemID}
    location_name_to_id = {str(loc): ITEM_ID_BASE +
                           loc for loc in TID}

    _item_name_to_RDI_type = {str(x): x for x in ItemID}

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        """
        Verify that the ROM exists?
        """
        pass

    def generate_early(self):
        """
        Set up the RDI settings/config objects that will be used
        in subsequent stages to create items/regions/etc for the multiworld.
        """
        self._translate_settings()
        base_rom = ctrom.CTRom.from_file(self.get_rom_path())
        self.ct_rom = randomizer.ctrom.CTRom(base_rom.getvalue())
        self.config = randomizer.get_random_config(
            self.rdi_settings, self.ct_rom, self.multiworld.random)

    def create_item(self, name: str) -> Item:
        """
        Create an AP item from the named RDI item.
        """
        return self._create_AP_item(self._item_name_to_RDI_type[name])

    def create_items(self) -> None:
        """
        Create the multiworld items for this player
        """
        items = []
        for loc, value in self.config.treasure_assignment.items():

            if loc in _locs_to_skip:
                continue

            if isinstance(value, tty.Gold):
                # TODO: Handle gold rewards
                #       I'm not sure it's possible to send arbitrary numbers
                #       for gold rewards, so maybe leave gold chests local?
                pass
            else:
                items.append(self._create_AP_item(value))

        self.multiworld.itempool += items

    def create_regions(self) -> None:
        """
        Create regions and locations for this player
        """
        # Create regions and connecting exits
        region_dict = self._create_region_map()

        # Create treasure locations and game/logic event locations
        self._create_locations_for_regions(region_dict)
        self._create_recruit_events(region_dict)
        self._create_flag_events(region_dict)

        # Create victory location
        menu_region = region_dict[self.origin_region_name].ap_region
        victory_loc = Location(self.player, "Victory", None, menu_region)
        victory_loc.event = True
        victory_loc.place_locked_item(
            Item("Victory", ItemClassification.progression, None, self.player))
        victory_loc.access_rule = self._create_victory_rule()
        menu_region.locations.append(victory_loc)
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has("Victory", self.player)

        # Add all regions to the multiworld object
        self.multiworld.regions += [x.ap_region for x in region_dict.values()]

    def _create_victory_rule(self) -> Callable[[CollectionState], bool]:
        """
        Create a victory rule for this game.
        Victory occurs when the player has completed the required objectives
        and collected the right items/characters to reach and defeat Lavos.
        """

        def victory_rule(state: CollectionState) -> bool:
            # Get objective count
            obj_tokens = ["Objective 1", "Objective 2",
                          "Objective 3", "Objective 4",
                          "Objective 5", "Objective 6",
                          "Objective 7", "Objective 8"]

            num_objs_complete = 0
            for obj in obj_tokens:
                if state.has(obj, self.player):
                    num_objs_complete = num_objs_complete + 1

            # Objective based access
            algetty_portal_open = num_objs_complete >= self.rdi_settings.objective_options.num_algetty_portal_objectives
            omen_open = num_objs_complete >= self.rdi_settings.objective_options.num_omen_objectives
            bucket_open = num_objs_complete >= self.rdi_settings.objective_options.num_bucket_objectives
            timegauge_1999_open = num_objs_complete >= self.rdi_settings.objective_options.num_timegauge_objectives

            # Location access
            has_eot = state.has(
                str(memory.Flags.HAS_EOT_TIMEGAUGE_ACCESS), self.player)

            # Build up the access rules to lavos
            # End of Time -> Bucket
            if has_eot and bucket_open:
                return True

            # Hard Lavos - TODO: Do we actually want to include this in logic?
            ocean_palace_access = state.has(
                str(objty.QuestID.ZEAL_PALACE_THRONE), self.player)
            ruby_knife = state.has(str(ItemID.RUBY_KNIFE), self.player)
            if ocean_palace_access and ruby_knife:
                return True

            # Crash Epoch into lavos in 1999
            has_flight = state.has(
                str(logictypes.ScriptReward.FLIGHT), self.player)
            if has_flight and timegauge_1999_open:
                return True

            # Black Omen
            if has_flight and algetty_portal_open and omen_open:
                return True

            return False

        return victory_rule

    def _create_flag_events(self, region_dict: dict[str, RegionData]):
        """
        Create event items/locations for script and memory flag rewards.
        These are used internally by the logic rules to gate access by some
        in-game event rather than holding an item or character.

        Ignore shop rewards
        """
        for name, loc_region in self.config.region_map.loc_region_dict.items():
            reward_list = \
                list(loc_region.reward_spots) + loc_region.region_rewards
            for reward in reward_list:
                if isinstance(reward, logictypes.ScriptReward) or \
                        isinstance(reward, logictypes.StrangeReward) or \
                        isinstance(reward, memory.Flags) or \
                        isinstance(reward, BossSpotID) or \
                        isinstance(reward, ItemID):

                    self._create_event_loc_item_pair(
                        str(reward), region_dict[loc_region.name].ap_region)

    def _create_recruit_events(self, region_dict: dict[str, RegionData]):
        """
        Create event locations and event items for character recruitment.
        """
        for name, loc_region in self.config.region_map.loc_region_dict.items():
            for reward in loc_region.reward_spots:
                if isinstance(reward, RecruitID):
                    # Found a recruit spot
                    for character in self.config.recruit_dict[reward]:
                        char_name = str(character)
                        ap_region = region_dict[loc_region.name].ap_region
                        self._create_event_loc_item_pair(
                            char_name, ap_region)

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
                        if loc in _locs_to_skip:
                            continue
                        # TODO: Filter out locations with gold rewards
                        if isinstance(self.config.treasure_assignment[loc], tty.Gold):
                            continue
                        location = Location(
                            self.player, str(loc), self.location_name_to_id[str(loc)], region_data.ap_region)
                        location.access_rule = lambda state: True
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
                from_region = region_dict[connector.from_region_name]
                to_region = region_dict[connector.to_region_name]

                # Create the exit and set up its rule
                exit_name = f"{connector.link_name}-{
                    connector.from_region_name}-{connector.to_region_name}"
                exit_obj = from_region.ap_region.create_exit(exit_name)
                access_rule = self._create_access_rule(connector)
                exit_obj.access_rule = access_rule
                exit_obj.connect(to_region.ap_region)

        return region_dict

    def _create_event_loc_item_pair(self, name: str, region: Region):
        """
        Create an event location with a locked event item
        """
        item = Item(name,
                    ItemClassification.progression,
                    None,
                    self.player)

        loc_name = f"{region.name}-{name}"
        loc = Location(self.player, loc_name, None, region)
        loc.event = True
        loc.place_locked_item(item)
        region.locations.append(loc)

    def get_filler_item_name(self) -> str:
        """
        Get a random filler item
        """
        # TODO: Real filler items - Ideally this will never be needed
        return str(ctenums.ItemID.MOP)

    def modify_multidata(self, multidata: dict):
        pass

    def generate_output(self, output_directory: str):
        """
        Generate the randomized ROM and create the patch file
        """

        out_rom = randomizer.get_ctrom_from_config(
            self.ct_rom, self.rdi_settings, self.config)

        basename = self.multiworld.get_out_file_name_base(self.player)
        output_path = os.path.join(output_directory, f"{basename}.sfc")

        with open(output_path, "wb") as file:
            file.write(out_rom.getbuffer())

        patch = CTRDIDeltaPatch(
            os.path.splittext(output_path)[0] +
            CTRDIDeltaPatch.patch_file_ending,
            player=self.player,
            player_name=self.multiworld.player_name[self.player],
            patched_path=output_path)

        patch.write()
        os.unlink(output_path)

    def _create_access_rule(
        self,
        connector: RegionConnector | ExitConnector
    ) -> Callable[[CollectionState], bool]:
        """
        Get an AP access rule from a RDI connector object
        """
        # Trivial case, always available
        # An list containint an empty list of single access rules
        if not connector.rule.get_access_rule()[0]:
            return lambda state: True

        # Convert the RDI rule to an AP rule
        def can_access(state: CollectionState) -> bool:

            for single_rule in connector.rule.get_access_rule():

                satisfies_rule = True
                for item in single_rule:
                    count = single_rule.count(item)
                    if not state.has(str(item), self.player, count):
                        # At least one condition of this rule isn't met
                        satisfies_rule = False

                if satisfies_rule:
                    return True

            return False

        return can_access

    def _create_AP_item(self, item: ctenums.ItemID) -> Item:
        """
        Create an AP item from a CTRDI ItemID
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
        data_dict = {}
        group_specs = arguments.Settings.get_argument_spec()
        for group_spec in group_specs.values():
            for flag_name, spec in group_spec.items():
                if hasattr(self.options, flag_name):
                    value = getattr(self.options, flag_name)
                    if isinstance(value, Choice):
                        value = value.name_lookup[value]

                    if isinstance(value, Toggle):
                        value = value.value == 1

                    if isinstance(value, Range):
                        value = value.value

                    # Skip string fields with no data
                    if isinstance(spec, argumenttypes.StringArgument):
                        if value != "":
                            data_dict[flag_name] = value
                    else:
                        data_dict[flag_name] = value

        # print(data_dict)
        # args = tomloptions.toml_data_to_args(data_dict)
        args = tomloptions.toml_data_to_args({})
        self.rdi_settings = randomizer.extract_settings(*args)

    @staticmethod
    def get_rom_path() -> str:
        """
        Get the path to the Chrono Trigger ROM
        """
        file_name = CTRDIWorld.settings.rom_file

        if not os.path.exists(file_name):
            # TODO: Refine error text
            raise ValueError("No Chrono Trigger ROM specified")

        return file_name

    @staticmethod
    def get_base_rom_bytes(file_name: str = "") -> bytes:
        """
        Get the base ROM data as a bytes object
        """
        base_rom_bytes = getattr(
            CTRDIWorld.get_base_rom_bytes, "base_rom_bytes", None)
        if not base_rom_bytes:
            file_name = CTRDIWorld.get_rom_path()
            base_rom_bytes = bytes(read_snes_rom(open(file_name, "rb")))

            basemd5 = hashlib.md5()
            basemd5.update(base_rom_bytes)
            if basemd5.hexdigest() != CTUSA_MD5_HASH:
                raise Exception(
                    'Supplied base ROM does not match the known MD5 hash')

            CTRDIWorld.get_base_rom_bytes.base_rom_bytes = base_rom_bytes

        return base_rom_bytes
