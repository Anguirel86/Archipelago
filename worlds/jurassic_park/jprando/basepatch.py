from . import memory as mem
from .asm import assemble
from .asm import instructions as inst
from .jprom import JPRom


def _patch_ap_item_handling(rom: JPRom):
    """
    Patch in a routine to handle delivering AP items to the player
    """
    spit_trap_duration = 0x60
    spit_trap_id = 0x40
    shock_trap_id = 0x41
    AM = inst.AddressingMode
    trap_routine: assemble.ASMList = [
        # Accumulator holds the item (trap) ID
        inst.REP(0x20),  # 16 bit mode
        inst.CMP(spit_trap_id, AM.IMM16),
        inst.BEQ("spit_trap"),
        inst.BRA("end"),
        "spit_trap",
        # Writing to 0x7E03BE causes the character to wander
        # when hit by dilophosaur spit.  The larger the value,
        # the longer the effect.
        # Only effective on the overworld
        inst.LDA(spit_trap_duration, AM.IMM16),
        inst.STA(mem.SPIT_TRAP_ADDR, AM.LNG),
        # inst.BRA("end"),
        # TODO: Shock trap here
        "end",
        inst.RTL(),
    ]
    trap_routine_assembled = assemble.assemble(trap_routine)
    trap_routine_addr = rom.reserve(len(trap_routine_assembled))

    # Egg handling routine
    egg_routine: assemble.ASMList = [
        inst.REP(0x20),
        # Decrement the eggs-remaining counter
        inst.LDA(mem.EGG_CNT_ADDR, AM.LNG),
        inst.BEQ("end"),  # Already at zero
        inst.SEC(),
        inst.DEC(mode=AM.NO_ARG),
        # If there are no eggs remaining, we need to set
        # the event flag for all eggs collected
        inst.BNE("still_eggs_left"),
        inst.STA(mem.EGG_CNT_ADDR, AM.LNG),
        inst.LDA(0xFFFF, AM.IMM16),
        inst.STA(mem.ALL_EGGS_COLLECTED, AM.LNG),
        inst.BRA("end"),
        "still_eggs_left",
        inst.STA(mem.EGG_CNT_ADDR, AM.LNG),
        "end",
        inst.RTL(),
    ]
    egg_routine_assembled = assemble.assemble(egg_routine)
    egg_routine_addr = rom.reserve(len(egg_routine_assembled))

    nerve_gas_routine: assemble.ASMList = [
        inst.REP(0x20),
        inst.LDA(mem.NERVE_GAS_FLAG_ADDR, AM.LNG),
        inst.ORA(mem.HAS_NERVE_GAS, AM.IMM16),
        inst.STA(mem.NERVE_GAS_FLAG_ADDR, AM.LNG),
        inst.RTL(),
    ]
    nerve_gas_routine_assembled = assemble.assemble(nerve_gas_routine)
    nerve_gas_routine_addr = rom.reserve(len(nerve_gas_routine_assembled))

    # ID cards are 16 bit flags, but we've split them in half to denote
    # the location being checked and the item being acquired.
    # Item ID from AP will be in A.
    id_card_routine: assemble.ASMList = [
        # Isolate the card index
        inst.LDA(mem.ITEM_RCV_ADDR, AM.LNG),
        inst.AND(0x0F, AM.IMM8),
        # Mult by 2 to get the byte offset of the card in the table
        inst.ASL(mode=AM.NO_ARG),
        inst.REP(0x20),
        inst.PHX(),
        inst.TAX(),
        inst.LDA(mem.ID_TABLE_BASE, AM.LNG_X),
        inst.ORA(mem.HAS_ID_CARD, AM.IMM16),
        inst.STA(mem.ID_TABLE_BASE, AM.LNG_X),
        inst.PLX(),
        inst.RTL(),
    ]
    id_card_routine_assembled = assemble.assemble(id_card_routine)
    id_card_routine_addr = rom.reserve(len(id_card_routine_assembled))

    # TODO: With this implementation, the player will have to leave the
    #       building and re-enter to trigger the local battery flag
    #       at 0x7E0269.  It should be possible to use the map
    #       indicator word at 0x7E16B5 to set this correctly if we get
    #       a battery for the current building.
    #       Though this will be a fair bit of code.
    battery_routine: assemble.ASMList = [
        # Isolate the battery index
        inst.LDA(mem.ITEM_RCV_ADDR, AM.LNG),
        inst.AND(0x0F, AM.IMM8),
        inst.PHX(),
        inst.TAX(),
        # Set the "acquired" part of the battery flag
        inst.LDA(mem.BATT_TABLE_START, AM.LNG_X),
        inst.ORA(mem.HAS_BATT, AM.IMM8),
        inst.STA(mem.BATT_TABLE_START, AM.LNG_X),
        inst.PLX(),
        inst.RTL(),
    ]
    battery_routine_assembled = assemble.assemble(battery_routine)
    battery_routine_addr = rom.reserve(len(battery_routine_assembled))

    filler_routine: assemble.ASMList = [
        inst.LDA(mem.ITEM_RCV_ADDR, AM.LNG),
        inst.REP(0x20),
        # Check/handle first aid kits
        inst.CMP(0x30, AM.IMM16),
        inst.BNE("check_primary_ammo"),
        # It's a first aid kit.  Fully restore health.
        inst.LDA(0x0000, AM.IMM16),
        inst.STA(mem.DAMAGE_TAKEN_ADDR, AM.LNG),
        inst.BRA("end"),
        "check_primary_ammo",
        inst.CMP(0x031, AM.IMM16),
        inst.BNE("check_secondary_ammo"),
        # Add 10 rounds to the current primary weapon ammo
        inst.LDA(mem.PRIMARY_WEAPON_AMMO, AM.LNG),
        inst.CLC(),
        inst.ADC(0xA, AM.IMM16),
        inst.STA(mem.PRIMARY_WEAPON_AMMO, AM.LNG),
        inst.BRA("end"),
        "check_secondary_ammo",
        inst.CMP(0x32, AM.IMM16),
        inst.BNE("end"),
        # Add 10 rounds to the current secondary weapon ammo
        inst.LDA(mem.SECONDARY_WEAPON_AMMO, AM.LNG),
        inst.CLC(),
        inst.ADC(0xA, AM.IMM16),
        inst.STA(mem.SECONDARY_WEAPON_AMMO, AM.LNG),
        "end",
        inst.RTL(),
    ]
    filler_routine_assembled = assemble.assemble(filler_routine)
    filler_routine_addr = rom.reserve(len(filler_routine_assembled))

    # This is the entry point for the AP item handling routine
    # We start out in 8 bit accum and reg mode
    item_routine: assemble.ASMList = [
        inst.REP(0x10),  # 16 bit index registers
        inst.SEP(0x20),  # 8 bit accumulator
        # Sometimes the B accumulator still has junk data in it, which can
        # break the ID card routine.  Clear it out to prevent issues.
        inst.LDA(0x00, AM.IMM8),
        inst.XBA(mode=AM.NO_ARG),
        inst.LDA(mem.ITEM_RCV_ADDR, AM.LNG),
        inst.BEQ("do_nothing"),  # no item to deliver
        # 0x01 is an egg
        inst.CMP(0x01, AM.IMM8),
        inst.BNE("check_nerve_gas"),
        inst.JSL(rom.to_cpu_addr(egg_routine_addr)),
        inst.BRA("end"),
        # 0x02 is the nerve gas canister
        "check_nerve_gas",
        inst.CMP(0x02, AM.IMM8),
        inst.BNE("check_id_cards"),
        inst.JSL(rom.to_cpu_addr(nerve_gas_routine_addr)),
        inst.BRA("end"),
        "check_id_cards",
        # Isolate the top "item type" nibble and jump to specialized
        # subroutines based on what type of item this is.
        inst.AND(0xF0, AM.IMM8),
        # Basically a jump table to handle different item types.
        # Items starting with 0x1X are ID cards
        inst.CMP(0x10, AM.IMM8),
        inst.BNE("check_batteries"),
        inst.JSL(rom.to_cpu_addr(id_card_routine_addr)),
        inst.BRA("end"),
        # Items starting with 0x2X are batteries
        "check_batteries",
        inst.CMP(0x20, AM.IMM8),
        inst.BNE("check_filler"),
        inst.JSL(rom.to_cpu_addr(battery_routine_addr)),
        inst.BRA("end"),
        "check_filler",
        inst.CMP(0x30, AM.IMM8),
        inst.BNE("check_traps"),
        inst.JSL(rom.to_cpu_addr(filler_routine_addr)),
        inst.BRA("end"),
        "check_traps",
        inst.CMP(0x40, AM.IMM8),
        inst.BNE("end"),  # nothing after traps
        inst.JSL(rom.to_cpu_addr(trap_routine_addr)),
        "end",
        # Increment the received counter
        inst.SEP(0x20),
        inst.LDA(mem.ITEM_CNT_ADDR, AM.LNG),
        inst.INC(mode=AM.NO_ARG),
        inst.STA(mem.ITEM_CNT_ADDR, AM.LNG),

        # Zero out the item received address to signal we're ready for another
        inst.LDA(0, AM.IMM8),
        inst.STA(mem.ITEM_RCV_ADDR, AM.LNG),
        "do_nothing",
        inst.SEP(0x30),  # Back to 8 bit mode
        inst.RTL(),
    ]

    item_routine_assembled = assemble.assemble(item_routine)
    item_routine_addr = rom.reserve(len(item_routine_assembled))

    # Write the new subroutines to the ROM
    rom.write(trap_routine_addr, trap_routine_assembled)
    rom.write(egg_routine_addr, egg_routine_assembled)
    rom.write(nerve_gas_routine_addr, nerve_gas_routine_assembled)
    rom.write(id_card_routine_addr, id_card_routine_assembled)
    rom.write(battery_routine_addr, battery_routine_assembled)
    rom.write(filler_routine_addr, filler_routine_assembled)
    rom.write(item_routine_addr, item_routine_assembled)

    # The indoor/outdoor hooks need to replace different functions since they
    # are part of separate loops.
    # Create a jump target for each that will call the function we're replacing
    # before jumping to the item handling routine.
    ow_trampoline: assemble.ASMList = [
        inst.JSL(0x81C63A),  # Call the thing we're replacing
        inst.JSL(rom.to_cpu_addr(item_routine_addr)),
        inst.RTL(),
    ]
    ow_tramp_assembled = assemble.assemble(ow_trampoline)
    ow_tramp_addr = rom.reserve(len(ow_tramp_assembled))
    rom.write(ow_tramp_addr, ow_tramp_assembled)

    indoor_trampoline: assemble.ASMList = [
        inst.JSL(0xA48E68),  # Call the thing we're replacing
        inst.JSL(rom.to_cpu_addr(item_routine_addr)),
        inst.RTL(),
    ]
    indoor_tramp_assembled = assemble.assemble(indoor_trampoline)
    indoor_tramp_addr = rom.reserve(len(indoor_tramp_assembled))
    rom.write(indoor_tramp_addr, indoor_tramp_assembled)

    # Install the indoor/outdoor hooks
    ow_hook: assemble.ASMList = [inst.JSL(rom.to_cpu_addr(ow_tramp_addr))]
    rom.write(0x00834E, assemble.assemble(ow_hook))

    indoor_hook: assemble.ASMList = [inst.JSL(rom.to_cpu_addr(indoor_tramp_addr))]
    rom.write(0x120551, assemble.assemble(indoor_hook))


