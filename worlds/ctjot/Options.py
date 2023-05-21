from Options import FreeText, OptionDict, OptionList


class Locations(OptionList):
    display_name = "locations"


class Items(OptionList):
    display_name = "items"


class Rules(OptionDict):
    display_name = "rules"


class Victory(OptionList):
    display_name = "victory"


class GameMode(FreeText):
    """Game mode chosen by the user."""
    display_name = "Game Mode"


class ItemDifficulty(FreeText):
    """Game mode chosen by the user."""
    display_name = "ItemDifficulty"
