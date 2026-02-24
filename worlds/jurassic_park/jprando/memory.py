#
# This file contains constants and common memory values/addresses
#

# Flag values for collecting various items and
# checking various location types
#
# Many of the flags are a full 8 or 16 bits in the vanilla game,
# but are being split in half in the randomizer to accomodate
# both both checking the location and owning the item.
HAS_ID_CARD: int = 0x00FF
CHECKED_ID_CARD_LOC: int = 0xFF00

HAS_BATT: int = 0x0F
CHECKED_BATT_LOC: int = 0xF0

HAS_NERVE_GAS: int = 0x0001
DEPLOYED_NERVE_GAS: int = 0x0002
CHECKED_NERVE_GAS_LOC: int = 0xFF00

# Custom AP memory addresses for handling item delivery
ITEM_RCV_ADDR: int = 0x7E0100
ITEM_CNT_ADDR: int = 0x7E0101
IN_GAME_BYTE: int = 0x7E0102

# ROM locations for storing AP player validation data
VALIDATION_ADDR = 0x20_0000
VALIDATION_SIZE = 0x20

# Some arbitrary value to denote that we're in game
IN_GAME_VAL: int = 0xDB

# Egg memory starts out as 0x000A until collected
EGG_COLLECTED_VAL = 0x0000

# ID Table start
ID_TABLE_BASE: int = 0x7E0253
ID_CARD_HAMMOND: int = 0x7E0253
ID_CARD_SATTLER: int = 0x7E0255
ID_CARD_MULDOON: int = 0x7E0257
ID_CARD_GRANT: int = 0x7E0259
ID_CARD_GENNARO: int = 0x7E025B
ID_CARD_ARNOLD: int = 0x7E025D
ID_CARD_NEDRY: int = 0x7E025F
ID_CARD_WU: int = 0x7E0261
ID_CARD_MALCOLM: int = 0x7E0263
ID_TABLE_SIZE = 18  # 9 entries, 2 bytes each

# Start of event/objective flags
SECURITY_LEVEL1: int = 0x7E0265
SECURITY_LEVEL2: int = 0x7E0267
CURRENT_BUILDING_BATTERY: int = 0x7E0269
GENERATOR_TURNED_ON: int = 0x7E026B
MAIN_SYSTEM_REBOOTED: int = 0x7E026D
RAPTOR_DOOR_BLOCKED: int = 0x7E026F
CLEARED_SHIP: int = 0x7E0271
DESTROYED_RAPTOR_NEST: int = 0x7E0273
CONTACTED_MAINLAND: int = 0x7E0275
MOTION_SENSORS_ACTIVATED: int = 0x7E0287
ALL_EGGS_COLLECTED: int = 0x7E0289

PRIMARY_WEAPON_AMMO: int = 0x7E028B
SECONDARY_WEAPON_AMMO: int = 0x7E0295
CATTLE_PROD_CHARGE_ADDR: int = 0x7E029F
DAMAGE_TAKEN_ADDR: int = 0x7E02EB

# 0xFFFF at victory addr instantly triggers escape cutscene
VICTORY_ADDR: int = 0x7E038B
SPIT_TRAP_ADDR: int = 0x7E03BE
EGG_CNT_ADDR: int = 0x7E0E0F
MAP_INDICATOR: int = 0x7E16B5

# Battery table
BATT_TABLE_START: int = 0x7E1DE4
NORTH_UTILITY_SHED_BATT: int = 0x7E1DE4
RAPTOR_PEN_BATT: int = 0x7E1DE5
VISITOR_CENTER_BATT: int = 0x7E1DE6
BEACH_UTILITY_SHED_BATT: int = 0x7E1DE7
NUBLAR_UTILITY_SHED_BATT: int = 0x7E1DE8
SHIP_BATT: int = 0x7E1DE9
BATT_TABLE_SIZE = 6

NERVE_GAS_FLAG_ADDR: int = 0x7E1DEF
CONTACTED_SHIP: int = 0x7E1DF5

# Egg table
EGG_TABLE_START: int = 0x7E31AC
EGG_TABLE_SIZE: int = 36  # 18 eggs, 2 bytes per entry
