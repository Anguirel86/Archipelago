from Options import OptionDict, OptionList


class Locations(OptionList):
    display_name = "locations"


class Items(OptionList):
    display_name = "items"


class Rules(OptionDict):
    display_name = "rules"


class Victory(OptionList):
    display_name = "victory"