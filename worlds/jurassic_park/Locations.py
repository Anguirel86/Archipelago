from dataclasses import dataclass
import typing
from typing import Callable


from BaseClasses import (
    CollectionState, ItemClassification as IC, Location, MultiWorld, Region
)

from .Items import JPItem


"""
Regions:
  Starting overworld region:
    - Northwest Triceratops Egg
    - North Mountain Egg
    - Jungle Triceratops Egg
    - Jungle Traps Egg
    - Jungle Dead End Egg
    - Nublar Utility Shed Mountain Egg
    - Nublar Utility Shed South Egg
    - Park Gate Egg
    - East Canal Egg
    - East Mountain Egg
    - East Harbor Egg
    - Ship Roof Egg (Confirm this)
    - Helipad Egg

  Overworld Gate 1 (north utility shed area)
    - Egg Behind Visitor Center
    - Egg Behind North Utility Shed

  Visitor Center
    - Battery
    - Reboot park systems (Nedry ID Card)
    - Activate motion sensors (Reboot system)
    - Request security level 1 (Reboot system and Dr. Wu card)
    - Alan Grant ID Card (Night vision)
  Visitor Center Roof
    - John Hammond ID Card
    - Visitor Center Roof Egg
  Nublar Utility Shed
    - Turn on Generator
    - Battery
    - Donald Genarro ID Card
  Beach Utility Shed
    - Dennis Nedry ID Card
    - Battery (Gennaro ID card)
    - Ray Arnold ID Card (Gennaro ID card)
  North Utility Shed
    - Battery
    - Nerve Gas
  Raptor Pen
    - Battery
    - Robert Muldoon ID Card
    - Ian Malcolm ID Card
    - Call Ship
    - Block Door (Back door - Hammond and Sattler ID cards)
  Raptor Nest OW (Behind Gate 2)
    - Raptor Nest North Egg
    - Raptor Nest South Egg
  Raptor Nest Inside
    - Place Nerve Gas
  Ship
    - Battery (Always available)
    - Dr. Wu ID Card (Night vision)
    - Ellie Sattler ID Card (Ray Arnold's ID Card)
    - Security Level 2
    - Clear Ship Objective
"""

JP_LOC_ID_BASE = 64_000_000


@dataclass
class LocationData:
    id: int
    access_tokens: typing.Optional[list[list[str]]]
    parent_region_name: str
    is_event: bool = False


@dataclass
class ConnectorData():
    from_region_name: str
    to_region_name: str
    access_tokens: typing.Optional[list[list[str]]]
    reversible: bool


class JPLocation(Location):
    game = "Jurassic Park"


# List of region names
#  - Overworld Start
#  - Nublar Utility Shed
#  - Beach Utility Shed
#  - Visitor Center
#  - Raptor Pen
#  - Ship
#  - Raptor Nest
#  - North Utility Shed
# Build up a table of entrance/exits between regions
connector_table: dict[str, ConnectorData] = {
    "Nublar Utility Shed": ConnectorData(
        "Overworld Start",
        "Nublar Utility Shed",
        None,
        True),

    "Beach Utility Shed": ConnectorData(
        "Overworld Start",
        "Beach Utility Shed",
        None,
        True),

    "Visitor Center": ConnectorData(
        "Overworld Start",
        "Visitor Center",
        None,
        True),

    "Raptor Pen": ConnectorData(
        "Overworld Start",
        "Raptor Pen",
        None,
        True),

    "Ship": ConnectorData(
        "Overworld Start",
        "Ship",
        None,
        True),

    # These last two need the park systems to be rebooted
    # in order to open the gates
    "Raptor Nest": ConnectorData(
        "Overworld Start",
        "Raptor Nest",
        [["Reboot Park Systems"]],
        True),

    "North Utility Shed": ConnectorData(
        "Overworld Start",
        "North Utility Shed",
        [["Reboot Park Systems"]],
        True)

    # NOTE: There is another connector between the visitor center and
    #       the raptor pen, but logically I think that's being handled
    #       by the access rules on the "Block Raptor Pen Door" location.
}