def _patch_door_locks(rom: JPRom):
    """
    Apply an assembly patch to modify door locks to handle
    the new ID card storage scheme.

    In vanilla, ID cards are stored as 16 bit flags.
    0x0000 represents not collected, 0xFFFF (usually) means collected.
    This is not true for Hammond's ID card, which is 0x0001 when collected.

    Locked doors check for a non-zero value at the card's memory index
    in order to be unlocked.

    In order to separate out owning the ID card from checking the ID card
    location, location collected is stored as 0x00FF, and owning is 0xFF00
    """

    AM = inst.AddressingMode
    routine: assemble.ASMList = [
        # Reimplement the stuff we deleted to make a jump point
        inst.ASL(mode=AM.NO_ARG),
        inst.AND(0x00FE, AM.IMM16),
        inst.TAY(),
        inst.LDA((mem.ID_TABLE_BASE & 0xFFFF), AM.ABS_Y),
        inst.AND(mem.HAS_ID_CARD, AM.IMM16),
        inst.RTL(),
    ]

    assembled_bytes = assemble.assemble(routine)
    patch_addr = rom.reserve(len(assembled_bytes))
    rom.write(patch_addr, assembled_bytes)

    hook_addr_doors = 0x123F6F
    hook_addr_elevators = 0x1244F0
    hook: assemble.ASMList = [
        inst.NOP(),
        inst.NOP(),
        inst.NOP(),
        inst.NOP(),
        inst.JSL(rom.to_cpu_addr(patch_addr), AM.LNG),
    ]

    assembled_hook = assemble.assemble(hook)
    rom.write(hook_addr_doors, assembled_hook)
    rom.write(hook_addr_elevators, assembled_hook)

    # TODO: Patch computer "Inventory" screen


