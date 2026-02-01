from dataclass import dataclass
import logging
import typing
from typing import override

from NetUtils import ClientStatus, NetworkItem
from SNIClient import SNIContext

from worlds.AutoSNIClient import SNIClient

from ctrando.common.ctenums import TreasureID as TID
import ctrando.common.memory
from ctrando.common.memory import Flags
from ctrando.treasures import treasuretypes

snes_logger = logging.getLogger("SNES")

ITEM_ID_BASE = 50_350_000
MAX_IN_GAME_ITEM_ID = 0xFF

# SNI memory mapping constants
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

# RDI constants
# NOTE: Addresses are in SNES addressing, not SNI addressing
# TODO: Update JoT values with RDI values
#       Received item count needs to be 2 bytes
EVENT_BLOCK_SIZE = 0x200
EVENT_BASE_ADDR = 0x7F0000
TREASURE_BASE_ADDR = 0x7F0001
RECEIVED_ITEM_ADDR = 0x7E287A  # TODO: Update this - JoT value
RECEIVED_ITEM_CNT = 0x7E287C  # TODO: Update this - JoT value
VICTORY_ADDR = 0x00  # TODO: Get real victory flag ADDR
VICTORY_FLAG = 0x01  # TODO: Get real victory flag bit

LOCATION_ADDR = 0xF50100  # Already in SNI address space

# ROM/player/slot validation
VALIDATION_ADDR = ROM_START + 0x3F8C03  # TODO: Update this - JoT value
VALIDATION_SIZE = 0x20

INVALID_TRACKING_LOCS = [0x00, 0x1B1]
MAX_MAP_ID = 0x1FF


@dataclass
class CheckCounter:
    address: int
    count: int