# Build up a table of all locations and their regions and access rules
location_table: dict[str, LocationData] = {
    #################
    # Egg locations #
    #################
    # Open egg locations
    "Northwest Triceratops Egg": LocationData(0x01, None, "Overworld Start"),
    "North Mountain Egg": LocationData(0x02, None, "Overworld Start"),
    "Jungle Triceratops Egg": LocationData(0x03, None, "Overworld Start"),
    "Jungle Traps Egg": LocationData(0x04, None, "Overworld Start"),
    "Jungle Dead End Egg": LocationData(0x05, None, "Overworld Start"),
    "Nublar Utility Shed Mountain Egg": LocationData(0x06, None, "Overworld Start"),
    "Nublar Utility Shed South Egg": LocationData(0x07, None, "Overworld Start"),
    "Park Gate Egg": LocationData(0x08, None, "Overworld Start"),
    "East Canal Egg": LocationData(0x09, None, "Overworld Start"),
    "East Mountain Egg": LocationData(0x0A, None, "Overworld Start"),
    "East Harbor Egg": LocationData(0x0B, None, "Overworld Start"),
    "Ship Roof Egg": LocationData(0x0C, None, "Overworld Start"),
    "Helipad Egg": LocationData(0x0D, None, "Overworld Start"),
    "Visitor Center Roof Egg": LocationData(0x0E, None, "Visitor Center"),

    # North utility shed egg locations
    "Behind Visitor Center Egg": LocationData(
        0x0F,
        [["Reboot Park Systems"]],
        "North Utility Shed"),

    "North Utility Shed Egg": LocationData(
        0x10,
        [["Reboot Park Systems"]],
        "North Utility Shed"),

    # Raptor nest egg locations
    "North Raptor Nest Egg": LocationData(
        0x11,
        [["Reboot Park Systems"]],
        "Raptor Nest"),

    "South Raptor Nest Egg": LocationData(
        0x12,
        [["Reboot Park Systems"]],
        "Raptor Nest"),

    #####################
    # ID Card locations #
    #####################
    "John Hammond ID Card": LocationData(0x20, None, "Visitor Center"),
    "Ellie Sattler ID Card": LocationData(
        0x21,
        [["Ship Battery", "Ray Arnold ID Card", "Security Level 2"]],
        "Ship"),
    "Robert Muldoon ID Card": LocationData(0x22, ["Raptor Pen Battery"], "Raptor Pen"),
    "Alan Grant ID Card": LocationData(
        0x23,
        [["Visitor Center Battery", "John Hammond ID Card"]],
        "Visitor Center"),
    "Donald Gennaro ID Card": LocationData(
        0x24,
        [["Ian Malcolm ID Card"]],  # TODO: Additional rules?
        "Nublar Utility Shed"),
    "Ray Arnold ID Card": LocationData(
        0x25,
        [["Beach Utility Shed Battry", "Donald Gennaro ID Card"]],
        "Beach Utility Shed"),
    "Dennis Nedry ID Card": LocationData(
        0x26,
        None,
        "Beach Utility Shed"),
    "Doctor Wu ID Card": LocationData(
        0x27,
        [["Ship Battery"]],
        "Ship"),
    "Ian Malcolm ID Card": LocationData(
        0x28,
        [["Raptor Pen Battery"]],
        "Raptor Pen"),

    #############
    # Batteries #
    #############
    "North Utility Shed Battery": LocationData(
        0x40,
        [["Reboot Park Systems"]],
        "North Utility Shed"),
    "Raptor Pen Battery": LocationData(
        0x41,
        None,
        "Raptor Pen"),
    "Visitor Center Battery": LocationData(
        0x42,
        [["John Hammond ID Card"]],
        "Visitor Center"),
    "Beach Utility Shed Battery": LocationData(
        0x43,
        [["Donald Gennaro ID Card"]],
        "Beach Utility Shed"),
    "Nublar Utility Shed Battery": LocationData(
        0x44,
        None,
        "Nublar Utility Shed"),
    "Ship Battery": LocationData(
        0x45,
        None,
        "Ship"),

    ###################
    # Event Locations #
    ###################
    "Turn on Generator": LocationData(
        0x60,
        None,
        "Nublar Utility Shed",
        True),
    "Reboot Park Systems": LocationData(
        0x61,
        [["Turn on Generator", "Dennis Nedry ID Card"]],
        "Visitor Center",
        True),
    "Activate Motion Sensors": LocationData(
        0x62,
        [["Reboot Park Systems"]],
        "Visitor Center",
        True),
    "Block Raptor Pen Door": LocationData(
        0x63,
        [["John Hammond ID Card", "Ellie Sattler ID Card"],
            ["Alan Grant ID Card", "Raptor Pen Battery"]],
        "Raptor Pen",
        True),
    "Security Level 1": LocationData(
        0x64,
        [["Reboot Park Systems", "Doctor Wu ID Card"]],
        "Visitor Center",
        True),
    "Security Level 2": LocationData(
        0x65,
        [["Security Level 1"]],
        "Ship",
        True),
    "Contact Ship": LocationData(
        0x66,
        [["Security Level 1", "Block Raptor Pen Door"]],
        "Raptor Pen",
        True),
    "Clear Ship": LocationData(
        0x67,
        [["Ship Battery", "Security Level 2",
            "Ray Arnold ID Card", "Block Raptor Pen Door"]],
        "Ship",
        True),
    "Collect Nerve Gas": LocationData(
        0x68,
        [["Reboot Park Systems", "Robert Muldoon ID Card"]],
        "North Utility Shed",
        True),
    "Destroy Raptor Nest": LocationData(
        0x69,
        [["Reboot Park Systems", "Collect Nerve Gas", "Clear Ship"]],
        "Raptor Nest",
        True),
    "Contact Mainland": LocationData(
        0x6A,
        [["Destroy Raptor Nest", "Ship Battery"]],
        "Ship",
        True)
}