def _patch_id_card_pickup(rom: JPRom):
    """
    Patch the indoor routines that determine if the keycard
    gets loaded and placed on the floor to respect the new
    flag layout.

    Also patch the pickup routine to set only the "location" bits
    including the outdoor Hammond ID pickup.
    """

    id_table_base = 0x7E0253

    # Patch the item sprite loading
    AM = inst.AddressingMode
    routine: assemble.ASMList = [
        inst.LDA(id_table_base, AM.LNG_X),
        inst.AND(mem.CHECKED_ID_CARD_LOC, AM.IMM16),
        inst.RTL(),
    ]

    assembled_bytes = assemble.assemble(routine)
    patch_addr = rom.reserve(len(assembled_bytes))
    rom.write(patch_addr, assembled_bytes)

    hook_addr = 0x10A377
    hook: assemble.ASMList = [inst.JSL(rom.to_cpu_addr(patch_addr), AM.LNG)]

    rom.write(hook_addr, assemble.assemble(hook))

    # Patch indoor ID card item pickup
    # Replace the LDA 0xFFFF with LDA 0x00FF
    pickup_patch: assemble.ASMList = [
        inst.TAX(),
        inst.LDA(id_table_base, AM.LNG_X),
        inst.ORA(mem.CHECKED_ID_CARD_LOC, AM.IMM16),
        inst.RTL(),
    ]
    assembled_pickup_patch = assemble.assemble(pickup_patch)
    patch_addr = rom.reserve(len(assembled_pickup_patch))
    rom.write(patch_addr, assembled_pickup_patch)

    pickup_hook_addr = 0x10A38B
    # Now install the hook for the indoor ID pickup patch
    id_pickup_hook: assemble.ASMList = [inst.JSL(rom.to_cpu_addr(patch_addr))]
    rom.write(pickup_hook_addr, assemble.assemble(id_pickup_hook))

    # Patch the Hammond ID card pickup
    # This is the only ID card on the overworld
    hammond_id_patch: assemble.ASMList = [
        inst.TAX(),
        # Index is based on WRAM start, not id table start
        inst.LDA(0x7E0000, AM.LNG_X),
        inst.ORA(mem.CHECKED_ID_CARD_LOC, AM.IMM16),
        inst.STA(0x7E0000, AM.LNG_X),
        inst.LDA(0x00A8, AM.IMM16),
        inst.RTL(),
    ]
    assembled_bytes = assemble.assemble(hammond_id_patch)
    patch_addr = rom.reserve(len(assembled_bytes))
    rom.write(patch_addr, assembled_bytes)

    hammond_id_hook_addr = 0x004321
    hammond_id_hook: assemble.ASMList = [
        inst.NOP(),
        inst.NOP(),
        inst.JSL(rom.to_cpu_addr(patch_addr)),
    ]

    rom.write(hammond_id_hook_addr, assemble.assemble(hammond_id_hook))


