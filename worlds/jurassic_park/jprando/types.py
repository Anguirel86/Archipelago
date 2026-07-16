from enum import IntEnum


class MapId(IntEnum):
    """Jurassic Park Map IDs."""

    OVERWORLD = 0x00
    NORTH_UTILITY_SHED_ENTRY_LEVEL = 0x01
    RAPTOR_PEN_ENTRY_LEVEL = 0x02
    VISITOR_CENTER_ROOF_LEVEL = 0x03
    VISITOR_CENTER_ENTRY_LEVEL = 0x04
    BEACH_UTILITY_SHED_ENTRY_LEVEL = 0x05
    NUBLAR_UTILITY_SHED_ENTRY_LEVEL = 0x06
    SHIP_ENTRY_LEVEL = 0x07
    RAPTOR_NEST_NORTH_ENTRANCE = 0x08
    RAPTOR_NEST_SOUTH_ENTRANCE = 0x09
    SECRET_LEVEL = 0x0A
    RAPTOR_PEN_GROUND_FLOOR = 0x0B
    RAPTOR_PEN_SUB_LEVEL_1 = 0x0C
    RAPTOR_PEN_SUB_LEVEL_2 = 0x0D
    RAPTOR_PEN_UPPER_LEVEL = 0x0E
    VISITOR_CENTER_FLOOR_2 = 0x0F
    VISITOR_CENTER_SUB_LEVEL = 0x10
    NUBLAR_UTILITY_SHED_SUB_LEVEL = 0x11
    BEACH_UTILITY_SHED_SUB_LEVEL = 0x12
    NORTH_UTILITY_SHED_SUB_LEVEL = 0x13
    SHIP_SUB_LEVEL_1 = 0x14
    SHIP_SUB_LEVEL_2 = 0x15
    SHIP_SUB_LEVEL_3 = 0x16
    SHIP_SUB_LEVEL_4 = 0x17


class Regions(IntEnum):
    """
    Jurassic Park Regions.
    These are the distinct logical regions within the game.
    """

    OVERWORLD_START = 0
    OVERWORLD_NORTH_UTILITY_SHED = 1
    OVERWORLD_RAPTOR_NEST = 2
    OVERWORLD_VISITOR_CENTER_ROOF = 3
    NUBLAR_UTILITY_SHED = 4
    BEACH_UTILITY_SHED = 5
    NORTH_UTILITY_SHED = 6
    VISITOR_CENTER = 7
    RAPTOR_PEN = 8
    RAPTOR_NEST = 9
    SHIP = 10
    SECRET_AREA = 11


REGION_NAMES: dict[Regions, str] = {
    Regions.OVERWORLD_START: "Overworld Start",
    Regions.OVERWORLD_NORTH_UTILITY_SHED: "Overworld North Utility Shed",
    Regions.OVERWORLD_RAPTOR_NEST: "Overworld Raptor Nest",
    Regions.OVERWORLD_VISITOR_CENTER_ROOF: "Overworld Visitor Center Roof",
    Regions.NUBLAR_UTILITY_SHED: "Nublar Utility Shed",
    Regions.BEACH_UTILITY_SHED: "Beach Utility Shed",
    Regions.NORTH_UTILITY_SHED: "North Utility Shed",
    Regions.VISITOR_CENTER: "Visitor Center",
    Regions.RAPTOR_PEN: "Raptor Pen",
    Regions.RAPTOR_NEST: "Raptor Nest",
    Regions.SHIP: "Ship",
    Regions.SECRET_AREA: "Secret Area",
}

# Entrance table addresses for main entrances from each location
MAP_ID_TO_ENTRANCE_TABLE: dict[MapId, int] = {
    MapId.NORTH_UTILITY_SHED_ENTRY_LEVEL: 0x8909,
    MapId.RAPTOR_PEN_ENTRY_LEVEL: 0x890D,
    MapId.VISITOR_CENTER_ENTRY_LEVEL: 0x8915,
    MapId.BEACH_UTILITY_SHED_ENTRY_LEVEL: 0x8919,
    MapId.NUBLAR_UTILITY_SHED_ENTRY_LEVEL: 0x891D,
    MapId.SHIP_ENTRY_LEVEL: 0x8921,
    MapId.RAPTOR_NEST_NORTH_ENTRANCE: 0x8925,
    MapId.RAPTOR_NEST_SOUTH_ENTRANCE: 0x892D,
    MapId.SECRET_LEVEL: 0x8935,
    MapId.VISITOR_CENTER_ROOF_LEVEL: 0x8915,
}


# Mapping of MapIDs to their entries in the OW coordinate table
# These coords are accesed when leaving the map and spawning back on the overworld
# NOTE: There are alternate table entries for the raptor nest that don't appear
#       to be used.  The raptor nest map seems to load a different (duplicate) copy
#       based on which entrance you use but both seem to use the same OW coord slot.
MAP_ID_TO_OVERWORLD_COORDINATES: dict[MapId, int] = {
    MapId.NORTH_UTILITY_SHED_ENTRY_LEVEL: 0x8947,
    MapId.RAPTOR_PEN_ENTRY_LEVEL: 0x894F,
    MapId.VISITOR_CENTER_ROOF_LEVEL: 0x8957,
    MapId.VISITOR_CENTER_ENTRY_LEVEL: 0x895F,
    MapId.BEACH_UTILITY_SHED_ENTRY_LEVEL: 0x8967,
    MapId.NUBLAR_UTILITY_SHED_ENTRY_LEVEL: 0x896F,
    MapId.SHIP_ENTRY_LEVEL: 0x8977,
    MapId.RAPTOR_NEST_NORTH_ENTRANCE: 0x897F,
    # MapId.RAPTOR_NEST_NORTH_ENTRANCE: 0x8987 # Alternate data
    MapId.RAPTOR_NEST_SOUTH_ENTRANCE: 0x898F,
    # MapId.RAPTOR_NEST_SOUTH_ENTRANCE: 0x8997 # Alternate data
    MapId.SECRET_LEVEL: 0x899F,
}
