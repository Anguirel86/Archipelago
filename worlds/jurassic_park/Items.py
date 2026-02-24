from dataclasses import dataclass
from typing import Optional

from BaseClasses import Item, ItemClassification as IC, MultiWorld

JP_ITEM_ID_BASE = 64_000_000


@dataclass
class ItemData():
    id: Optional[int]
    classification: Optional[IC]
    is_event: bool


item_table: dict[str, ItemData] = {
    "Egg": ItemData(0x01, IC.progression, False),
    # "Nerve Gas Canister": ItemData(0x02, IC.progression, False),

    # ID cards
    # Card IDs are in order of the ID card table in the game RAM
    "John Hammond ID Card": ItemData(0x10, IC.progression, False),
    "Ellie Sattler ID Card": ItemData(0x11, IC.progression, False),
    "Robert Muldoon ID Card": ItemData(0x12, IC.progression, False),
    "Alan Grant ID Card": ItemData(0x13, IC.progression, False),
    "Donald Gennaro ID Card": ItemData(0x14, IC.progression, False),
    "Ray Arnold ID Card": ItemData(0x15, IC.progression, False),
    "Dennis Nedry ID Card": ItemData(0x16, IC.progression, False),
    "Doctor Wu ID Card": ItemData(0x17, IC.progression, False),
    "Ian Malcolm ID Card": ItemData(0x18, IC.progression, False),

    # Batteries
    # Battery IDs are in order of the battery table in the game RAM
    "North Utility Shed Battery": ItemData(0x20, IC.progression, False),
    "Raptor Pen Battery": ItemData(0x21, IC.progression, False),
    "Visitor Center Battery": ItemData(0x22, IC.progression, False),
    "Beach Utility Shed Battery": ItemData(0x23, IC.progression, False),
    "Nublar Utility Shed Battery": ItemData(0x24, IC.progression, False),
    "Ship Battery": ItemData(0x25, IC.progression, False),

    # Filler items
    "First Aid Kit": ItemData(0x30, IC.filler, False),
    "Primary Ammo": ItemData(0x31, IC.filler, False),
    "Secondary Ammo": ItemData(0x32, IC.filler, False),

    # Traps
    "Dilophosaur Spit Trap": ItemData(0x40, IC.trap, False),
    "Shock Trap": ItemData(0x41, IC.trap, False),  # NOTE: Not yet implemented
}

EGG_COUNT = 18

filler_items: list[str] = ["Fist Aid Kit", "Primary Ammo", "Secondary Ammo"]


class JPItem(Item):
    game = "Jurassic Park"


def create_item(name: str, player: int) -> JPItem:
    """
    Create the requested item
    """
    if name not in item_table:
        raise Exception(f"{name} is not a valid Jurassic Park item")

    item_data = item_table[name]
    return JPItem(name,
                  item_data.classification,
                  item_data.id + JP_ITEM_ID_BASE,
                  player)


def create_all_progression_items(player: int) -> list[JPItem]:
    """
    Create all items for this player
    """
    items = []
    for name, item_data in item_table.items():
        if item_data.classification is not IC.progression:
            continue

        # Eggs are a special case.  We need multiple
        if name == "Egg":
            for i in range(EGG_COUNT):
                items.append(create_item(name, player))
        else:
            items.append(create_item(name, player))

    return items


def get_random_filler_name(multiworld: MultiWorld) -> str:
    return multiworld.random.choice(filler_items)


def create_filler_items(player: int, include_traps: bool) -> list[JPItem]:
    """
    Create filler items and traps to round out the item list.
    """
    # Naive implementation, just hardcode filler/trap lists.
    # For now we have 11 spots (event locations) that will need filler.
    items: list[JPItem] = []
    if include_traps:
        items.append(create_item("First Aid Kit", player))
        items.append(create_item("First Aid Kit", player))
        items.append(create_item("First Aid Kit", player))
        items.append(create_item("Primary Ammo", player))
        items.append(create_item("Primary Ammo", player))
        items.append(create_item("Primary Ammo", player))
        items.append(create_item("Primary Ammo", player))
        items.append(create_item("Secondary Ammo", player))
        items.append(create_item("Secondary Ammo", player))
        items.append(create_item("Secondary Ammo", player))
        items.append(create_item("Secondary Ammo", player))
    else:
        items.append(create_item("First Aid Kit", player))
        items.append(create_item("First Aid Kit", player))
        items.append(create_item("First Aid Kit", player))
        items.append(create_item("Primary Ammo", player))
        items.append(create_item("Primary Ammo", player))
        items.append(create_item("Primary Ammo", player))
        items.append(create_item("Secondary Ammo", player))
        items.append(create_item("Secondary Ammo", player))
        items.append(create_item("Dilophosaur Spit Trap", player))
        items.append(create_item("Dilophosaur Spit Trap", player))
        items.append(create_item("Dilophosaur Spit Trap", player))

    return items


def get_id_to_name_mapping() -> dict[int, str]:
    return {item.id + JP_ITEM_ID_BASE: name for name, item in
            item_table.items() if item.id is not None}


def get_name_to_id_mapping() -> dict[str, int]:
    return {name: item.id + JP_ITEM_ID_BASE for name, item in
            item_table.items() if item.id is not None}
