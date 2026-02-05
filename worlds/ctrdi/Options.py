from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, Range, Toggle

# TODO: Autogenerate these from arg specs?
#       Do we want to limit options somewhat so it's not
#       completely overwhelming?  Maybe a free text section
#       that gets interpreted as rando args for advanced stuff?
#       Just going to add a few options for now to test with


class XpScale(Range):
    """Factor by which to scale XP earned in battles"""
    # NOTE: It looks like Range only support integers
    #       But this field is a float in RDI
    display_name = "XP Scale"
    range_start = 1
    range_end = 10
    default = 4


class TpScale(Range):
    """Factor by which to scale TP earned in battles"""
    # NOTE: It looks like Range only support integers
    #       But this field is a float in RDI
    display_name = "TP Scale"
    range_start = 1
    range_end = 10
    default = 4


class TechOrder(Choice):
    """ Order in which techs are learned"""
    display_name = "Tech Order"
    option_vanilla = 0
    option_random_order = 1
    option_mp = 2
    option_mp_type = 3
    default = 0


class ShowFullTechList(Toggle):
    """The tech page of the menu will show all single techs"""
    display_name = "Show Full Tech List"


@dataclass
class CTRDIOptions(PerGameCommonOptions):
    xp_scale: XpScale
    tp_scale: TpScale
    tech_order: TechOrder
    show_full_tech_list: ShowFullTechList
