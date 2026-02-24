from dataclasses import dataclass

from Options import PerGameCommonOptions, Range, Toggle


class RequiredDinoEggs(Range):
    """Number of eggs required to beat the game"""
    display_name = "Required Eggs"
    range_start = 0
    range_end = 18
    default = 18


class EnableTraps(Toggle):
    """Enable shock and dilophosaurus spit traps"""
    display_name = "Enable Traps"


# TODO: Maybe groups these into a "QoL" options group?
# TODO: Is linked gates worth including?
#       Reduces backtracking some
class LinkedGates(Toggle):
    """Opening one gate opens them all"""
    display_name = "Linked Gates"


class PassiveHealthRegen(Toggle):
    """Enable passive health regen"""
    display_name = "Passive Health Regen"


class InfiniteLives(Toggle):
    """Grant the player infinite lives"""
    display_name = "Infinite Lives"


class InfiniteCattleProd(Toggle):
    """Cattle Prod never runs out of charge"""
    display_name = "Infinite Cattle Prod"


class InfiniteAmmo(Toggle):
    """Infinite ammo for primary and secondary weapons"""
    display_name = "Infinite Ammo"


@dataclass
class JPOptions(PerGameCommonOptions):
    eggs_required: RequiredDinoEggs
    enable_traps: EnableTraps
    passive_health_regen: PassiveHealthRegen
    infinite_lives: InfiniteLives
    infinite_cattle_prod: InfiniteCattleProd
    infinite_ammo: InfiniteAmmo
    linked_gates: LinkedGates
