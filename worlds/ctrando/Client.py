import logging

from NetUtils import ClientStatus, NetworkItem
from SNIClient import SNIContext

from worlds.AutoSNIClient import SNIClient

from ctrando.common.ctenums import TreasureID as TID
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
RECEIVE_ITEM_ADDR = 0x7E287A  # TODO: Update this - JoT value
RECEIVED_ITEM_CNT = 0x7E287C  # TODO: Update this - JoT value

LOCATION_ADDR = 0xF50100  # Already in SNI address space

# ROM/player/slot validation
VALIDATION_ADDR = ROM_START + 0x3F8C03  # TODO: Update this - JoT value
VALIDATION_SIZE = 0x20

INVALID_TRACKING_LOCS = [0x00, 0x1B1]
MAX_MAP_ID = 0x1FF


class RDIClient(SNIClient):
    """
    Game client for Chrono Trigger Rando Dalton Imperial
    """

    game = "Chrono Trigger Rando Dalton Imperial"

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

    def _track_locations(self, ctx: SNIContext) -> bool:
        """
        Track which locations the player has collected.
        """
        from SNIClient import snes_read

        if not ctx.allow_collect or ctx.server is None or ctx.slot is None:
            # Client isn't fully connected yet
            return False

        # Read the map and event data needed for subsequent checks
        map_data = await snes_read(ctx, LOCATION_ADDR, 2)
        event_data = await snes_read(
            ctx,
            self._convert_to_sni_addressing(EVENT_BASE_ADDR), EVENT_BLOCK_SIZE)

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
        # due to junk data in memory.
        if map_id > MAX_MAP_ID:
            return False

        new_locations: list[int] = []
        for loc, treasure in treasuretypes.get_base_treasure_dict().items():
            loc_id = self._loc_name_to_id[str(loc)]
            if loc_id not in ctx.checked_locations and loc_id not in new_locations:
                if isinstance(treasure, treasuretypes.ChestTreasure):
                    if self._is_chest_collected(event_data, treasure.chest_index):
                        new_locations.append(loc_id)
                elif isinstance(treasure, treasuretypes.ScriptTreasure):
                    # TODO: Other treasure types
                    #       Might need to pay attention to order if we need
                    #       to use the more exotic ones since a lot of them
                    #       subclass ScriptTreasure
                    pass

    async def validate_rom(self, ctx: SNIContext) -> bool:
        from SNIClient import snes_read

        data = await snes_read(ctx, VALIDATION_ADDR, VALIDATION_SIZE)
        if data is None:
            return False

        # TODO: Actual slot validation
        return True

    async def game_watcher(self, ctx: SNIContext) -> None:
        pass

    async def deathlink_kill_player(self, ctx: SNIContext) -> None:
        """
        Not implmented for RDI
        """
        pass
