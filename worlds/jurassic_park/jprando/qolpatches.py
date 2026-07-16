from .asm import assemble
from .asm import instructions as inst

from .jprom import JPRom

from . import memory as mem


def patch_health_regen(rom: JPRom):
    """
    Patch in automatic health regen over time.

    Hook into the routine that charges the cattle prod and jump
    to a subroutine that decrements the damage counter.

    NOTE: Full charge in buildings is 0x20, but only 0x1F on the overworld.
          This applies the same patch for both, and caps charge at 0x1F
    """

    health_regen_tick = 0x02

    jump_rom_addr_ow = 0x32D3
    jump_rom_addr_inside = 0x7CCA

    AM = inst.AddressingMode
    routine: assemble.ASMList = [
        inst.LDA(mem.DAMAGE_TAKEN_ADDR, AM.LNG),
        inst.CMP(0x0000, AM.IMM16),
        inst.BEQ("health_regen_end"),  # Health is already full
        inst.CMP(health_regen_tick, AM.IMM16),
        inst.BCC("top_off_health"),  # Health missing is less than a full tick
        inst.SEC(),
        inst.SBC(health_regen_tick, AM.IMM16),
        inst.STA(mem.DAMAGE_TAKEN_ADDR, AM.LNG),
        inst.BRA("health_regen_end"),
        "top_off_health",
        inst.LDA(0x00, AM.IMM16),
        inst.STA(mem.DAMAGE_TAKEN_ADDR, AM.LNG),
        "health_regen_end",

        # Handle cattle prod recharge that we wiped out with the patch
        inst.LDA(mem.CATTLE_PROD_CHARGE_ADDR, AM.LNG),
        inst.CMP(0x1F, AM.IMM16),
        inst.BCS("done"),
        inst.INC(mode=AM.NO_ARG),
        inst.STA(mem.CATTLE_PROD_CHARGE_ADDR, AM.LNG),
        "done",
        inst.RTL()
    ]

    # Write the assembled function to the ROM
    snippet = assemble.ASMSnippet(routine)
    assembled_bytes = snippet.to_bytes()

    patch_addr = rom.reserve(len(assembled_bytes))
    cpu_addr = rom.to_cpu_addr(patch_addr)
    rom.write(patch_addr, assembled_bytes)

    # Patch the original routines to call the new function
    jump_patch: assemble.ASMList = [
        inst.JSL(cpu_addr, AM.LNG),
    ]

    jump_snippet = assemble.ASMSnippet(jump_patch)

    # Overworld patch
    rom.write_patch_with_padding(
        jump_rom_addr_ow,
        jump_rom_addr_ow + 11,
        jump_snippet.to_bytes())

    # Inside buildings
    rom.write_patch_with_padding(
        jump_rom_addr_inside,
        jump_rom_addr_inside + 23,
        jump_snippet.to_bytes())


def patch_infinite_lives(rom: JPRom):
    nop3 = bytes([0xEA] * 3)
    rom.write(0x80CD, nop3)


def patch_infinite_cattle_prod(rom: JPRom):
    nop3 = bytes([0xEA] * 3)
    rom.write(0x327E, nop3)  # overworld
    rom.write(0x10BCD6, nop3)  # inside buildings


def patch_infinite_ammo(rom: JPRom):
    """
    Patch to grant the player infinite ammo.
    """
    nop3 = bytes([0xEA] * 3)

    # primary weapon
    rom.write(0x2F99, nop3)  # overworld
    # in buildings
    rom.write(0x10AF2B, nop3)  # Tranq darts
    rom.write(0x10AEA3, nop3)  # Shotgun
    rom.write(0x10AFC1, nop3)  # Rockets

    # Secondary weapon
    # Overworld
    rom.write(0x3053, nop3)  # Bolas
    rom.write(0x3156, nop3)  # Gas canisters
    # in buildings
    rom.write(0x10AB84, nop3)  # Bolas
    rom.write(0x10A85E, nop3)  # Gas canisters


def patch_gates_open_together(rom: JPRom):
    """
    When one gate is opened, all gates are opened
    """
    nop3 = bytes([0xEA] * 3)
    # NOP the LDA #$0000 in each routine that closes the gate
    rom.write(0x132A80, nop3)  # Gate 1 routine
    rom.write(0x132A93, nop3)  # Gate 2 routine
    rom.write(0x132AA6, nop3)  # Gate 3 routine
