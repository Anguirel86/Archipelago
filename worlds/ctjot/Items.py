from BaseClasses import ItemClassification, Item

import json
from typing import NamedTuple


class ItemData(NamedTuple):
    """
    Store the data associated with a Chrono Trigger item.
    """
    name: str
    code: int
    item_type: str
    classification: ItemClassification


class CTJoTItemManager:
    """
    Manage item data.
    """
    _item_data_map = {}
    _ITEM_ID_START = 5000

    # Key items that lead to go mode or other progression
    _progression_items = ["Toma's Pop", "Bent Hilt", "Bent Sword",
                          "Dreamstone", "Ruby Knife", "Gate Key",
                          "Pendant", "Moon Stone", "PrismShard",
                          "C. Trigger", "Hero Medal", "Tools",
                          "JetsOfTime", "Grand Leon", "Clone",
                          "Jerky", "Robo's Rbn"]

    # Key items that are useful, but not progression
    _useful_items = ["Fragment"]

    # Some items to be used for junk fill in case more items are needed
    # TODO: Pick real filler items
    _junk_fill_items = ["Mop"]

    _characters = ["Crono", "Marle", "Lucca", "Robo", "Frog", "Ayla", "Magus"]

    def __init__(self):
        self._read_item_data()

    def _read_item_data(self):
        """
        Read the item_data file and populate the item DB
        """
        import pkgutil
        items = json.loads(pkgutil.get_data(__name__, "data/item_data.json").decode())
        for key, value in items.items():
            classification = ItemClassification.progression if key in self._progression_items \
                else ItemClassification.progression if key in self._characters \
                else ItemClassification.useful if key in self._useful_items \
                else ItemClassification.filler
            self._item_data_map[key] = ItemData(key, self._ITEM_ID_START + value, "CTJoTItem", classification)

    def get_item_data_by_name(self, item_name: str) -> ItemData:
        """
        Get item data
        """
        return self._item_data_map[item_name]

    def create_item(self, item_name: str, player: int) -> Item:
        """
        Create an AP Item for the given item name and player.
        """
        item = self.get_item_data_by_name(item_name)
        return Item(item_name, item.classification, item.code, player)

    def get_junk_fill_items(self) -> list[str]:
        """
        Get the list of items that can be used a junk fill.
        """
        return self._junk_fill_items

    def get_item_name_to_id_mapping(self) -> dict[str, int]:
        """
        Get a dictionary of item names to IDs for all possible items.
        """
        return {name: item.code for name, item in self._item_data_map.items()}

    @staticmethod
    def create_event_item(item_name: str, player: int) -> Item:
        """
        Create an item object for an event rather than a normal item.

        Used for creating character recruitments and victory event items.
        """
        return Item(item_name, ItemClassification.progression, None, player)
