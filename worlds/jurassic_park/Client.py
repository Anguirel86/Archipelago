import base64
import logging
from time import time

from NetUtils import ClientStatus
from worlds.AutoSNIClient import SNIClient

from .Items import get_name_to_id_mapping, JP_ITEM_ID_BASE
from .Locations import get_name_to_id_mapping as loc_name_to_id_mapping
from .Locations import get_id_to_name_mapping as loc_id_to_name_mapping

from .jprando import memory as mem

snes_logger = logging.getLogger("snes")

SNI_WRAM_START = 0xF50000

# Table of egg locations to their offsets in the egg table
egg_table: dict[str, int] = {
    "Northwest Triceratops Egg": 0,
    "North Utility Shed Egg": 2,
    "North Mountain Egg": 4,
    "North Raptor Nest Egg": 6,
    "Behind Visitor Center Egg": 8,
    "Visitor Center Roof Egg": 10,
    "Jungle Triceratops Egg": 12,
    "Jungle Traps Egg": 14,
    "Jungle Dead End Egg": 16,
    "Nublar Utility Shed Mountain Egg": 18,
    "Nublar Utility Shed South Egg": 20,
    "East Canal Egg": 22,
    "Park Gate Egg": 24,
    "East Mountain Egg": 26,
    "East Harbor Egg": 28,
    "South Raptor Nest Egg": 30,
    "Ship Roof Egg": 32,
    "Helipad Egg": 34
}

id_card_table: dict[str, int] = {
    "John Hammond ID Card": 0,
    "Ellie Sattler ID Card": 2,
    "Robert Muldoon ID Card": 4,
    "Alan Grant ID Card": 6,
    "Donald Gennaro ID Card": 8,
    "Ray Arnold ID Card": 10,
    "Dennis Nedry ID Card": 12,
    "Doctor Wu ID Card": 14,
    "Ian Malcolm ID Card": 16
}

battery_table: dict[str, int] = {
    "North Utility Shed Battery": 0,
    "Raptor Pen Battery": 1,
    "Visitor Center Battery": 2,
    "Beach Utility Shed Battery": 3,
    "Nublar Utility Shed Battery": 4,
    "Ship Battery": 5
}


