from . import memory as mem
from .asm import assemble
from .asm import instructions as inst
from .jprom import JPRom


def apply_entrance_rando(rom: JPRom):
    """
    Apply randomization to entrance locations.
    """