_script_locations: dict[TID, Flags | CheckCounter] = {
    # Northern Ruins event chests
    TID.NORTHERN_RUINS_BASEMENT_600: Flags.NORTHERN_RUINS_BASEMENT_CHEST_600_OBTAINED,
    TID.NORTHERN_RUINS_BASEMENT_1000: Flags.NORTHERN_RUINS_BASEMENT_CHEST_1000_OBTAINED,
    TID.NORTHERN_RUINS_ANTECHAMBER_LEFT_600: Flags.NORTHERN_RUINS_ANTECHAMBER_CHEST_600_OBTAINED,
    TID.NORTHERN_RUINS_ANTECHAMBER_LEFT_1000: Flags.NORTHERN_RUINS_ANTECHAMBER_CHEST_1000_OBTAINED,

    # Sealed chests
    TID.NORTHERN_RUINS_ANTECHAMBER_SEALED_600: Flags.NORTHERN_RUINS_ANTECHAMBER_SEALED_600_OBTAINED,
    TID.NORTHERN_RUINS_ANTECHAMBER_SEALED_1000: Flags.NORTHERN_RUINS_ANTECHAMBER_SEALED_1000_OBTAINED,
    TID.NORTHERN_RUINS_BACK_LEFT_SEALED_600: Flags.NORTHERN_RUINS_BACK_LEFT_SEALED_600_OBTAINED,
    TID.NORTHERN_RUINS_BACK_LEFT_SEALED_1000: Flags.NORTHERN_RUINS_BACK_LEFT_SEALED_1000_OBTAINED,
    TID.NORTHERN_RUINS_BACK_RIGHT_SEALED_600: Flags.NORTHERN_RUINS_BACK_RIGHT_SEALED_600_OBTAINED,
    TID.NORTHERN_RUINS_BACK_RIGHT_SEALED_1000: Flags.NORTHERN_RUINS_BACK_RIGHT_SEALED_1000_OBTAINED,
    TID.TRUCE_INN_SEALED_600: Flags.TRUCE_INN_SEALED_600_OBTAINED,
    TID.TRUCE_INN_SEALED_1000: Flags.TRUCE_INN_SEALED_1000_OBTAINED,
    TID.PYRAMID_LEFT: Flags.PYRAMID_LEFT_CHEST,
    TID.PYRAMID_RIGHT: Flags.PYRAMID_RIGHT_CHEST,
    TID.PORRE_ELDER_SEALED_1: Flags.PORRE_ELDER_SEALED_1_OBTAINED,
    TID.PORRE_ELDER_SEALED_2: Flags.PORRE_ELDER_SEALED_2_OBTAINED,
    TID.PORRE_MAYOR_SEALED_1: Flags.PORRE_MAYOR_SEALED_1_OBTAINED,
    TID.PORRE_MAYOR_SEALED_2: Flags.PORRE_MAYOR_SEALED_2_OBTAINED,
    TID.GUARDIA_CASTLE_SEALED_600: Flags.GUARDIA_CASTLE_SEALED_600_OBTAINED,
    TID.GUARDIA_CASTLE_SEALED_1000: Flags.GUARDIA_CASTLE_SEALED_1000_OBTAINED,
    TID.GUARDIA_FOREST_SEALED_600: Flags.GUARDIA_FOREST_SEALED_600_OBTAINED,
    TID.GUARDIA_FOREST_SEALED_1000: Flags.GUARDIA_FOREST_DEAD_END_SEALED_CHEST,
    TID.HECKRAN_SEALED_1: Flags.HECKRAN_SEALED_OBTAINED,
    TID.HECKRAN_SEALED_2: Flags.HECKRAN_SEALED_OBTAINED,
    TID.MAGIC_CAVE_SEALED: Flags.MAGIC_CAVE_SEALED_CHEST,

    # Standard key item locations
    TID.REPTITE_LAIR_KEY: Flags.NIZBEL_DEFEATED,
    TID.MELCHIOR_RAINBOW_SHELL: Flags.MELCHIOR_TREASURY_FREE_ITEM_GIVEN,
    TID.MELCHIOR_SUNSTONE_RAINBOW: Flags.MELCHIOR_TREASURY_SUNSTONE_ITEM_GIVEN,
    TID.MELCHIOR_SUNSTONE_SPECS: Flags.MELCHIOR_TREASURY_SUNSTONE_ITEM_GIVEN,
    TID.FROGS_BURROW_LEFT: Flags.OBTAINED_BURROW_LEFT_ITEM,
    TID.MT_WOE_KEY: Flags.MT_WOE_BOSS_DEFEATED,
    TID.FIONA_KEY: Flags.OBTAINED_GREEN_DREAM_ITEM,
    TID.ARRIS_DOME_DOAN_KEY: Flags.OBTAINED_DOAN_ITEM,
    TID.SUN_PALACE_KEY: Flags.SUN_PALACE_ITEM_OBTAINED,
    TID.GENO_DOME_BOSS_1: Flags.GENO_DOME_ATROPOS_DEFEATED,
    TID.GENO_DOME_BOSS_2: Flags.GENO_DOME_MOTHER_BRAIN_DEFEATED,
    TID.GIANTS_CLAW_KEY: Flags.OBTAINED_GIANTS_CLAW_KEY,
    TID.KINGS_TRIAL_KEY: Flags.KINGS_TRIAL_COMPLETE,
    TID.ZENAN_BRIDGE_CHEF: Flags.CHEF_GIVES_JERKY,
    TID.ZENAN_BRIDGE_CHEF_TAB: Flags.CHEF_GIVES_JERKY,
    TID.ZENAN_BRIDGE_CAPTAIN: Flags.ZENAN_CAPTAIN_ITEM,
    TID.SNAIL_STOP_KEY: Flags.OBTAINED_SNAIL_STOP_ITEM,
    TID.LAZY_CARPENTER: Flags.CHORAS_1000_RECEIVED_TOOLS,
    TID.TABAN_GIFT_VEST: Flags.TABAN_VEST_GIVEN,
    TID.DENADORO_MTS_KEY: Flags.OBTAINED_DENADORO_KEY,

    # Other script treasures
    TID.TABAN_GIFT_HELM: Flags.TABAN_HELM_GIVEN,
    TID.TABAN_GIFT_SUIT: Flags.TABAN_SUIT_GIVEN,
    TID.JERKY_GIFT: Flags.PORRE_JERKY_ITEM_OBTAINED,
    TID.DENADORO_ROCK: Flags.OBTAINED_GOLD_ROCK,
    TID.LARUBA_ROCK: Flags.RECEIVED_SILVER_ROCK,
    TID.KAJAR_ROCK: Flags.OBTAINED_BLACK_ROCK,
    TID.BEKKLER_KEY: Flags.HAS_BEKKLER_ITEM,
    TID.CYRUS_GRAVE_KEY: Flags.MASAMUNE_UPGRADED,
    TID.SUN_KEEP_2300: Flags.MOONSTONE_COLLECTED_2300,
    TID.ARRIS_DOME_FOOD_LOCKER_KEY: Flags.OBTAINED_ARRIS_FOOD_ITEM,
    TID.LUCCA_WONDERSHOT: Flags.LUCCA_MAKING_WONDERSHOT,
    TID.TABAN_SUNSHADES: Flags.WONDERSHOT_SUNSHADES_RECEIVED,
    TID.TATA_REWARD: Flags.OBTAINED_TATA_ITEM,
    TID.TOMA_REWARD: Flags.OBTAINED_TOMA_ITEM,
    TID.MELCHIOR_FORGE_MASA: Flags.HAS_FORGED_MASAMUNE,
    TID.EOT_GASPAR_REWARD: Flags.HAS_GASPAR_ITEM,
    TID.FAIR_PENDANT: Flags.FAIR_PENDANT_PICKED_UP,
    TID.HUNTING_RANGE_NU_REWARD: Flags.HUNTING_RANGE_NU_REWARD,
    TID.ZEAL_MAMMON_MACHINE: Flags.HAS_USED_MAMMON_MACHINE,
    TID.MAGUS_CASTLE_FOUR_KIDS: Flags.MAGUS_CASTLE_GHOST_KIDS_CHEST,
    TID.MAGUS_CASTLE_SLASH_SWORD_FLOOR: Flags.MAGUS_CASTLE_SLASH_SWORD_TREASURE,
    TID.GUARDIA_PRISON_LUNCH_BAG: Flags.RECEIVED_PRISON_CELL_GIFT,
    TID.DORINO_BROMIDE_MAGIC_TAB: Flags.DORINO_BROMIDE_MAGIC_TAB,
    TID.GUARDIA_FOREST_POWER_TAB_600: Flags.OBTAINED_GUARDIA_FOREST_600_TAB,
    TID.GUARDIA_FOREST_POWER_TAB_1000: Flags.OBTAINED_GUARDIA_FOREST_1000_TAB,
    TID.MANORIA_CONFINEMENT_POWER_TAB: Flags.MANORIA_CONFINEMENT_POWER_TAB,
    TID.PORRE_MARKET_600_POWER_TAB: Flags.PORRE_MARKET_600_TAB,
    TID.DENADORO_MTS_SPEED_TAB: Flags.DENADORO_MTS_SPEED_TAB,
    TID.TOMAS_GRAVE_SPEED_TAB: Flags.WEST_CAPE_SPEED_TAB,
    TID.GIANTS_CLAW_CAVERNS_POWER_TAB: Flags.GIANTS_CLAW_CAVERNS_POWER_TAB,
    TID.GIANTS_CLAW_ENTRANCE_POWER_TAB: Flags.GIANTS_CLAW_ENTRANCE_POWER_TAB,
    TID.GIANTS_CLAW_TRAPS_POWER_TAB: Flags.GIANTS_CLAW_TRAPS_POWER_TAB,
    TID.SUN_KEEP_600_POWER_TAB: Flags.SUN_KEEP_600_POWER_TAB,
    TID.MEDINA_ELDER_SPEED_TAB: Flags.MEDINA_ELDER_SPEED_TAB,
    TID.MEDINA_ELDER_MAGIC_TAB: Flags.MEDINA_ELDER_MAGIC_TAB,
    TID.MAGUS_CASTLE_FLEA_MAGIC_TAB: Flags.MAGUS_CASTLE_FLEA_MAGIC_TAB,
    TID.MAGUS_CASTLE_DUNGEONS_MAGIC_TAB: Flags.MAGUS_CASTLE_DUNGEONS_MAGIC_TAB,
    TID.TRANN_DOME_SEALED_MAGIC_TAB: Flags.TRANN_DOME_SEALED_MAGIC_TAB,
    TID.ARRIS_DOME_SEALED_POWER_TAB: Flags.ARRIS_DOME_SEALED_POWER_TAB,
    TID.DEATH_PEAK_POWER_TAB: Flags.DEATH_PEAK_POWER_TAB,
    TID.BLACKBIRD_DUCTS_MAGIC_TAB: Flags.BLACKBIRD_DUCTS_MAGIC_TAB,
    TID.KEEPERS_DOME_MAGIC_TAB: Flags.OBTAINED_KEEPERS_DOME_MAGIC_TAB,
    TID.GENO_DOME_ATROPOS_MAGIC_TAB: Flags.GENO_DOME_ATROPOS_MAGIC_TAB,
    TID.GENO_DOME_CORRIDOR_POWER_TAB: Flags.GENO_DOME_CORRIDOR_POWER_TAB,
    TID.GENO_DOME_LABS_MAGIC_TAB: Flags.GENO_DOME_LABS_MAGIC_TAB,
    TID.GENO_DOME_LABS_SPEED_TAB: Flags.GENO_DOME_LABS_SPEED_TAB,
    TID.ENHASA_NU_BATTLE_MAGIC_TAB: Flags.ENHASA_NU_BATTLE,
    TID.ENHASA_NU_BATTLE_SPEED_TAB: Flags.ENHASA_NU_BATTLE,
    TID.KAJAR_SPEED_TAB: Flags.KAJAR_MAGIC_LAB_SPEED_TAB,
    TID.KAJAR_NU_SCRATCH_MAGIC_TAB: Flags.NU_SCRATCH_MAGIC_TAB,
    TID.LAST_VILLAGE_NU_SHOP_MAGIC_TAB: Flags.LAST_VILLAGE_NU_SHOP_MAGIC_TAB,
    TID.SUNKEN_DESERT_POWER_TAB: Flags.SUNKEN_DESERT_POWER_TAB,
    TID.MOUNTAINS_RE_NICE_MAGIC_TAB: Flags.MOUNTAINS_RE_NICE_MAGIC_TAB,
    TID.BEAST_NEST_POWER_TAB: Flags.BEAST_NEST_POWER_TAB,
    TID.MT_WOE_MAGIC_TAB: Flags.MT_WOE_MAGIC_TAB,
    TID.OCEAN_PALACE_ELEVATOR_MAGIC_TAB: Flags.OCEAN_PALACE_ELEVATOR_MAGIC_TAB,
    TID.OZZIES_FORT_GUILLOTINES_TAB: Flags.OZZIES_FORT_GUILLOTINES_TAB,
    TID.PROTO_DOME_PORTAL_TAB: Flags.PROTO_DOME_PORTAL_POWER_TAB,
    TID.NORTHERN_RUINS_HEROS_GRAVE_MAGIC_TAB: Flags.CYRUS_GRAVE_MAGIC_TAB,
    TID.CRONOS_MOM: Flags.MOM_GAVE_MONEY,
    TID.TRUCE_MAYOR_2F_OLD_MAN: CheckCounter(
        ctrando.memory.Memory.TRUCE_MAYOR_2F_GOLD_NPC_COUNTER, 2),
    TID.IOKA_SWEETWATER_TONIC: Flags.OBTAINED_SWEETWATER_HUT_TONICS,
    TID.DORINO_INN_POWERMEAL: Flags.OBTAINED_DORINO_INN_POWERMEAL,
    TID.YAKRA_KEY_CHEST: Flags.RESCUE_CHANCELLOR_1000,
    TID.COURTROOM_YAKRA_KEY: Flags.OBTAINED_YAKRA_KEY,
}