def _patch_battery_pickup(rom: JPRom):
    """
    Patch the battery routines to split the flags into "collected" and "owned"

    The battery flags are one byte each.
    0x00 - Uncollected
    0xFF - Collected

    Split this byte in half, so that 0x0F means the location has been checked
    and 0xF0 means the battery item has been obtained.
    """

    # Patch the routine for picking up batteries
    AM = inst.AddressingMode
    batt_loc_routine: assemble.ASMList = [
        inst.LDA(mem.BATT_TABLE_START, AM.LNG_X),
        inst.ORA(mem.CHECKED_BATT_LOC, AM.IMM8),
        inst.STA(mem.BATT_TABLE_START, AM.LNG_X),
        inst.RTL(),
    ]

    assembled_bytes = assemble.assemble(batt_loc_routine)
    patch_addr = rom.reserve(len(assembled_bytes))
    rom.write(patch_addr, assembled_bytes)

    batt_loc_hook_addr = 0x10A65F
    batt_loc_hook: assemble.ASMList = [
        inst.JSL(rom.to_cpu_addr(patch_addr)),
        inst.REP(0x20),
    ]

    # This will also NOP out the instructions that set the current
    # building's battery status.
    rom.write_patch_with_padding(batt_loc_hook_addr, batt_loc_hook_addr + 13, assemble.assemble(batt_loc_hook))

    # Patch the routine that checks battery status on building entry
    batt_load_hook_addr = 0x12007E
    batt_load_routine: assemble.ASMList = [
        # This will cause 0x0F to be stored in the battery status byte instead
        # of 0xFF.  This is fine since dark rooms just check for non-zero.
        inst.AND(mem.HAS_BATT, AM.IMM16)
    ]
    rom.write(batt_load_hook_addr, assemble.assemble(batt_load_routine))

    # Patch the routine that determines whether the battery sprite should
    # appear on the ground.
    # Replace the AND(0x00FF)
    sprite_load_routine: assemble.ASMList = [inst.AND(0x00F0, AM.IMM16)]
    rom.write(0x10A636, assemble.assemble(sprite_load_routine))