class JPClient(SNIClient):
    """
    Client for the Jurassic Park SNES randomizer
    """

    game = "Jurassic Park"
    patch_suffix = [".apjp"]

    _loc_name_to_id = loc_name_to_id_mapping()
    _loc_id_to_name = loc_id_to_name_mapping()
    _item_name_to_id = get_name_to_id_mapping()

    def __init__(self):
        super().__init__()

    @staticmethod
    def _conv_to_sni(addr: int) -> int:
        return (addr - 0x7E0000) + SNI_WRAM_START

    @staticmethod
    def _to_u16(data: bytes, idx: int) -> int:
        return int.from_bytes(
            data[idx:idx+2], byteorder="little", signed=False)

    async def _can_track(self, ctx) -> bool:
        """
        Check if we're in a state where we can perform tracking.
        The client must be connected and the game must be started.
        """
        if not ctx.allow_collect or ctx.server is None or ctx.slot is None:
            # CLient isn't connected
            return False

        from SNIClient import snes_read
        data = await snes_read(ctx, self._conv_to_sni(mem.IN_GAME_BYTE), 1)

        if data is None:
            # Read failed?
            return False

        return data[0] == mem.IN_GAME_VAL

    async def _track_egg_locations(self, ctx) -> list[int]:
        """
        Track collected egg locations.
        Return a list of IDs of any newly checked locations.

        Should only be called if _can_track() is true
        """
        from SNIClient import snes_read
        egg_data = await snes_read(
            ctx, self._conv_to_sni(mem.EGG_TABLE_START), mem.EGG_TABLE_SIZE)

        if not egg_data:
            return []

        new_locs: list[int] = []
        for name, idx in egg_table.items():
            loc_id = self._loc_name_to_id[name]
            found = self._to_u16(egg_data, idx) == mem.EGG_COLLECTED_VAL
            if found and loc_id not in ctx.checked_locations:
                new_locs.append(loc_id)

        return new_locs

    async def _track_id_card_locations(self, ctx) -> list[int]:
        """
        Track collected ID card locations
        """
        from SNIClient import snes_read
        card_data = await snes_read(
            ctx, self._conv_to_sni(mem.ID_TABLE_BASE), mem.ID_TABLE_SIZE)

        if not card_data:
            return []

        new_locs: list[int] = []
        for name, idx in id_card_table.items():
            loc_id = self._loc_name_to_id[name]
            found = (self._to_u16(card_data, idx)
                     & mem.CHECKED_ID_CARD_LOC) != 0
            if found and loc_id not in ctx.checked_locations:
                new_locs.append(loc_id)

        return new_locs

    async def _track_battery_locations(self, ctx) -> list[int]:
        """
        Track night vision goggle battery locations.
        """
        from SNIClient import snes_read
        batt_data = await snes_read(
            ctx, self._conv_to_sni(mem.BATT_TABLE_START), mem.BATT_TABLE_SIZE)

        if not batt_data:
            return []

        new_locs: list[int] = []
        for name, idx in battery_table.items():
            loc_id = self._loc_name_to_id[name]
            found = (batt_data[idx] & mem.CHECKED_BATT_LOC) != 0
            if found and loc_id not in ctx.checked_locations:
                new_locs.append(loc_id)

        return new_locs

    async def _track_event_locations(self, ctx) -> list[int]:
        """
        Track event locations.
        """
        from SNIClient import snes_read

        # Most of the events are clustered starting at 0x7E0265
        event_data = await snes_read(
            ctx, self._conv_to_sni(0x7E0265), 0x40)

        new_locs: list[int] = []
        if not event_data:
            return new_locs

        def check_event(data: bytes, idx: int, name: str) -> bool:
            val = self._to_u16(data, idx)
            complete = (val & 0xFF00) != 0
            loc_id = self._loc_name_to_id[name]
            if complete and loc_id not in ctx.checked_locations:
                new_locs.append(loc_id)

        check_event(event_data, 0, "Security Level 1")
        check_event(event_data, 2, "Security Level 2")
        # Index 4 is the RAM for the current building's battery
        check_event(event_data, 6, "Turn on Generator")
        check_event(event_data, 8, "Reboot Park Systems")
        check_event(event_data, 10, "Block Raptor Pen Door")
        check_event(event_data, 12, "Clear Ship")
        check_event(event_data, 14, "Destroy Raptor Nest")
        check_event(event_data, 16, "Contact Mainland")
        check_event(event_data, 34, "Activate Motion Sensors")

        # A few events are in another memory region
        # The nerve gas flag goes to 0x0001 when collected and then to 0x002
        # when it has been deployed in the raptor nest
        nerve_gas = await snes_read(ctx, self._conv_to_sni(0x7E1DEF), 2)
        if nerve_gas:
            val = self._to_u16(nerve_gas, 0)
            loc_id = self._loc_name_to_id["Collect Nerve Gas"]
            if val > 0 and loc_id not in ctx.checked_locations:
                new_locs.append(loc_id)

        contact_ship = await snes_read(
            ctx, self._conv_to_sni(mem.CONTACTED_SHIP), 2)
        if contact_ship:
            val = self._to_u16(contact_ship, 0)
            loc_id = self._loc_name_to_id["Contact Ship"]
            if val == 0xFFFF and loc_id not in ctx.checked_locations:
                new_locs.append(loc_id)

        return new_locs

    async def _check_win(self, ctx) -> bool:
        """
        Check if the player has escaped the island.
        """
        # TODO: The victory address is wrong.
        #       It looks like it might be used for some flag to show a text box?
        from SNIClient import snes_read
        data = await snes_read(
            ctx, self._conv_to_sni(mem.VICTORY_ADDR), 2)

        if not data:
            return False

        victory_flag = self._to_u16(data, 0)

        return victory_flag == 0xFFFF

    async def _deliver_next_item(self, ctx):
        """
        If there are any items waiting to be sent to the player,
        send the next one in the queue now.
        """
        from SNIClient import snes_read, snes_buffered_write, snes_flush_writes

        data = await snes_read(ctx, self._conv_to_sni(mem.ITEM_RCV_ADDR), 2)
        if data is None:
            return

        if data[0] != 0:
            # There is already an item in the receive queue
            # Don't try to send another.
            return

        num_items_delivered = data[1]
        if len(ctx.items_received) > num_items_delivered:
            item = ctx.items_received[num_items_delivered]

            item_id = item.item - JP_ITEM_ID_BASE

            snes_buffered_write(
                ctx,
                self._conv_to_sni(mem.ITEM_RCV_ADDR),
                bytes([item_id]))

            await snes_flush_writes(ctx)

    async def _temu_save_feature(self, ctx) -> None:
        """
        Jurassic Park doesn't natively support a save feature.
        Use the AP location data to mimic a save feature and
        set appropriate event/location flags.
        """
        from SNIClient import snes_read, snes_buffered_write, snes_flush_writes

        data = await snes_read(ctx, self._conv_to_sni(mem.ITEM_RCV_ADDR), 2)
        if data is None:
            return

        # Of the number of items delivered is zero, but the user has done
        # location checks already, then they are probably reloading an
        # in-progress game.  This is when we want to "load the save".
        num_items_delivered = data[1]
        if num_items_delivered == 0 and len(ctx.checked_locations) > 0:
            # Set egg locations
            has_writes = False
            nerve_gas_counter = 0
            for loc in ctx.checked_locations:
                has_writes = True
                # I think checked locations are int IDs
                # loc_id = loc - JP_ITEM_ID_BASE
                loc_name = self._loc_id_to_name[loc]
                snes_logger.info(f"Temu save -  {loc_name} : {loc}")

                if loc_name in egg_table:
                    offset = egg_table[loc_name]
                    snes_buffered_write(
                        ctx,
                        self._conv_to_sni(mem.EGG_TABLE_START) + offset,
                        bytes([0x00, 0x00]))
                elif loc_name in id_card_table:
                    offset = id_card_table[loc_name]
                    flag = mem.CHECKED_ID_CARD_LOC.to_bytes(2, "little")
                    snes_buffered_write(
                        ctx,
                        self._conv_to_sni(mem.ID_TABLE_BASE) + offset,
                        flag)
                elif loc_name in battery_table:
                    offset = battery_table[loc_name]
                    flag = mem.CHECKED_BATT_LOC.to_bytes(1)
                    snes_buffered_write(
                        ctx,
                        self._conv_to_sni(mem.BATT_TABLE_START) + offset,
                        flag)
                else:
                    # This is an event location
                    evt_addr = self._conv_to_sni(0x7E0265)
                    flag = 0xFFFF.to_bytes(2, "little")
                    if loc_name == "Security Level 1":
                        snes_buffered_write(ctx, evt_addr, flag)
                    elif loc_name == "Security Level 2":
                        snes_buffered_write(ctx, evt_addr + 2, flag)
                    elif loc_name == "Turn on Generator":
                        snes_buffered_write(ctx, evt_addr + 6, flag)
                    elif loc_name == "Reboot Park Systems":
                        snes_buffered_write(ctx, evt_addr + 8, flag)
                    elif loc_name == "Block Raptor Pen Door":
                        snes_buffered_write(ctx, evt_addr + 10, flag)
                    elif loc_name == "Clear Ship":
                        snes_buffered_write(ctx, evt_addr + 12, flag)
                    elif loc_name == "Destroy Raptor Nest":
                        nerve_gas_counter = 2
                        snes_buffered_write(ctx, evt_addr + 14, flag)
                    elif loc_name == "Contact Mainland":
                        snes_buffered_write(ctx, evt_addr + 16, flag)
                    elif loc_name == "Activate Motion Sensors":
                        snes_buffered_write(ctx, evt_addr + 34, flag)
                    elif loc_name == "Collect Nerve Gas":
                        nerve_gas_counter = max(1, nerve_gas_counter)
                    elif loc_name == "Contact Ship":
                        snes_buffered_write(
                            ctx, self._conv_to_sni(mem.CONTACTED_SHIP), flag)

            if nerve_gas_counter > 0:
                # This is a separate flag tracking the nerge gas canister.
                # 0 - Not collected
                # 1 - Collected
                # 2 - Deployed in the raptor nest
                snes_buffered_write(
                    ctx,
                    self._conv_to_sni(mem.NERVE_GAS_FLAG_ADDR),
                    nerve_gas_counter.to_bytes(2, "little"))

            if has_writes:
                snes_logger.info("Flushing snes write queue")
                await snes_flush_writes(ctx)

    async def game_watcher(self, ctx) -> None:
        can_track = await self._can_track(ctx)
        if not can_track:
            return

        # Check if we need to load "save data"
        await self._temu_save_feature(ctx)

        new_locs: list[int] = await self._track_egg_locations(ctx)
        new_locs += await self._track_id_card_locations(ctx)
        new_locs += await self._track_battery_locations(ctx)
        new_locs += await self._track_event_locations(ctx)

        if len(new_locs) > 0:
            await ctx.send_msgs(
                [{"cmd": "LocationChecks", "locations": new_locs}])

        await self._deliver_next_item(ctx)

        # TODO: Death link

        if not ctx.finished_game:
            victory = await self._check_win(ctx)
            if victory:
                await ctx.send_msgs(
                    [{"cmd": "StatusUpdate",
                      "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True

    async def validate_rom(self, ctx) -> bool:
        """
        Validate whether the currently connected ROM is
        a Jurassic Park SNES game for this player.
        """
        from SNIClient import snes_read

        data = await snes_read(ctx, mem.VALIDATION_ADDR, mem.VALIDATION_SIZE)

        if data is None or data[0:4] != b"APJP":
            return False

        # Name should be a 8 byte hash of the player's settings name
        # TODO: Include seed info in validation so ROMs can't be reused?
        name = data[4:12]

        ctx.game = self.game
        ctx.items_handling = 0b011
        ctx.rom = name
        ctx.allow_collect = True

        # TODO: deathlink init
        return True

    async def dealink_kill_player(self, ctx) -> None:
        """
        Share the misery.
        """
        can_track = await self._can_track(ctx)
        if not can_track:
            return

        from SNIClient import (
            DeathState, snes_buffered_write, snes_flush_writes
        )

        # 0x0100 would do, but there's no kill like overkill
        # This matches dark room damage for the insta-kill
        snes_buffered_write(
            ctx,
            self._conv_to_sni(mem.DAMAGE_TAKEN_ADDR),
            int.to_bytes(0x200), byteorder="little")
        await snes_flush_writes(ctx)

        ctx.last_death_link = time()
        ctx.death_state = DeathState.dead