class CTRDIClient(SNIClient):
    """
    Game client for Chrono Trigger Rando Dalton Imperial
    """

    game = "Chrono Trigger: Rando Dalton Imperial"

    _loc_name_to_id = {str(loc): ITEM_ID_BASE + loc for loc in TID}

    def __init__(self):
        super().__init__()

    @staticmethod
    def _convert_to_sni_addressing(addr: int) -> int:
        """
        Convert a SNES address to the SNI address space.
        """
        return (addr - 0x7E0000) + WRAM_START

    @staticmethod
    def _is_chest_collected(event_data, chest_index: int) -> bool:
        """
        Check if the chest at the given index has been collected
        """
        chest_data_start = TREASURE_BASE_ADDR - EVENT_BASE_ADDR
        byte_offset = chest_index // 8
        bit = 1 << (chest_index % 8)

        return (event_data[chest_data_start + byte_offset] & bit) > 0

    @staticmethod
    def _is_script_treasure_collected(event_data, loc: TID) -> bool:
        """
        Check if a script based treasure has been collected
        """
        if loc not in _script_locations.keys():
            raise Exception(f"Unknown location: {str(loc)}")

        check_data = _script_locations[loc]
        offset = check_data.address - EVENT_BASE_ADDR
        if isinstance(check_data, Flags):
            # Standard memory flag
            return event_data[offset] & check_data.bit
        else:
            # Counter type check
            return event_data[offset] >= check_data.count

    def _can_track(
            self,
            ctx: SNIContext,
            event_data: typing.Optional[bytes],
            map_data: typing.Optional[bytes]) -> bool:
        """
        Check if the game is in a valid state for tracking.
        Tracking isn't valid on some maps or during certain cutscenes.
        """

        if map_data is None or event_data is None:
            # Error during read?
            return False

        # Using a time gate triggers a cutscene that overwrites event memory.
        # Don't track events when the event memory is messed up.
        # During gate travel, the first 4 bytes of event data are always set
        # to a predictable pattern, so don't track anything if we see that.
        if event_data[0:4] == b"@ABC":
            return False

        # Don't track on invalid maps like the title screen
        map_id = int.from_bytes(map_data, "little")
        if map_id in INVALID_TRACKING_LOCS:
            return False

        # This is a slightly naive check to make sure the game has valid
        # data loaded and isn't just junk from the system turning on.
        #
        # This tries to fix an issue where the game auto-completes on connect
        # due to junk data in memory on flashcarts.
        if map_id > MAX_MAP_ID:
            return False

    def _track_locations(
            self,
            ctx: SNIContext,
            event_data: typing.Optional[bytes]) -> list[int]:
        """
        Track which locations the player has collected.
        """
        new_locations: list[int] = []
        for loc, treasure in treasuretypes.get_base_treasure_dict().items():
            loc_id = self._loc_name_to_id[str(loc)]
            if loc_id not in ctx.checked_locations and loc_id not in new_locations:
                if isinstance(treasure, treasuretypes.ChestTreasure):
                    if self._is_chest_collected(event_data, treasure.chest_index):
                        new_locations.append(loc_id)
                else:
                    # Script based treasures
                    if self._is_script_treasure_collected(event_data, loc):
                        new_locations.append(loc_id)

        return new_locations

    @classmethod
    async def _deliver_next_item(cls, ctx: SNIContext):
        """
        Deliver the next available item to the player if there are
        any items waiting to be delivered.
        """
        from SNIClient import snes_read, snes_buffered_write, snes_flush_writes

        item_buf = await snes_read(
            ctx, cls._convert_to_sni_addressing(RECEIVED_ITEM_ADDR), 1)

        item_cnt = await snes_read(
            ctx, cls._convert_to_sni_addressing(RECEIVED_ITEM_CNT), 1)

        if item_cnt is None or \
                item_buf is None or \
                item_buf[0] != 0:
            # Read failed or an item is already in the delivery buffer
            return

        if len(ctx.items_received) > item_cnt[0]:
            item = ctx.items_received[item_cnt[0]]
            in_game_id = item.item - ITEM_ID_BASE

            if in_game_id <= MAX_IN_GAME_ITEM_ID:
                snes_buffered_write(
                    ctx,
                    cls._convert_to_sni_addressing(RECEIVED_ITEM_ADDR),
                    bytes[in_game_id])

                await snes_flush_writes(ctx)

    async def _handle_victory_condition(
            self, ctx: SNIContext, event_data: bytes):
        """
        Check if the player has achieved the goal.
        """
        offset = VICTORY_ADDR - EVENT_BASE_ADDR
        victory = (event_data[offset] & VICTORY_FLAG) > 0

        if victory and not ctx.finished_game:
            # Notify the server that the player beat the game
            ctx.finished_game = True
            await ctx.send_msg(
                [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

    @override
    async def validate_rom(self, ctx: SNIContext) -> bool:
        from SNIClient import snes_read

        data = await snes_read(ctx, VALIDATION_ADDR, VALIDATION_SIZE)
        if data is None:
            return False

        # TODO: Actual slot validation
        return True

    @override
    async def game_watcher(self, ctx: SNIContext) -> None:
        from SNIClient import snes_read

        if not ctx.allow_collect or ctx.server is None or ctx.slot is None:
            # Client isn't fully connected yet
            return False

        # Read the map and event data needed for subsequent checks
        map_data = await snes_read(ctx, LOCATION_ADDR, 2)
        event_addr = self._convert_to_sni_addressing(
            EVENT_BASE_ADDR), EVENT_BLOCK_SIZE
        event_data = await snes_read(ctx, event_addr)

        # Check if the game is in a valid state for tracking then
        # handle new locations and item delivery.
        if self._can_track(ctx, event_data, map_data):
            new_locations = self._track_locations(ctx, event_data)
            self._deliver_next_item(ctx)

            if len(new_locations) > 0:
                # Send newly checked locations to the server
                await ctx.send_msgs(
                    [{"cmd": "LocationChecks", "locations": new_locations}])

            self._handle_victory_condition(ctx, event_data)

    @override
    async def deathlink_kill_player(self, ctx: SNIContext) -> None:
        """
        Not implmented for RDI
        """
        pass