def _patch_nerve_gas(rom: JPRom):
    """
    Split the nerve gas flag into a collected and owned pair.

    NOTE:
    This flag is a little more complicated.  In vanilla, the 16 bit word gets
    incremented by 1 when the nerve gas is picked up, then incremented to 2
    when the nerve gas is deployed.  So for splitting this flag, the MSB
    will still remain a counter, and the LSB will be a "normal" flag, where
    0x00 means the location hasn't been checked, and 0xFF means it has.
    """
    AM = inst.AddressingMode

    # TODO: Can't pick up the nerve gas location if the player
    #       has the nerve gas item in inventory.

    # Modify the nerve gas pickup code
    nerve_gas_routine: assemble.ASMList = [
        inst.JSL(0xA4DF0D),
        inst.LDA(mem.CHECKED_NERVE_GAS_LOC, AM.IMM16),
        inst.STA(mem.NERVE_GAS_FLAG_ADDR, AM.LNG),
        inst.RTL(),
    ]

    assembled_bytes = assemble.assemble(nerve_gas_routine)
    patch_addr = rom.reserve(len(assembled_bytes))
    rom.write(patch_addr, assembled_bytes)

    nerve_gas_hook_addr = 0x10A6FC
    nerve_gas_hook: assemble.ASMList = [inst.JSL(rom.to_cpu_addr(patch_addr)), inst.NOP(), inst.NOP(), inst.NOP()]
    rom.write(nerve_gas_hook_addr, assemble.assemble(nerve_gas_hook))

    # Modify the code to deploy the nerve gas in the raptor nest
    ng_deploy_routine: assemble.ASMList = [
        # Load the nerve gas flag and isolate the part that says
        # we actually have the item.
        inst.LDA(mem.NERVE_GAS_FLAG_ADDR, AM.LNG),
        inst.AND(0x00FF, AM.IMM16),
        # Replicate what we replaced here.
        # If the Z flag is clear, mimic the replaced branch and jump
        # to A2A692.  Otherwise, just jump back and keep processing.
        inst.BEQ("end"),
        inst.JMP(0xA1A692, AM.LNG),
        "end",
        inst.JMP(0xA1A68A + 4, AM.LNG),
    ]

    assembled_deploy_routine = assemble.assemble(ng_deploy_routine)
    deploy_addr = rom.reserve(len(assembled_deploy_routine))
    rom.write(deploy_addr, assembled_deploy_routine)

    # Jump to our new routine to load the modified nerve gas flag.
    ng_patch: assemble.ASMList = [inst.JMP(rom.to_cpu_addr(deploy_addr), AM.LNG), inst.NOP()]
    rom.write(0x10A68A, assemble.assemble(ng_patch))


