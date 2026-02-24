import base64
import hashlib
import logging
import os
import threading
import typing

# Archipelago imports
import settings
import worlds

import Utils

from BaseClasses import Item, MultiWorld, Tutorial
from worlds.AutoWorld import WebWorld, World

# local world imports
from .Client import JPClient
from .Options import JPOptions
from . import Items
from . import Locations

from .jprando import jprom
from .jprando import qolpatches as qol
from .jprando import basepatch as bp


class JPWebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "Setup guide for JP multiworld",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Anguirel"]
    )]


JPUSA_MD5_HASH = jprom.JPRom.JPUSA_MD5_HASH


class JPDeltaPatch(worlds.Files.APDeltaPatch):
    hash = JPUSA_MD5_HASH
    game = "Jurassic Park"
    patch_file_ending = ".apjp"

    @classmethod
    def get_source_data(cls) -> bytes:
        file_path = JPWorld.get_base_rom_path()
        rom_data = bytes(Utils.read_snes_rom(open(file_path, "rb")))

        rommd5 = hashlib.md5()
        rommd5.update(rom_data)

        if rommd5.hexdigest() != JPUSA_MD5_HASH:
            raise Exception("Invalid hash. Please use a Jurassic Park USA ROM")

        return rom_data


class JPSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the JP ROM"""
        description = "Jurassic Park (USA) ROM"
        copy_to = "Jurassic Park (USA).sfc"
        md5s = [JPUSA_MD5_HASH]

    rom_file: RomFile = RomFile(RomFile.copy_to)


jp_logger = logging.getLogger("Jurassic Park")


class JPWorld(World):
    """
    TODO: Description here
    """

    game: str = "Jurassic Park"
    topology_present = True
    origin_region_name = "Overworld Start"
    options_dataclass = JPOptions
    options: JPOptions
    settings_key = "jp_options"
    settings: typing.ClassVar[JPSettings]

    web = JPWebWorld()

    item_name_to_id = Items.get_name_to_id_mapping()
    location_name_to_id = Locations.get_name_to_id_mapping()

    rom_name_available_event: threading.Event
    encoded_name: str

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.rom_name_available_event = threading.Event()
        self.encoded_name = ""

    def generate_early(self):
        pass

    def create_item(self, name: str) -> Item:
        return Items.create_item(name, self.player)

    def get_filler_item_name(self) -> str:
        return Items.get_random_filler_name(self.multiworld)

    def create_items(self) -> None:
        items = Items.create_all_progression_items(self.player)
        items += Items.create_filler_items(self.player,
                                           self.options.enable_traps.value)
        self.multiworld.itempool += items

    def create_regions(self) -> None:
        regions = Locations.create_regions(
            self.player, self.multiworld, self.options.eggs_required)
        self.multiworld.regions += regions

        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has("Escape the Island", self.player)

    def generate_output(self, output_directory: str):

        try:
            rom = jprom.JPRom(self.get_base_rom_path())
            player_name = self.multiworld.player_name[self.player]
            hashed_name_bytes = hash(player_name).to_bytes(8, signed=True)
            self.encoded_name = base64.b64encode(hashed_name_bytes).decode()

            eggs_required = self.options.eggs_required.value

            bp.apply_AP_base_patch(rom, hashed_name_bytes, eggs_required)

            # Apply optional quality-of-life patches
            if self.options.passive_health_regen:
                qol.patch_health_regen(rom)
            if self.options.infinite_lives:
                qol.patch_infinite_lives(rom)
            if self.options.infinite_cattle_prod:
                qol.patch_infinite_cattle_prod(rom)
            if self.options.infinite_ammo:
                qol.patch_infinite_ammo(rom)
            if self.options.linked_gates:
                qol.patch_gates_open_together(rom)

            # Write the modified ROM
            rompath = os.path.join(
                output_directory,
                f"{self.multiworld.get_out_file_name_base(self.player)}.sfc")

            rom.write_to_file(rompath)

            # Generate the patch file
            patch = JPDeltaPatch(
                os.path.splitext(rompath)[0]+JPDeltaPatch.patch_file_ending,
                player=self.player,
                player_name=self.multiworld.player_name[self.player],
                patched_path=rompath)

            patch.write()

            os.unlink(rompath)
        except Exception as e:
            raise e
        finally:
            self.rom_name_available_event.set()

    def modify_multidata(self, multidata: dict):
        self.rom_name_available_event.wait()
        player_name = self.multiworld.player_name[self.player]
        jp_logger.info(f"JP encoded player name: {self.encoded_name}")
        jp_logger.info(f"original name: {
                       multidata["connect_names"][player_name]}")

        multidata["connect_names"][self.encoded_name] = \
            multidata["connect_names"][player_name]

    @staticmethod
    def get_base_rom_path():
        options = settings.get_settings()
        file_name = options["jp_options"]["rom_file"]

        if not os.path.exists(file_name):
            file_name = Utils.user_path(file_name)

        return file_name