def create_regions(player: int, multiworld: MultiWorld, eggs_required: int):
    """
    Create the regions, locations, and entrances for this player
    """
    regions: dict[str, Region] = {}
    for name, loc_data in location_table.items():
        region_name = loc_data.parent_region_name
        # Create the region if needed
        if region_name not in regions:
            region = Region(region_name, player, multiworld)
            regions[region_name] = region
        else:
            region = regions[region_name]

        # Add location to its parent region
        loc = create_location(player, name, loc_data.id,
                              loc_data.access_tokens, region)
        region.locations.append(loc)

        if (loc_data.is_event):
            # Create an additional event location for a locked event item
            create_event_location(player, name, loc_data.access_tokens, region)

    # Create the entrance/exit pairs for the regions
    for name, conn_data in connector_table.items():
        to_region = regions[conn_data.to_region_name]
        from_region = regions[conn_data.from_region_name]

        # There's only one entrance to each region currently,
        # so no need for complex naming.  Just use the "to region"
        exit_obj = from_region.create_exit(name)
        exit_obj.access_rule = create_access_rule(
            player, conn_data.access_tokens)
        exit_obj.connect(to_region)

        # If the connector is reversible, add its opposite
        if conn_data.reversible:
            reverse_name = f"{
                conn_data.to_region_name}-{conn_data.from_region_name}"
            reverse_exit = to_region.create_exit(reverse_name)
            reverse_exit.access_rule = create_access_rule(
                player, conn_data.access_tokens)
            reverse_exit.connect(from_region)

    # Set the victory condition for this game
    create_victory_location(player, regions["Overworld Start"], eggs_required)

    return regions.values()


def create_location(
        player: int,
        name: str,
        loc_id: int,
        rules: typing.Optional[list[list[str]]],
        region: Region) -> JPLocation:
    """
    Create a JPLocation object with the given parameters.
    """
    access_rule = create_access_rule(player, rules)
    loc = JPLocation(player, name, loc_id + JP_LOC_ID_BASE, region)
    loc.access_rule = access_rule
    return loc


def create_event_location(
        player: int,
        name: str,
        rules: typing.Optional[list[list[str]]],
        region: Region) -> JPLocation:
    access_rule = create_access_rule(player, rules)
    region.add_event(f"{name}_evt", name, access_rule, show_in_spoiler=False)


def create_victory_location(
        player: int,
        region: Region,
        eggs_required: int):

    def victory_rule(state: CollectionState) -> bool:
        # In order to escape, the player must contact the mainland
        # and collect all of the eggs.  Egg count is adjustable
        # via an option.
        called_helicopter = state.has("Contact Mainland", player)
        all_eggs = state.has("Egg", player, eggs_required)
        return called_helicopter and all_eggs

    item = JPItem("Escape the Island", IC.progression, None, player)

    loc = JPLocation(player, "Escape the Island", None, region)
    loc.event = True
    loc.access_rule = victory_rule
    loc.place_locked_item(item)
    region.locations.append(loc)


def create_access_rule(
        player: int,
        rules: typing.Optional[list[list[str]]]
) -> Callable[[CollectionState], bool]:

    if rules is None:
        return lambda state: True

    def can_access(state: CollectionState) -> bool:
        for rule in rules:
            has_access = True
            for item in rule:
                if not state.has(item, player):
                    has_access = False
                    break

            if has_access:
                # One of the access rules was satisfied
                return True

        # No access rules were satisfied
        return False

    return can_access


def get_id_to_name_mapping() -> dict[int, str]:
    return {loc.id + JP_LOC_ID_BASE: name
            for name, loc in location_table.items()}


def get_name_to_id_mapping() -> dict[str, int]:
    return {name: loc.id + JP_LOC_ID_BASE
            for name, loc in location_table.items()}