def _add_ap_logo_tiles(rom: JPRom):
    """
    Overwrite the overworld egg tiles with the AP logo.
    """
    with open("ap-logo-tiles.bin", "rb") as file:
        tile_data = file.read()

    # TODO: Palette is going to be messed up
    #       Need to figure out how to fix this
    rom.write(0x0BB800, tile_data)

    # BB700 is the start of the overworld ID card tiles


def _patch_egg_pickup(rom: JPRom, eggs_required: int):
    """
    Modify the egg pickup routine so that it does not decrement the
    remaining egg counter.  This will be handled when eggs are
    delivered in the AP item patch.
    """
    # We can't just NOP the DEC call here since the next instruction relies
    # on the Z flag.  Loading a non-zero value to A here will always trigger
    # the branch, skipping the "All eggs collected" flag code.  We'll set this
    # flag in the AP Item handling code, so this should be ok.
    # Both instructions are three bytes, so no jump patch is needed.

    # TODO: Maybe hijack the text box here for an AP item related message
    #       instead of the default egg counter?
    AM = inst.AddressingMode
    routine: assemble.ASMList = [inst.LDA(0x0001, AM.IMM16)]
    rom.write(0x004E52, assemble.assemble(routine))

    # Set the user configured number of eggs required to complete the game
    # Overwrite the instruction that sets this initial value on new game.
    routine = [inst.LDA(eggs_required, AM.IMM16)]
    rom.write(0x00D7E9, assemble.assemble(routine))


def _patch_ap_player_id_info(rom: JPRom, player_name: bytes):
    """
    Reserve some ROM space for player identifying info.
    Write "APJP" followed by a hash of the player name (8 bytes)
    """
    # NOTE: This has to be done before any other patches to ensure
    #       that we always get the same location (0x20_0000).
    addr = rom.reserve(0x20)
    rom.write(addr, b"APJP")
    rom.write(addr + 4, player_name)


def _patch_in_game_byte(rom: JPRom):
    """
    Set a byte in memory during game init that can be
    used to tell the client when tracking is available.

    """
    # TODO: It looks like the init code runs again on death.
    #       And when leaving buildings?
    #       This is probably ok?  Investigate.

    AM = inst.AddressingMode
    routine: assemble.ASMList = [
        # These STZs were erased to make room for our subroutine call
        inst.STZ(0x9A, AM.DIR),
        inst.STZ(0x9C, AM.DIR),
        inst.SEP(0x20),  # 8 bit accumulator
        inst.LDA(mem.IN_GAME_VAL, AM.IMM8),
        inst.STA(mem.IN_GAME_BYTE, AM.LNG),
        inst.REP(0x20),  # 16 bit accumulator
        inst.RTL(),
    ]
    assembled_routine = assemble.assemble(routine)
    patch_addr = rom.reserve(len(assembled_routine))
    rom.write(patch_addr, assembled_routine)

    patch: assemble.ASMList = [inst.JSL(rom.to_cpu_addr(patch_addr))]
    # This gets installed near the end of initialization, shortly before
    # the game enters its main loop.
    rom.write(0x00829C, assemble.assemble(patch))


def apply_ap_base_patch(rom: JPRom, player_name: bytes, eggs_required: int):
    """
    Apply the base patches to modify the game to be a randomizer
    and work with Archipelago.
    """
    _patch_ap_player_id_info(rom, player_name)
    _patch_ap_item_handling(rom)
    _patch_door_locks(rom)
    _patch_id_card_pickup(rom)
    _patch_battery_pickup(rom)
    # _patch_nerve_gas(rom)
    _patch_egg_pickup(rom, eggs_required)
    _patch_in_game_byte(rom)
    # _add_ap_logo_tiles(rom)
