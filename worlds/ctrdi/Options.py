
from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, FreeText, OptionGroup, \
    PerGameCommonOptions, Range, Toggle


class XpScale(Range):
    """Factor by which to scale XP earned in battle"""
    display_name = "Xp Scale"
    range_start = 1
    range_end = 10
    default = 4


class TpScale(Range):
    """Factor by which to scale TP earned in battle"""
    display_name = "Tp Scale"
    range_start = 1
    range_end = 10
    default = 4


class SplitTp(Toggle):
    """TP is split among living party members rather than shared evenly"""
    display_name = "Split Tp"


class FixTpDoubling(Toggle):
    """TP rewards are not duplicated for every gained tech level"""
    display_name = "Fix Tp Doubling"


class XpPenaltyLevel(Range):
    """Levels past this level become more difficult to obtain"""
    display_name = "Xp Penalty Level"
    range_start = 1
    range_end = 99
    default = 40


class XpPenaltyPercent(Range):
    """For each level beyond the penalty, the requirement grows by this percent"""
    display_name = "Xp Penalty Percent"
    range_start = 0
    range_end = 100
    default = 15


class LevelCap(Range):
    """Levels beyond the level cap will have prohibitively large requirements."""
    display_name = "Level Cap"
    range_start = 1
    range_end = 99
    default = 50


class BossXpFactor(Range):
    """Boss xp is additionally multiplied by this factor"""
    display_name = "Boss Xp Factor"
    range_start = 0
    range_end = 5
    default = 2


class MidbossRewardFactor(Range):
    """Midboss xp/tp is additionally multiplied by this factor"""
    display_name = "Midboss Reward Factor"
    range_start = 0
    range_end = 5
    default = 2


class NormalizeBossXp(Toggle):
    """Boss xp is proportional to their level"""
    display_name = "Normalize Boss Xp"


class DropEnemyPool(Choice):
    """Pool of enemies which can have a dropped item"""
    display_name = "Drop Enemy Pool"

    option_vanilla = 0
    option_all = 1
    default = 0


class DropRewardPool(Choice):
    """Method of choosing enemy dropped items"""
    display_name = "Drop Reward Pool"

    option_vanilla = 0
    option_shuffle = 1
    option_rdi_random = 2
    default = 0


class DropRate(Range):
    """Percentage (decimal) of enemies in the drop pool which have a dropped item"""
    display_name = "Drop Rate"
    range_start = 0
    range_end = 1
    default = 1


class MarkDroppingEnemies(Toggle):
    """Alter enemy names to indicate a dropped item"""
    display_name = "Mark Dropping Enemies"


class CharmEnemyPool(Choice):
    """Pool of enemies which can have a charmable item"""
    display_name = "Charm Enemy Pool"

    option_vanilla = 0
    option_all = 1
    default = 0


class CharmRewardPool(Choice):
    """Method of choosing enemy charmable items"""
    display_name = "Charm Reward Pool"

    option_vanilla = 0
    option_shuffle = 1
    option_rdi_random = 2
    default = 0


class CharmRate(Range):
    """Percentage (decimal) of enemies in the charm pool which have a charmable item"""
    display_name = "Charm Rate"
    range_start = 0
    range_end = 1
    default = 1


class MarkCharmableEnemies(Toggle):
    """Alter enemy names to indicate a charmable item"""
    display_name = "Mark Charmable Enemies"


class TechOrder(Choice):
    """Order in which techs are learned"""
    display_name = "Tech Order"

    option_vanilla = 0
    option_rdi_random = 1
    option_mp = 2
    option_mp_type = 3
    default = 0


class TechDamage(Choice):
    """Damage dealt by techs"""
    display_name = "Tech Damage"

    option_vanilla = 0
    option_shuffle = 1
    option_rdi_random = 2
    default = 0


class TechDamageRandomFactorMin(Range):
    """Minimum percent (as decimal, default 1.0) which MP costs may shift (ignored if vanilla damage)"""
    display_name = "Tech Damage Random Factor Min"
    range_start = 1
    range_end = 2
    default = 1


class TechDamageRandomFactorMax(Range):
    """Maximum percent (as decimal, default 1.0) which MP costs may shift (ignored if vanilla damage)"""
    display_name = "Tech Damage Random Factor Max"
    range_start = 1
    range_end = 2
    default = 1


class PreserveMagic(Toggle):
    """Keep each PC's first magic tech in its vanilla location (may break specified order)"""
    display_name = "Preserve Magic"


class BlackHoleFactor(Range):
    """Percent kill chance per MP in black hole's cost"""
    display_name = "Black Hole Factor"
    range_start = 0
    range_end = 10
    default = 2


class BlackHoleMin(Range):
    """Base percent kill chance for black hole, total is base + mp*factor"""
    display_name = "Black Hole Min"
    range_start = 0
    range_end = 100
    default = 10


class ShowFullTechList(Toggle):
    """The tech page of the menu will show all single techs"""
    display_name = "Show Full Tech List"


class BalanceTechMps(Toggle):
    """Ensure every character has at least one strong tech."""
    display_name = "Balance Tech Mps"


class DynamicScalingScheme(Choice):
    """Method for dynamically scaling enemies"""
    display_name = "Dynamic Scaling Scheme"

    option_none = 0
    option_progression = 1
    option_logic_depth = 2
    default = 1


class LevelsPerBoss(Range):
    """Scaling levels gained per boss defeated"""
    display_name = "Levels Per Boss"
    range_start = 0
    range_end = 10
    default = 2


class LevelsPerQuest(Range):
    """Scaling levels gained per quest completed"""
    display_name = "Levels Per Quest"
    range_start = 0
    range_end = 10
    default = 2


class LevelsPerKeyItem(Range):
    """Scaling levels gained per key item obtained"""
    display_name = "Levels Per Key Item"
    range_start = 0
    range_end = 10
    default = 0


class LevelsPerObjective(Range):
    """Scaling levels gained per objective completed"""
    display_name = "Levels Per Objective"
    range_start = 0
    range_end = 10
    default = 2


class LevelsPerCharacter(Range):
    """Scaling levels gained per character recruited"""
    display_name = "Levels Per Character"
    range_start = 0
    range_end = 10
    default = 2


class MaxScalingLevel(Range):
    """Maximum level to scale to (if not none)"""
    display_name = "Max Scaling Level"
    range_start = 1
    range_end = 99
    default = 50


class DynamicScaleLavos(Toggle):
    """Include Lavos in the dynamic scaling (if not none)"""
    display_name = "Dynamic Scale Lavos"


class DynamicScaleLavosGauntlet(Toggle):
    """Include Lavos attack modes in the dynamic scaling (if not none)"""
    display_name = "Dynamic Scale Lavos Gauntlet"


class DefenseSafetyMinLevel(Range):
    """Level before which enemies have standard phys defense"""
    display_name = "Defense Safety Min Level"
    range_start = 1
    range_end = 99
    default = 10


class DefenseSafetyMaxLevel(Range):
    """Level after which enemies have their normal phys defense"""
    display_name = "Defense Safety Max Level"
    range_start = 1
    range_end = 99
    default = 30


class ObstacleSafetyLevel(Range):
    """Level before which Obstacle is single target"""
    display_name = "Obstacle Safety Level"
    range_start = 1
    range_end = 99
    default = 30


class NormalEnemyHpScale(Range):
    """Multiply non-boss enemy hp by this factor"""
    display_name = "Normal Enemy Hp Scale"
    range_start = 1
    range_end = 2
    default = 1


class StaticBossHpScale(Range):
    """Multiply boss hp by this factor"""
    display_name = "Static Boss Hp Scale"
    range_start = 1
    range_end = 2
    default = 1


class StaticHpScaleLavos(Toggle):
    """Apply static hp scaling to lavos"""
    display_name = "Static Hp Scale Lavos"


class ElementSafetyLevel(Range):
    """Before this level any magic hits Nizbel/Retinite weakness"""
    display_name = "Element Safety Level"
    range_start = 1
    range_end = 99
    default = 30


class MillennialFairMod(Range):
    """Additional scaling levels for millennial_fair"""
    display_name = "Millennial Fair Mod"
    range_start = -50
    range_end = 50
    default = 0


class GuardiaForest1000Mod(Range):
    """Additional scaling levels for guardia_forest_1000"""
    display_name = "Guardia Forest 1000 Mod"
    range_start = -50
    range_end = 50
    default = 0


class GuardiaForest600Mod(Range):
    """Additional scaling levels for guardia_forest_600"""
    display_name = "Guardia Forest 600 Mod"
    range_start = -50
    range_end = 50
    default = 0


class CronoTrialMod(Range):
    """Additional scaling levels for crono_trial"""
    display_name = "Crono Trial Mod"
    range_start = -50
    range_end = 50
    default = 0


class HeckranCaveMod(Range):
    """Additional scaling levels for heckran_cave"""
    display_name = "Heckran Cave Mod"
    range_start = -50
    range_end = 50
    default = 0


class TruceCanyonMod(Range):
    """Additional scaling levels for truce_canyon"""
    display_name = "Truce Canyon Mod"
    range_start = -50
    range_end = 50
    default = 0


class ManoriaCathedralMod(Range):
    """Additional scaling levels for manoria_cathedral"""
    display_name = "Manoria Cathedral Mod"
    range_start = -50
    range_end = 50
    default = 0


class DenadoroMountainsMod(Range):
    """Additional scaling levels for denadoro_mountains"""
    display_name = "Denadoro Mountains Mod"
    range_start = -50
    range_end = 50
    default = 0


class CursedWoodsMod(Range):
    """Additional scaling levels for cursed_woods"""
    display_name = "Cursed Woods Mod"
    range_start = -50
    range_end = 50
    default = 0


class Lab16Mod(Range):
    """Additional scaling levels for lab_16"""
    display_name = "Lab 16 Mod"
    range_start = -50
    range_end = 50
    default = 0


class Lab32Mod(Range):
    """Additional scaling levels for lab_32"""
    display_name = "Lab 32 Mod"
    range_start = -50
    range_end = 50
    default = 0


class SewersMod(Range):
    """Additional scaling levels for sewers"""
    display_name = "Sewers Mod"
    range_start = -50
    range_end = 50
    default = 0


class DeathPeakMod(Range):
    """Additional scaling levels for death_peak"""
    display_name = "Death Peak Mod"
    range_start = -50
    range_end = 50
    default = 0


class ArrisDomeMod(Range):
    """Additional scaling levels for arris_dome"""
    display_name = "Arris Dome Mod"
    range_start = -50
    range_end = 50
    default = 0


class ProtoDomeMod(Range):
    """Additional scaling levels for proto_dome"""
    display_name = "Proto Dome Mod"
    range_start = -50
    range_end = 50
    default = 0


class FactoryRuinsMod(Range):
    """Additional scaling levels for factory_ruins"""
    display_name = "Factory Ruins Mod"
    range_start = -50
    range_end = 50
    default = 0


class MysticMountainsMod(Range):
    """Additional scaling levels for mystic_mountains"""
    display_name = "Mystic Mountains Mod"
    range_start = -50
    range_end = 50
    default = 0


class HuntingRangeMod(Range):
    """Additional scaling levels for hunting_range"""
    display_name = "Hunting Range Mod"
    range_start = -50
    range_end = 50
    default = 0


class DactylNestMod(Range):
    """Additional scaling levels for dactyl_nest"""
    display_name = "Dactyl Nest Mod"
    range_start = -50
    range_end = 50
    default = 0


class ShellTrialMod(Range):
    """Additional scaling levels for shell_trial"""
    display_name = "Shell Trial Mod"
    range_start = -50
    range_end = 50
    default = 0


class ZenanBridgeMod(Range):
    """Additional scaling levels for zenan_bridge"""
    display_name = "Zenan Bridge Mod"
    range_start = -50
    range_end = 50
    default = 0


class NorthernRuinsMod(Range):
    """Additional scaling levels for northern_ruins"""
    display_name = "Northern Ruins Mod"
    range_start = -50
    range_end = 50
    default = 0


class GiantsClawMod(Range):
    """Additional scaling levels for giants_claw"""
    display_name = "Giants Claw Mod"
    range_start = -50
    range_end = 50
    default = 0


class OzziesFortMod(Range):
    """Additional scaling levels for ozzies_fort"""
    display_name = "Ozzies Fort Mod"
    range_start = -50
    range_end = 50
    default = 0


class MagusCastleMod(Range):
    """Additional scaling levels for magus_castle"""
    display_name = "Magus Castle Mod"
    range_start = -50
    range_end = 50
    default = 0


class MagicCaveMod(Range):
    """Additional scaling levels for magic_cave"""
    display_name = "Magic Cave Mod"
    range_start = -50
    range_end = 50
    default = 0


class SunkenDesertMod(Range):
    """Additional scaling levels for sunken_desert"""
    display_name = "Sunken Desert Mod"
    range_start = -50
    range_end = 50
    default = 0


class SunPalaceMod(Range):
    """Additional scaling levels for sun_palace"""
    display_name = "Sun Palace Mod"
    range_start = -50
    range_end = 50
    default = 0


class GenoDomeMod(Range):
    """Additional scaling levels for geno_dome"""
    display_name = "Geno Dome Mod"
    range_start = -50
    range_end = 50
    default = 0


class ForestMazeMod(Range):
    """Additional scaling levels for forest_maze"""
    display_name = "Forest Maze Mod"
    range_start = -50
    range_end = 50
    default = 0


class ReptiteLairMod(Range):
    """Additional scaling levels for reptite_lair"""
    display_name = "Reptite Lair Mod"
    range_start = -50
    range_end = 50
    default = 0


class TyranoLairMod(Range):
    """Additional scaling levels for tyrano_lair"""
    display_name = "Tyrano Lair Mod"
    range_start = -50
    range_end = 50
    default = 0


class BlackOmenMod(Range):
    """Additional scaling levels for black_omen"""
    display_name = "Black Omen Mod"
    range_start = -50
    range_end = 50
    default = 0


class NorthCapeMod(Range):
    """Additional scaling levels for north_cape"""
    display_name = "North Cape Mod"
    range_start = -50
    range_end = 50
    default = 0


class EpochBattleMod(Range):
    """Additional scaling levels for epoch_battle"""
    display_name = "Epoch Battle Mod"
    range_start = -50
    range_end = 50
    default = 0


class BlackbirdMod(Range):
    """Additional scaling levels for blackbird"""
    display_name = "Blackbird Mod"
    range_start = -50
    range_end = 50
    default = 0


class EnhasaMod(Range):
    """Additional scaling levels for enhasa"""
    display_name = "Enhasa Mod"
    range_start = -50
    range_end = 50
    default = 0


class OceanPalaceMod(Range):
    """Additional scaling levels for ocean_palace"""
    display_name = "Ocean Palace Mod"
    range_start = -50
    range_end = 50
    default = 0


class MtWoeMod(Range):
    """Additional scaling levels for mt_woe"""
    display_name = "Mt Woe Mod"
    range_start = -50
    range_end = 50
    default = 0


class IncentiveFactor(Range):
    """Factor by which to increase the weight of incentive spots"""
    display_name = "Incentive Factor"
    range_start = 1
    range_end = 10
    default = 5


class HardLavosEndBoss(Toggle):
    """The game will end if Ocean Palace Lavos is defeated"""
    display_name = "Hard Lavos End Boss"


class BoatsOfTime(Toggle):
    """Additional ferry locations."""
    display_name = "Boats Of Time"


class JetsOfTime(Toggle):
    """Add JetsOfTime item and turn-in on Blackbird scaffolding"""
    display_name = "Jets Of Time"


class BossRandomizationType(Choice):
    """How bosses should be assigned to spots"""
    display_name = "Boss Randomization Type"

    option_vanilla = 0
    option_shuffle = 1
    option_rdi_random = 2
    default = 0


class MidbossRandomizationType(Choice):
    """How midbosses should be assigned to spots"""
    display_name = "Midboss Randomization Type"

    option_vanilla = 0
    option_shuffle = 1
    option_rdi_random = 2
    default = 0


class ShopInventoryRandomization(Choice):
    """How shop inventory should be randomized"""
    display_name = "Shop Inventory Randomization"

    option_vanilla = 0
    option_shuffle = 1
    option_full_random = 2
    option_tiered_random = 3
    default = 0


class ShopCapacityRandomization(Choice):
    """How shop capacity should be randomized"""
    display_name = "Shop Capacity Randomization"

    option_vanilla = 0
    option_shuffle = 1
    option_rdi_random = 2
    default = 0


class ItemBasePrices(Choice):
    """Unmodified price of items"""
    display_name = "Item Base Prices"

    option_vanilla = 0
    option_balanced = 1
    option_max = 2
    default = 0


class ItemPriceRandomization(Choice):
    """How item prices should be randomized"""
    display_name = "Item Price Randomization"

    option_vanilla = 0
    option_rdi_random = 1
    option_random_multiplier = 2
    default = 0


class ItemPriceMinMultiplier(Range):
    """minimum price multiplier that an item's price can roll"""
    display_name = "Item Price Min Multiplier"
    range_start = 1
    range_end = 10
    default = 1


class ItemPriceMaxMultiplier(Range):
    """maximum price multiplier that an item's price can roll"""
    display_name = "Item Price Max Multiplier"
    range_start = 1
    range_end = 10
    default = 2


class NumAlgettyPortalObjectives(Range):
    """Number of objectives needed to unlock the portal in Algetty's entrance"""
    display_name = "Num Algetty Portal Objectives"
    range_start = 0
    range_end = 8
    default = 3


class NumOmenObjectives(Range):
    """Number of objectives needed to unlock the final door in the Black Omen"""
    display_name = "Num Omen Objectives"
    range_start = 0
    range_end = 8
    default = 4


class NumBucketObjectives(Range):
    """Number of objectives needed to unlock the bucket in the End of Time"""
    display_name = "Num Bucket Objectives"
    range_start = 0
    range_end = 8
    default = 5


class NumGauntletObjectives(Range):
    """Number of objectives needed to remove the lavos boss gauntlet"""
    display_name = "Num Gauntlet Objectives"
    range_start = 0
    range_end = 8
    default = 5


class NumTimegaugeObjectives(Range):
    """Number of objectives needed to unlock the bucket in the End of Time"""
    display_name = "Num Timegauge Objectives"
    range_start = 0
    range_end = 8
    default = 6


class Objective1(FreeText):
    """Specifier for objective 1"""
    display_name = "Objective 1"
    default = ""


class Objective2(FreeText):
    """Specifier for objective 2"""
    display_name = "Objective 2"
    default = ""


class Objective3(FreeText):
    """Specifier for objective 3"""
    display_name = "Objective 3"
    default = ""


class Objective4(FreeText):
    """Specifier for objective 4"""
    display_name = "Objective 4"
    default = ""


class Objective5(FreeText):
    """Specifier for objective 5"""
    display_name = "Objective 5"
    default = ""


class Objective6(FreeText):
    """Specifier for objective 6"""
    display_name = "Objective 6"
    default = ""


class Objective7(FreeText):
    """Specifier for objective 7"""
    display_name = "Objective 7"
    default = ""


class Objective8(FreeText):
    """Specifier for objective 8"""
    display_name = "Objective 8"
    default = ""


class ShuffleEntrances(Toggle):
    """Whether to shuffle entrances or not"""
    display_name = "Shuffle Entrances"


class RestVanilla(Toggle):
    """Only shuffle locations in preserve_spots"""
    display_name = "Rest Vanilla"


class StarterMinLevel(Range):
    """Minimum level at which the starter recruit can join (default: 1)"""
    display_name = "Starter Min Level"
    range_start = 1
    range_end = 99
    default = 1


class StarterMinTechlevel(Range):
    """Minimum techlevel at which the starter recruit can join (default: 0)"""
    display_name = "Starter Min Techlevel"
    range_start = 0
    range_end = 8
    default = 0


class FairMinLevel(Range):
    """Minimum level at which the fair recruit can join (default: 1)"""
    display_name = "Fair Min Level"
    range_start = 1
    range_end = 99
    default = 1


class FairMinTechlevel(Range):
    """Minimum techlevel at which the fair recruit can join (default: 0)"""
    display_name = "Fair Min Techlevel"
    range_start = 0
    range_end = 8
    default = 0


class CathedralMinLevel(Range):
    """Minimum level at which the cathedral recruit can join (default: 5)"""
    display_name = "Cathedral Min Level"
    range_start = 1
    range_end = 99
    default = 5


class CathedralMinTechlevel(Range):
    """Minimum techlevel at which the cathedral recruit can join (default: 0)"""
    display_name = "Cathedral Min Techlevel"
    range_start = 0
    range_end = 8
    default = 0


class CastleMinLevel(Range):
    """Minimum level at which the castle recruit can join (default: 5)"""
    display_name = "Castle Min Level"
    range_start = 1
    range_end = 99
    default = 5


class CastleMinTechlevel(Range):
    """Minimum techlevel at which the castle recruit can join (default: 1)"""
    display_name = "Castle Min Techlevel"
    range_start = 0
    range_end = 8
    default = 1


class TrialMinLevel(Range):
    """Minimum level at which the trial recruit can join (default: 7)"""
    display_name = "Trial Min Level"
    range_start = 1
    range_end = 99
    default = 7


class TrialMinTechlevel(Range):
    """Minimum techlevel at which the trial recruit can join (default: 1)"""
    display_name = "Trial Min Techlevel"
    range_start = 0
    range_end = 8
    default = 1


class ProtoMinLevel(Range):
    """Minimum level at which the proto recruit can join (default: 10)"""
    display_name = "Proto Min Level"
    range_start = 1
    range_end = 99
    default = 10


class ProtoMinTechlevel(Range):
    """Minimum techlevel at which the proto recruit can join (default: 2)"""
    display_name = "Proto Min Techlevel"
    range_start = 0
    range_end = 8
    default = 2


class NorthCapeMinLevel(Range):
    """Minimum level at which the north_cape recruit can join (default: 37)"""
    display_name = "North Cape Min Level"
    range_start = 1
    range_end = 99
    default = 37


class NorthCapeMinTechlevel(Range):
    """Minimum techlevel at which the north_cape recruit can join (default: 3)"""
    display_name = "North Cape Min Techlevel"
    range_start = 0
    range_end = 8
    default = 3


class BurrowMinLevel(Range):
    """Minimum level at which the burrow recruit can join (default: 18)"""
    display_name = "Burrow Min Level"
    range_start = 1
    range_end = 99
    default = 18


class BurrowMinTechlevel(Range):
    """Minimum techlevel at which the burrow recruit can join (default: 2)"""
    display_name = "Burrow Min Techlevel"
    range_start = 0
    range_end = 8
    default = 2


class DactylMinLevel(Range):
    """Minimum level at which the dactyl recruit can join (default: 20)"""
    display_name = "Dactyl Min Level"
    range_start = 1
    range_end = 99
    default = 20


class DactylMinTechlevel(Range):
    """Minimum techlevel at which the dactyl recruit can join (default: 2)"""
    display_name = "Dactyl Min Techlevel"
    range_start = 0
    range_end = 8
    default = 2


class DeathPeakMinLevel(Range):
    """Minimum level at which the death_peak recruit can join (default: 37)"""
    display_name = "Death Peak Min Level"
    range_start = 1
    range_end = 99
    default = 37


class DeathPeakMinTechlevel(Range):
    """Minimum techlevel at which the death_peak recruit can join (default: 8)"""
    display_name = "Death Peak Min Techlevel"
    range_start = 0
    range_end = 8
    default = 8


class YakraBoxMinLevel(Range):
    """Minimum level at which the yakra_box recruit can join (default: 25)"""
    display_name = "Yakra Box Min Level"
    range_start = 1
    range_end = 99
    default = 25


class YakraBoxMinTechlevel(Range):
    """Minimum techlevel at which the yakra_box recruit can join (default: 3)"""
    display_name = "Yakra Box Min Techlevel"
    range_start = 0
    range_end = 8
    default = 3


class MinimumRecruits(Toggle):
    """All recruits are given a min level of 1 and min tech level of 0, overrides other settings"""
    display_name = "Minimum Recruits"


class ScaleLevelToLeader(Toggle):
    """Recruits are scaled to the level of the lead character (but not below the spot minimum)"""
    display_name = "Scale Level To Leader"


class ScaleTechlevelToLeader(Toggle):
    """Recruits are scaled to the tech level of the lead character (but not below the spot minimum)"""
    display_name = "Scale Techlevel To Leader"


class ScaleGear(Toggle):
    """Recruit gear is scaled based on the level at which they are recruited"""
    display_name = "Scale Gear"


class LootPool(Choice):
    """Method to determine which loot is available for assignment"""
    display_name = "Loot Pool"

    option_vanilla = 0
    option_rdi_random = 1
    option_tiered_random = 2
    default = 0


class CustomLootPool(FreeText):
    """Custom distribution for loot pool (e.g. 75:"vanilla", 25:"random"). Overrides loot_pool.  Leave "none" to ignore."""
    display_name = "Custom Loot Pool"
    default = ""


class LootAssignmentScheme(Choice):
    """Method used to assign loot."""
    display_name = "Loot Assignment Scheme"

    option_shuffle = 0
    option_logic_depth = 1
    default = 0


class GoodLootRate(Range):
    """Percent chance to fill a good loot spot with good loot"""
    display_name = "Good Loot Rate"
    range_start = 0
    range_end = 1
    default = 1


class PostAssignShuffleRate(Range):
    """Percent chance to shuffle after basic assignment"""
    display_name = "Post Assign Shuffle Rate"
    range_start = 0
    range_end = 1
    default = 1


class TradingPostBaseCost(Range):
    """Number of materials of each type required for base trade"""
    display_name = "Trading Post Base Cost"
    range_start = 1
    range_end = 10
    default = 3


class TradingPostUpgradeCost(Range):
    """Number of materials of each type required for upgraded trade"""
    display_name = "Trading Post Upgrade Cost"
    range_start = 1
    range_end = 10
    default = 3


class TradingPostSpecialCost(Range):
    """Number of materials of each type required for special trade"""
    display_name = "Trading Post Special Cost"
    range_start = 1
    range_end = 15
    default = 10


class JohnnyKeyThreshold(Range):
    """Points needed for the Johnny key item"""
    display_name = "Johnny Key Threshold"
    range_start = 0
    range_end = 2500
    default = 1500


class JohnnyLowThreshold(Range):
    """Points needed for the low tier Johnny rewards"""
    display_name = "Johnny Low Threshold"
    range_start = 0
    range_end = 2500
    default = 1200


class JohnnyLowItem(Choice):
    """Low tier Johnny item reward"""
    display_name = "Johnny Low Item"

    option_wood_sword = 0
    option_iron_blade = 1
    option_steelsaber = 2
    option_lode_sword = 3
    option_red_katana = 4
    option_flint_edge = 5
    option_dark_saber = 6
    option_aeon_blade = 7
    option_demon_edge = 8
    option_alloyblade = 9
    option_star_sword = 10
    option_vedicblade = 11
    option_kali_blade = 12
    option_shiva_edge = 13
    option_bolt_sword = 14
    option_slasher = 15
    option_bronze_bow = 16
    option_iron_bow = 17
    option_lode_bow = 18
    option_robin_bow = 19
    option_sage_bow = 20
    option_dream_bow = 21
    option_cometarrow = 22
    option_sonicarrow = 23
    option_valkerye = 24
    option_siren = 25
    option_air_gun = 26
    option_dart_gun = 27
    option_auto_gun = 28
    option_picomagnum = 29
    option_plasma_gun = 30
    option_ruby_gun = 31
    option_dream_gun = 32
    option_megablast = 33
    option_shock_wave = 34
    option_wondershot = 35
    option_graedus = 36
    option_tin_arm = 37
    option_hammer_arm = 38
    option_miragehand = 39
    option_stone_arm = 40
    option_doomfinger = 41
    option_magma_hand = 42
    option_megatonarm = 43
    option_big_hand = 44
    option_kaiser_arm = 45
    option_giga_arm = 46
    option_terra_arm = 47
    option_crisis_arm = 48
    option_bronzeedge = 49
    option_iron_sword = 50
    option_masamune_1 = 51
    option_flashblade = 52
    option_pearl_edge = 53
    option_rune_blade = 54
    option_bravesword = 55
    option_masamune_2 = 56
    option_demon_hit = 57
    option_fist = 58
    option_fist_2 = 59
    option_fist_3 = 60
    option_iron_fist = 61
    option_bronzefist = 62
    option_darkscythe = 63
    option_hurricane = 64
    option_starscythe = 65
    option_doomsickle = 66
    option_mop = 67
    option_bent_sword = 68
    option_bent_hilt = 69
    option_swallow = 70
    option_slasher_2 = 71
    option_rainbow = 72
    option_hide_tunic = 73
    option_karate_gi = 74
    option_bronzemail = 75
    option_maidensuit = 76
    option_iron_suit = 77
    option_titan_vest = 78
    option_gold_suit = 79
    option_ruby_vest = 80
    option_dark_mail = 81
    option_mist_robe = 82
    option_meso_mail = 83
    option_lumin_robe = 84
    option_flash_mail = 85
    option_lode_vest = 86
    option_aeon_suit = 87
    option_zodiaccape = 88
    option_nova_armor = 89
    option_prismdress = 90
    option_moon_armor = 91
    option_ruby_armor = 92
    option_ravenarmor = 93
    option_gloom_cape = 94
    option_white_mail = 95
    option_black_mail = 96
    option_blue_mail = 97
    option_red_mail = 98
    option_white_vest = 99
    option_black_vest = 100
    option_blue_vest = 101
    option_red_vest = 102
    option_taban_vest = 103
    option_taban_suit = 104
    option_hide_cap = 105
    option_bronzehelm = 106
    option_iron_helm = 107
    option_beret = 108
    option_gold_helm = 109
    option_rock_helm = 110
    option_ceratopper = 111
    option_glow_helm = 112
    option_lode_helm = 113
    option_aeon_helm = 114
    option_prism_helm = 115
    option_doom_helm = 116
    option_dark_helm = 117
    option_gloom_helm = 118
    option_safe_helm = 119
    option_taban_helm = 120
    option_sight_cap = 121
    option_memory_cap = 122
    option_time_hat = 123
    option_vigil_hat = 124
    option_ozziepants = 125
    option_haste_helm = 126
    option_rbow_helm = 127
    option_mermaidcap = 128
    option_bandana = 129
    option_ribbon = 130
    option_powerglove = 131
    option_defender = 132
    option_magicscarf = 133
    option_amulet = 134
    option_dash_ring = 135
    option_hit_ring = 136
    option_power_ring = 137
    option_magic_ring = 138
    option_wall_ring = 139
    option_silvererng = 140
    option_gold_erng = 141
    option_silverstud = 142
    option_gold_stud = 143
    option_sightscope = 144
    option_charm_top = 145
    option_rage_band = 146
    option_frenzyband = 147
    option_third_eye = 148
    option_wallet = 149
    option_greendream = 150
    option_berserker = 151
    option_powerscarf = 152
    option_speed_belt = 153
    option_black_rock = 154
    option_blue_rock = 155
    option_silverrock = 156
    option_white_rock = 157
    option_gold_rock = 158
    option_hero_medal = 159
    option_musclering = 160
    option_flea_vest = 161
    option_magic_seal = 162
    option_power_seal = 163
    option_valor_crest = 164
    option_dragon_tear = 165
    option_sun_shades = 166
    option_prismspecs = 167
    option_tonic = 168
    option_mid_tonic = 169
    option_full_tonic = 170
    option_ether = 171
    option_mid_ether = 172
    option_full_ether = 173
    option_elixir = 174
    option_hyperether = 175
    option_megaelixir = 176
    option_heal = 177
    option_revive = 178
    option_shelter = 179
    option_power_meal = 180
    option_lapis = 181
    option_barrier = 182
    option_shield = 183
    option_power_tab = 184
    option_magic_tab = 185
    option_speed_tab = 186
    option_petal = 187
    option_fang = 188
    option_horn = 189
    option_feather = 190
    option_seed = 191
    option_bike_key = 192
    option_pendant = 193
    option_gate_key = 194
    option_prismshard = 195
    option_c_trigger = 196
    option_tools = 197
    option_jerky = 198
    option_dreamstone = 199
    option_race_log = 200
    option_moon_stone = 201
    option_sun_stone = 202
    option_ruby_knife = 203
    option_yakra_key = 204
    option_clone = 205
    option_tomas_pop = 206
    option_petals_2 = 207
    option_fangs_2 = 208
    option_horns_2 = 209
    option_feathers_2 = 210
    option_jetsoftime = 211
    option_pendant_charge = 212
    option_rainbow_shell = 213
    default = 169


class JohnnyLowQuantity(Range):
    """Number of items for the low tier Johnny reward"""
    display_name = "Johnny Low Quantity"
    range_start = 1
    range_end = 10
    default = 5


class JohnnyMidThreshold(Range):
    """Points needed for the mid tier Johnny rewards"""
    display_name = "Johnny Mid Threshold"
    range_start = 0
    range_end = 2500
    default = 2000


class JohnnyMidItem(Choice):
    """Mid tier Johnny item reward"""
    display_name = "Johnny Mid Item"

    option_wood_sword = 0
    option_iron_blade = 1
    option_steelsaber = 2
    option_lode_sword = 3
    option_red_katana = 4
    option_flint_edge = 5
    option_dark_saber = 6
    option_aeon_blade = 7
    option_demon_edge = 8
    option_alloyblade = 9
    option_star_sword = 10
    option_vedicblade = 11
    option_kali_blade = 12
    option_shiva_edge = 13
    option_bolt_sword = 14
    option_slasher = 15
    option_bronze_bow = 16
    option_iron_bow = 17
    option_lode_bow = 18
    option_robin_bow = 19
    option_sage_bow = 20
    option_dream_bow = 21
    option_cometarrow = 22
    option_sonicarrow = 23
    option_valkerye = 24
    option_siren = 25
    option_air_gun = 26
    option_dart_gun = 27
    option_auto_gun = 28
    option_picomagnum = 29
    option_plasma_gun = 30
    option_ruby_gun = 31
    option_dream_gun = 32
    option_megablast = 33
    option_shock_wave = 34
    option_wondershot = 35
    option_graedus = 36
    option_tin_arm = 37
    option_hammer_arm = 38
    option_miragehand = 39
    option_stone_arm = 40
    option_doomfinger = 41
    option_magma_hand = 42
    option_megatonarm = 43
    option_big_hand = 44
    option_kaiser_arm = 45
    option_giga_arm = 46
    option_terra_arm = 47
    option_crisis_arm = 48
    option_bronzeedge = 49
    option_iron_sword = 50
    option_masamune_1 = 51
    option_flashblade = 52
    option_pearl_edge = 53
    option_rune_blade = 54
    option_bravesword = 55
    option_masamune_2 = 56
    option_demon_hit = 57
    option_fist = 58
    option_fist_2 = 59
    option_fist_3 = 60
    option_iron_fist = 61
    option_bronzefist = 62
    option_darkscythe = 63
    option_hurricane = 64
    option_starscythe = 65
    option_doomsickle = 66
    option_mop = 67
    option_bent_sword = 68
    option_bent_hilt = 69
    option_swallow = 70
    option_slasher_2 = 71
    option_rainbow = 72
    option_hide_tunic = 73
    option_karate_gi = 74
    option_bronzemail = 75
    option_maidensuit = 76
    option_iron_suit = 77
    option_titan_vest = 78
    option_gold_suit = 79
    option_ruby_vest = 80
    option_dark_mail = 81
    option_mist_robe = 82
    option_meso_mail = 83
    option_lumin_robe = 84
    option_flash_mail = 85
    option_lode_vest = 86
    option_aeon_suit = 87
    option_zodiaccape = 88
    option_nova_armor = 89
    option_prismdress = 90
    option_moon_armor = 91
    option_ruby_armor = 92
    option_ravenarmor = 93
    option_gloom_cape = 94
    option_white_mail = 95
    option_black_mail = 96
    option_blue_mail = 97
    option_red_mail = 98
    option_white_vest = 99
    option_black_vest = 100
    option_blue_vest = 101
    option_red_vest = 102
    option_taban_vest = 103
    option_taban_suit = 104
    option_hide_cap = 105
    option_bronzehelm = 106
    option_iron_helm = 107
    option_beret = 108
    option_gold_helm = 109
    option_rock_helm = 110
    option_ceratopper = 111
    option_glow_helm = 112
    option_lode_helm = 113
    option_aeon_helm = 114
    option_prism_helm = 115
    option_doom_helm = 116
    option_dark_helm = 117
    option_gloom_helm = 118
    option_safe_helm = 119
    option_taban_helm = 120
    option_sight_cap = 121
    option_memory_cap = 122
    option_time_hat = 123
    option_vigil_hat = 124
    option_ozziepants = 125
    option_haste_helm = 126
    option_rbow_helm = 127
    option_mermaidcap = 128
    option_bandana = 129
    option_ribbon = 130
    option_powerglove = 131
    option_defender = 132
    option_magicscarf = 133
    option_amulet = 134
    option_dash_ring = 135
    option_hit_ring = 136
    option_power_ring = 137
    option_magic_ring = 138
    option_wall_ring = 139
    option_silvererng = 140
    option_gold_erng = 141
    option_silverstud = 142
    option_gold_stud = 143
    option_sightscope = 144
    option_charm_top = 145
    option_rage_band = 146
    option_frenzyband = 147
    option_third_eye = 148
    option_wallet = 149
    option_greendream = 150
    option_berserker = 151
    option_powerscarf = 152
    option_speed_belt = 153
    option_black_rock = 154
    option_blue_rock = 155
    option_silverrock = 156
    option_white_rock = 157
    option_gold_rock = 158
    option_hero_medal = 159
    option_musclering = 160
    option_flea_vest = 161
    option_magic_seal = 162
    option_power_seal = 163
    option_valor_crest = 164
    option_dragon_tear = 165
    option_sun_shades = 166
    option_prismspecs = 167
    option_tonic = 168
    option_mid_tonic = 169
    option_full_tonic = 170
    option_ether = 171
    option_mid_ether = 172
    option_full_ether = 173
    option_elixir = 174
    option_hyperether = 175
    option_megaelixir = 176
    option_heal = 177
    option_revive = 178
    option_shelter = 179
    option_power_meal = 180
    option_lapis = 181
    option_barrier = 182
    option_shield = 183
    option_power_tab = 184
    option_magic_tab = 185
    option_speed_tab = 186
    option_petal = 187
    option_fang = 188
    option_horn = 189
    option_feather = 190
    option_seed = 191
    option_bike_key = 192
    option_pendant = 193
    option_gate_key = 194
    option_prismshard = 195
    option_c_trigger = 196
    option_tools = 197
    option_jerky = 198
    option_dreamstone = 199
    option_race_log = 200
    option_moon_stone = 201
    option_sun_stone = 202
    option_ruby_knife = 203
    option_yakra_key = 204
    option_clone = 205
    option_tomas_pop = 206
    option_petals_2 = 207
    option_fangs_2 = 208
    option_horns_2 = 209
    option_feathers_2 = 210
    option_jetsoftime = 211
    option_pendant_charge = 212
    option_rainbow_shell = 213
    default = 171


class JohnnyMidQuantity(Range):
    """Number of items for the mid tier Johnny reward"""
    display_name = "Johnny Mid Quantity"
    range_start = 1
    range_end = 10
    default = 5


class JohnnyHighThreshold(Range):
    """Points needed for the high tier Johnny rewards"""
    display_name = "Johnny High Threshold"
    range_start = 0
    range_end = 2500
    default = 2300


class JohnnyHighItem(Choice):
    """High tier Johnny item reward"""
    display_name = "Johnny High Item"

    option_wood_sword = 0
    option_iron_blade = 1
    option_steelsaber = 2
    option_lode_sword = 3
    option_red_katana = 4
    option_flint_edge = 5
    option_dark_saber = 6
    option_aeon_blade = 7
    option_demon_edge = 8
    option_alloyblade = 9
    option_star_sword = 10
    option_vedicblade = 11
    option_kali_blade = 12
    option_shiva_edge = 13
    option_bolt_sword = 14
    option_slasher = 15
    option_bronze_bow = 16
    option_iron_bow = 17
    option_lode_bow = 18
    option_robin_bow = 19
    option_sage_bow = 20
    option_dream_bow = 21
    option_cometarrow = 22
    option_sonicarrow = 23
    option_valkerye = 24
    option_siren = 25
    option_air_gun = 26
    option_dart_gun = 27
    option_auto_gun = 28
    option_picomagnum = 29
    option_plasma_gun = 30
    option_ruby_gun = 31
    option_dream_gun = 32
    option_megablast = 33
    option_shock_wave = 34
    option_wondershot = 35
    option_graedus = 36
    option_tin_arm = 37
    option_hammer_arm = 38
    option_miragehand = 39
    option_stone_arm = 40
    option_doomfinger = 41
    option_magma_hand = 42
    option_megatonarm = 43
    option_big_hand = 44
    option_kaiser_arm = 45
    option_giga_arm = 46
    option_terra_arm = 47
    option_crisis_arm = 48
    option_bronzeedge = 49
    option_iron_sword = 50
    option_masamune_1 = 51
    option_flashblade = 52
    option_pearl_edge = 53
    option_rune_blade = 54
    option_bravesword = 55
    option_masamune_2 = 56
    option_demon_hit = 57
    option_fist = 58
    option_fist_2 = 59
    option_fist_3 = 60
    option_iron_fist = 61
    option_bronzefist = 62
    option_darkscythe = 63
    option_hurricane = 64
    option_starscythe = 65
    option_doomsickle = 66
    option_mop = 67
    option_bent_sword = 68
    option_bent_hilt = 69
    option_swallow = 70
    option_slasher_2 = 71
    option_rainbow = 72
    option_hide_tunic = 73
    option_karate_gi = 74
    option_bronzemail = 75
    option_maidensuit = 76
    option_iron_suit = 77
    option_titan_vest = 78
    option_gold_suit = 79
    option_ruby_vest = 80
    option_dark_mail = 81
    option_mist_robe = 82
    option_meso_mail = 83
    option_lumin_robe = 84
    option_flash_mail = 85
    option_lode_vest = 86
    option_aeon_suit = 87
    option_zodiaccape = 88
    option_nova_armor = 89
    option_prismdress = 90
    option_moon_armor = 91
    option_ruby_armor = 92
    option_ravenarmor = 93
    option_gloom_cape = 94
    option_white_mail = 95
    option_black_mail = 96
    option_blue_mail = 97
    option_red_mail = 98
    option_white_vest = 99
    option_black_vest = 100
    option_blue_vest = 101
    option_red_vest = 102
    option_taban_vest = 103
    option_taban_suit = 104
    option_hide_cap = 105
    option_bronzehelm = 106
    option_iron_helm = 107
    option_beret = 108
    option_gold_helm = 109
    option_rock_helm = 110
    option_ceratopper = 111
    option_glow_helm = 112
    option_lode_helm = 113
    option_aeon_helm = 114
    option_prism_helm = 115
    option_doom_helm = 116
    option_dark_helm = 117
    option_gloom_helm = 118
    option_safe_helm = 119
    option_taban_helm = 120
    option_sight_cap = 121
    option_memory_cap = 122
    option_time_hat = 123
    option_vigil_hat = 124
    option_ozziepants = 125
    option_haste_helm = 126
    option_rbow_helm = 127
    option_mermaidcap = 128
    option_bandana = 129
    option_ribbon = 130
    option_powerglove = 131
    option_defender = 132
    option_magicscarf = 133
    option_amulet = 134
    option_dash_ring = 135
    option_hit_ring = 136
    option_power_ring = 137
    option_magic_ring = 138
    option_wall_ring = 139
    option_silvererng = 140
    option_gold_erng = 141
    option_silverstud = 142
    option_gold_stud = 143
    option_sightscope = 144
    option_charm_top = 145
    option_rage_band = 146
    option_frenzyband = 147
    option_third_eye = 148
    option_wallet = 149
    option_greendream = 150
    option_berserker = 151
    option_powerscarf = 152
    option_speed_belt = 153
    option_black_rock = 154
    option_blue_rock = 155
    option_silverrock = 156
    option_white_rock = 157
    option_gold_rock = 158
    option_hero_medal = 159
    option_musclering = 160
    option_flea_vest = 161
    option_magic_seal = 162
    option_power_seal = 163
    option_valor_crest = 164
    option_dragon_tear = 165
    option_sun_shades = 166
    option_prismspecs = 167
    option_tonic = 168
    option_mid_tonic = 169
    option_full_tonic = 170
    option_ether = 171
    option_mid_ether = 172
    option_full_ether = 173
    option_elixir = 174
    option_hyperether = 175
    option_megaelixir = 176
    option_heal = 177
    option_revive = 178
    option_shelter = 179
    option_power_meal = 180
    option_lapis = 181
    option_barrier = 182
    option_shield = 183
    option_power_tab = 184
    option_magic_tab = 185
    option_speed_tab = 186
    option_petal = 187
    option_fang = 188
    option_horn = 189
    option_feather = 190
    option_seed = 191
    option_bike_key = 192
    option_pendant = 193
    option_gate_key = 194
    option_prismshard = 195
    option_c_trigger = 196
    option_tools = 197
    option_jerky = 198
    option_dreamstone = 199
    option_race_log = 200
    option_moon_stone = 201
    option_sun_stone = 202
    option_ruby_knife = 203
    option_yakra_key = 204
    option_clone = 205
    option_tomas_pop = 206
    option_petals_2 = 207
    option_fangs_2 = 208
    option_horns_2 = 209
    option_feathers_2 = 210
    option_jetsoftime = 211
    option_pendant_charge = 212
    option_rainbow_shell = 213
    default = 173


class JohnnyHighQuantity(Range):
    """Number of items for the high tier Johnny reward"""
    display_name = "Johnny High Quantity"
    range_start = 1
    range_end = 10
    default = 5


class SightscopeAll(Toggle):
    """Enable sightscope usage on all enemies."""
    display_name = "Sightscope All"


class ForcedSightscope(Toggle):
    """Sightscope effect will be present without the item equipped."""
    display_name = "Forced Sightscope"


class ShuffleEnemies(Toggle):
    """Normal enemy types are shuffled (respects enemy size)"""
    display_name = "Shuffle Enemies"


class DefaultFastLocMovement(Toggle):
    """Default location (dungeon, etc) movement is fast and run button slows"""
    display_name = "Default Fast Loc Movement"


class DefaultFastOwMovement(Toggle):
    """Default overworld movement is fast and run button slows"""
    display_name = "Default Fast Ow Movement"


class DefaultFastEpochMovement(Toggle):
    """Default epoch movement is fast and run button slows"""
    display_name = "Default Fast Epoch Movement"


class BattleSpeed(Range):
    """Default battle speed"""
    display_name = "Battle Speed"
    range_start = 1
    range_end = 8
    default = 5


class MessageSpeed(Range):
    """Default message speed"""
    display_name = "Message Speed"
    range_start = 1
    range_end = 8
    default = 5


class BattleMemoryCursor(Toggle):
    """By default turn battle memory cursor on"""
    display_name = "Battle Memory Cursor"


class MenuMemoryCursor(Toggle):
    """By default turn menu memory cursor on"""
    display_name = "Menu Memory Cursor"


class WindowBackground(Range):
    """Default window background"""
    display_name = "Window Background"
    range_start = 1
    range_end = 8
    default = 1


class UseLSelectWarp(Toggle):
    """Use L+Select instead of Start+Select for house warp"""
    display_name = "Use L Select Warp"


class UseMsu1(Toggle):
    """Apply an MSU-1 patch to the rom."""
    display_name = "Use Msu1"


class CronoPalette(FreeText):
    """Hex format palette for Crono"""
    display_name = "Crono Palette"
    default = ""


class MarlePalette(FreeText):
    """Hex format palette for Marle"""
    display_name = "Marle Palette"
    default = ""


class LuccaPalette(FreeText):
    """Hex format palette for Lucca"""
    display_name = "Lucca Palette"
    default = ""


class RoboPalette(FreeText):
    """Hex format palette for Robo"""
    display_name = "Robo Palette"
    default = ""


class FrogPalette(FreeText):
    """Hex format palette for Frog"""
    display_name = "Frog Palette"
    default = ""


class AylaPalette(FreeText):
    """Hex format palette for Ayla"""
    display_name = "Ayla Palette"
    default = ""


class MagusPalette(FreeText):
    """Hex format palette for Magus"""
    display_name = "Magus Palette"
    default = ""


class RemoveFlashes(Toggle):
    """Remove flashes from many animations"""
    display_name = "Remove Flashes"


class DsReplacementChance(Range):
    """Percent chance (e.g. 10 for 10 percent) to replace an item with a ds counterpart"""
    display_name = "Ds Replacement Chance"
    range_start = 0
    range_end = 100
    default = 50


class BronzeFistPolicy(Choice):
    """How to modify BronzeFist pre-shuffle"""
    display_name = "Bronze Fist Policy"

    option_vanilla = 0
    option_remove = 1
    option_4x_crit = 2
    option_random_other = 3
    default = 0


class WeaponRandoEffectScheme(Choice):
    """How to randomize weapon effects"""
    display_name = "Weapon Rando Effect Scheme"

    option_no_change = 0
    option_shuffle = 1
    option_shuffle_linked = 2
    option_rdi_random = 3
    default = 2


class WeaponRandoStatBoostScheme(Choice):
    """How to randomize weapon stat boosts"""
    display_name = "Weapon Rando Stat Boost Scheme"

    option_no_change = 0
    option_shuffle = 1
    option_shuffle_linked = 2
    option_rdi_random = 3
    default = 2


class RandomWeaponEffectSpec(FreeText):
    """Distribution for choosing random effects after the forced ones"""
    display_name = "Random Weapon Effect Spec"
    default = ""


class RandomWeaponStatBoostSpec(FreeText):
    """Distribution for choosing random stat boosts after the forced ones"""
    display_name = "Random Weapon Stat Boost Spec"
    default = ""


class WeaponRandoEffectScheme2(Choice):
    """How to randomize weapon effects"""
    display_name = "Weapon Rando Effect Scheme 2"

    option_no_change = 0
    option_shuffle = 1
    option_shuffle_linked = 2
    option_rdi_random = 3
    default = 2


class WeaponRandoStatBoostScheme2(Choice):
    """How to randomize weapon stat boosts"""
    display_name = "Weapon Rando Stat Boost Scheme 2"

    option_no_change = 0
    option_shuffle = 1
    option_shuffle_linked = 2
    option_rdi_random = 3
    default = 2


class RandomWeaponEffectSpec2(FreeText):
    """Distribution for choosing random effects after the forced ones"""
    display_name = "Random Weapon Effect Spec 2"
    default = ""


class RandomWeaponStatBoostSpec2(FreeText):
    """Distribution for choosing random stat boosts after the forced ones"""
    display_name = "Random Weapon Stat Boost Spec 2"
    default = ""


class WeaponRandoEffectScheme3(Choice):
    """How to randomize weapon effects"""
    display_name = "Weapon Rando Effect Scheme 3"

    option_no_change = 0
    option_shuffle = 1
    option_shuffle_linked = 2
    option_rdi_random = 3
    default = 2


class WeaponRandoStatBoostScheme3(Choice):
    """How to randomize weapon stat boosts"""
    display_name = "Weapon Rando Stat Boost Scheme 3"

    option_no_change = 0
    option_shuffle = 1
    option_shuffle_linked = 2
    option_rdi_random = 3
    default = 2


class RandomWeaponEffectSpec3(FreeText):
    """Distribution for choosing random effects after the forced ones"""
    display_name = "Random Weapon Effect Spec 3"
    default = ""


class RandomWeaponStatBoostSpec3(FreeText):
    """Distribution for choosing random stat boosts after the forced ones"""
    display_name = "Random Weapon Stat Boost Spec 3"
    default = ""


class UsePhysMarle(Toggle):
    """+Hit, Physical arrow tech"""
    display_name = "Use Phys Marle"


class UseHasteAll(Toggle):
    """AoE Haste, 15 MP cost"""
    display_name = "Use Haste All"


class UsePhysLucca(Toggle):
    """+Hit. Physical Flame Toss + Bombs"""
    display_name = "Use Phys Lucca"


class UseProtectAll(Toggle):
    """AoE Protect, 2x MP cost"""
    display_name = "Use Protect All"


class UseReraise(Toggle):
    """Life2 gives greendream effect"""
    display_name = "Use Reraise"


class UseMagusDualTechs(Toggle):
    """Magus can perform dual techs with fire/ice/lit2"""
    display_name = "Use Magus Dual Techs"


class UseDaltonizedMagus(Toggle):
    """Magus shadow techs are replaced with Dalton versions"""
    display_name = "Use Daltonized Magus"


class DaltonLevel(Range):
    """The internal level of Dalton [Experimental]"""
    display_name = "Dalton Level"
    range_start = 0
    range_end = 99
    default = 26


class DaltonPlusLevel(Range):
    """The internal level of Dalton Plus [Experimental]"""
    display_name = "Dalton Plus Level"
    range_start = 0
    range_end = 99
    default = 20


class ElderSpawnLevel(Range):
    """The internal level of Elder Spawn [Experimental]"""
    display_name = "Elder Spawn Level"
    range_start = 0
    range_end = 99
    default = 46


class FleaLevel(Range):
    """The internal level of Flea [Experimental]"""
    display_name = "Flea Level"
    range_start = 0
    range_end = 99
    default = 19


class GigaMutantLevel(Range):
    """The internal level of Giga Mutant [Experimental]"""
    display_name = "Giga Mutant Level"
    range_start = 0
    range_end = 99
    default = 47


class GolemLevel(Range):
    """The internal level of Golem [Experimental]"""
    display_name = "Golem Level"
    range_start = 0
    range_end = 99
    default = 27


class GolemBossLevel(Range):
    """The internal level of Golem Boss [Experimental]"""
    display_name = "Golem Boss Level"
    range_start = 0
    range_end = 99
    default = 34


class HeckranLevel(Range):
    """The internal level of Heckran [Experimental]"""
    display_name = "Heckran Level"
    range_start = 0
    range_end = 99
    default = 12


class LavosSpawnLevel(Range):
    """The internal level of Lavos Spawn [Experimental]"""
    display_name = "Lavos Spawn Level"
    range_start = 0
    range_end = 99
    default = 32


class MammonMachineLevel(Range):
    """The internal level of Mammon M [Experimental]"""
    display_name = "Mammon Machine Level"
    range_start = 0
    range_end = 99
    default = 44


class MagusNcLevel(Range):
    """The internal level of Magus (North Cape) [Experimental]"""
    display_name = "Magus Nc Level"
    range_start = 0
    range_end = 99
    default = 30


class MasaMuneLevel(Range):
    """The internal level of Masa Mune [Experimental]"""
    display_name = "Masa Mune Level"
    range_start = 0
    range_end = 99
    default = 15


class MegaMutantLevel(Range):
    """The internal level of Mega Mutant [Experimental]"""
    display_name = "Mega Mutant Level"
    range_start = 0
    range_end = 99
    default = 46


class MudImpLevel(Range):
    """The internal level of Mud Imp [Experimental]"""
    display_name = "Mud Imp Level"
    range_start = 0
    range_end = 99
    default = 29


class NizbelLevel(Range):
    """The internal level of Nizbel [Experimental]"""
    display_name = "Nizbel Level"
    range_start = 0
    range_end = 99
    default = 17


class Nizbel2Level(Range):
    """The internal level of Nizbel II [Experimental]"""
    display_name = "Nizbel 2 Level"
    range_start = 0
    range_end = 99
    default = 23


class RetiniteLevel(Range):
    """The internal level of Retinite [Experimental]"""
    display_name = "Retinite Level"
    range_start = 0
    range_end = 99
    default = 28


class RSeriesLevel(Range):
    """The internal level of R Series [Experimental]"""
    display_name = "R Series Level"
    range_start = 0
    range_end = 99
    default = 5


class RustTyranoLevel(Range):
    """The internal level of Rust Tyrano [Experimental]"""
    display_name = "Rust Tyrano Level"
    range_start = 0
    range_end = 99
    default = 35


class SlashLevel(Range):
    """The internal level of Slash Sword [Experimental]"""
    display_name = "Slash Level"
    range_start = 0
    range_end = 99
    default = 20


class SonOfSunLevel(Range):
    """The internal level of Son Of Sun [Experimental]"""
    display_name = "Son Of Sun Level"
    range_start = 0
    range_end = 99
    default = 43


class TerraMutantLevel(Range):
    """The internal level of Terra Mutant [Experimental]"""
    display_name = "Terra Mutant Level"
    range_start = 0
    range_end = 99
    default = 48


class YakraLevel(Range):
    """The internal level of Yakra [Experimental]"""
    display_name = "Yakra Level"
    range_start = 0
    range_end = 99
    default = 4


class YakraXiiiLevel(Range):
    """The internal level of Yakra XIII [Experimental]"""
    display_name = "Yakra Xiii Level"
    range_start = 0
    range_end = 99
    default = 39


class ZomborLevel(Range):
    """The internal level of Zombor [Experimental]"""
    display_name = "Zombor Level"
    range_start = 0
    range_end = 99
    default = 9


class DragonTankLevel(Range):
    """The internal level of Dragon Tank [Experimental]"""
    display_name = "Dragon Tank Level"
    range_start = 0
    range_end = 99
    default = 5


class GigaGaiaLevel(Range):
    """The internal level of Giga Gaia [Experimental]"""
    display_name = "Giga Gaia Level"
    range_start = 0
    range_end = 99
    default = 30


class GuardianLevel(Range):
    """The internal level of Guardian [Experimental]"""
    display_name = "Guardian Level"
    range_start = 0
    range_end = 99
    default = 6


class MagusLevel(Range):
    """The internal level of Magus [Experimental]"""
    display_name = "Magus Level"
    range_start = 0
    range_end = 99
    default = 20


class BlackTyranoLevel(Range):
    """The internal level of Black Tyrano [Experimental]"""
    display_name = "Black Tyrano Level"
    range_start = 0
    range_end = 99
    default = 20


class OzzieTrioLevel(Range):
    """The internal level of Ozzie Trio [Experimental]"""
    display_name = "Ozzie Trio Level"
    range_start = 0
    range_end = 99
    default = 33


class AtroposLevel(Range):
    """The internal level of Atropos Xr [Experimental]"""
    display_name = "Atropos Level"
    range_start = 0
    range_end = 99
    default = 33


class FleaPlusLevel(Range):
    """The internal level of Flea Plus [Experimental]"""
    display_name = "Flea Plus Level"
    range_start = 0
    range_end = 99
    default = 27


class SuperSlashLevel(Range):
    """The internal level of Super Slash [Experimental]"""
    display_name = "Super Slash Level"
    range_start = 0
    range_end = 99
    default = 27


class KrawlieLevel(Range):
    """The internal level of Krawlie [Experimental]"""
    display_name = "Krawlie Level"
    range_start = 0
    range_end = 99
    default = 6


class GatoLevel(Range):
    """The internal level of Gato [Experimental]"""
    display_name = "Gato Level"
    range_start = 0
    range_end = 99
    default = 1


class Zeal2Level(Range):
    """The internal level of Zeal 2 [Experimental]"""
    display_name = "Zeal2 Level"
    range_start = 0
    range_end = 99
    default = 50


@dataclass
class CTRDIOptions(PerGameCommonOptions):
    xp_scale: XpScale
    tp_scale: TpScale
    split_tp: SplitTp
    fix_tp_doubling: FixTpDoubling
    xp_penalty_level: XpPenaltyLevel
    xp_penalty_percent: XpPenaltyPercent
    level_cap: LevelCap
    boss_xp_factor: BossXpFactor
    midboss_reward_factor: MidbossRewardFactor
    normalize_boss_xp: NormalizeBossXp
    drop_enemy_pool: DropEnemyPool
    drop_reward_pool: DropRewardPool
    drop_rate: DropRate
    mark_dropping_enemies: MarkDroppingEnemies
    charm_enemy_pool: CharmEnemyPool
    charm_reward_pool: CharmRewardPool
    charm_rate: CharmRate
    mark_charmable_enemies: MarkCharmableEnemies
    tech_order: TechOrder
    tech_damage: TechDamage
    tech_damage_random_factor_min: TechDamageRandomFactorMin
    tech_damage_random_factor_max: TechDamageRandomFactorMax
    preserve_magic: PreserveMagic
    black_hole_factor: BlackHoleFactor
    black_hole_min: BlackHoleMin
    show_full_tech_list: ShowFullTechList
    balance_tech_mps: BalanceTechMps
    dynamic_scaling_scheme: DynamicScalingScheme
    levels_per_boss: LevelsPerBoss
    levels_per_quest: LevelsPerQuest
    levels_per_key_item: LevelsPerKeyItem
    levels_per_objective: LevelsPerObjective
    levels_per_character: LevelsPerCharacter
    max_scaling_level: MaxScalingLevel
    dynamic_scale_lavos: DynamicScaleLavos
    dynamic_scale_lavos_gauntlet: DynamicScaleLavosGauntlet
    defense_safety_min_level: DefenseSafetyMinLevel
    defense_safety_max_level: DefenseSafetyMaxLevel
    obstacle_safety_level: ObstacleSafetyLevel
    normal_enemy_hp_scale: NormalEnemyHpScale
    static_boss_hp_scale: StaticBossHpScale
    static_hp_scale_lavos: StaticHpScaleLavos
    element_safety_level: ElementSafetyLevel
    millennial_fair_mod: MillennialFairMod
    guardia_forest_1000_mod: GuardiaForest1000Mod
    guardia_forest_600_mod: GuardiaForest600Mod
    crono_trial_mod: CronoTrialMod
    heckran_cave_mod: HeckranCaveMod
    truce_canyon_mod: TruceCanyonMod
    manoria_cathedral_mod: ManoriaCathedralMod
    denadoro_mountains_mod: DenadoroMountainsMod
    cursed_woods_mod: CursedWoodsMod
    lab_16_mod: Lab16Mod
    lab_32_mod: Lab32Mod
    sewers_mod: SewersMod
    death_peak_mod: DeathPeakMod
    arris_dome_mod: ArrisDomeMod
    proto_dome_mod: ProtoDomeMod
    factory_ruins_mod: FactoryRuinsMod
    mystic_mountains_mod: MysticMountainsMod
    hunting_range_mod: HuntingRangeMod
    dactyl_nest_mod: DactylNestMod
    shell_trial_mod: ShellTrialMod
    zenan_bridge_mod: ZenanBridgeMod
    northern_ruins_mod: NorthernRuinsMod
    giants_claw_mod: GiantsClawMod
    ozzies_fort_mod: OzziesFortMod
    magus_castle_mod: MagusCastleMod
    magic_cave_mod: MagicCaveMod
    sunken_desert_mod: SunkenDesertMod
    sun_palace_mod: SunPalaceMod
    geno_dome_mod: GenoDomeMod
    forest_maze_mod: ForestMazeMod
    reptite_lair_mod: ReptiteLairMod
    tyrano_lair_mod: TyranoLairMod
    black_omen_mod: BlackOmenMod
    north_cape_mod: NorthCapeMod
    epoch_battle_mod: EpochBattleMod
    blackbird_mod: BlackbirdMod
    enhasa_mod: EnhasaMod
    ocean_palace_mod: OceanPalaceMod
    mt_woe_mod: MtWoeMod
    incentive_factor: IncentiveFactor
    hard_lavos_end_boss: HardLavosEndBoss
    boats_of_time: BoatsOfTime
    jets_of_time: JetsOfTime
    boss_randomization_type: BossRandomizationType
    midboss_randomization_type: MidbossRandomizationType
    shop_inventory_randomization: ShopInventoryRandomization
    shop_capacity_randomization: ShopCapacityRandomization
    item_base_prices: ItemBasePrices
    item_price_randomization: ItemPriceRandomization
    item_price_min_multiplier: ItemPriceMinMultiplier
    item_price_max_multiplier: ItemPriceMaxMultiplier
    num_algetty_portal_objectives: NumAlgettyPortalObjectives
    num_omen_objectives: NumOmenObjectives
    num_bucket_objectives: NumBucketObjectives
    num_gauntlet_objectives: NumGauntletObjectives
    num_timegauge_objectives: NumTimegaugeObjectives
    objective_1: Objective1
    objective_2: Objective2
    objective_3: Objective3
    objective_4: Objective4
    objective_5: Objective5
    objective_6: Objective6
    objective_7: Objective7
    objective_8: Objective8
    shuffle_entrances: ShuffleEntrances
    rest_vanilla: RestVanilla
    starter_min_level: StarterMinLevel
    starter_min_techlevel: StarterMinTechlevel
    fair_min_level: FairMinLevel
    fair_min_techlevel: FairMinTechlevel
    cathedral_min_level: CathedralMinLevel
    cathedral_min_techlevel: CathedralMinTechlevel
    castle_min_level: CastleMinLevel
    castle_min_techlevel: CastleMinTechlevel
    trial_min_level: TrialMinLevel
    trial_min_techlevel: TrialMinTechlevel
    proto_min_level: ProtoMinLevel
    proto_min_techlevel: ProtoMinTechlevel
    north_cape_min_level: NorthCapeMinLevel
    north_cape_min_techlevel: NorthCapeMinTechlevel
    burrow_min_level: BurrowMinLevel
    burrow_min_techlevel: BurrowMinTechlevel
    dactyl_min_level: DactylMinLevel
    dactyl_min_techlevel: DactylMinTechlevel
    death_peak_min_level: DeathPeakMinLevel
    death_peak_min_techlevel: DeathPeakMinTechlevel
    yakra_box_min_level: YakraBoxMinLevel
    yakra_box_min_techlevel: YakraBoxMinTechlevel
    minimum_recruits: MinimumRecruits
    scale_level_to_leader: ScaleLevelToLeader
    scale_techlevel_to_leader: ScaleTechlevelToLeader
    scale_gear: ScaleGear
    loot_pool: LootPool
    custom_loot_pool: CustomLootPool
    loot_assignment_scheme: LootAssignmentScheme
    good_loot_rate: GoodLootRate
    post_assign_shuffle_rate: PostAssignShuffleRate
    trading_post_base_cost: TradingPostBaseCost
    trading_post_upgrade_cost: TradingPostUpgradeCost
    trading_post_special_cost: TradingPostSpecialCost
    johnny_key_threshold: JohnnyKeyThreshold
    johnny_low_threshold: JohnnyLowThreshold
    johnny_low_item: JohnnyLowItem
    johnny_low_quantity: JohnnyLowQuantity
    johnny_mid_threshold: JohnnyMidThreshold
    johnny_mid_item: JohnnyMidItem
    johnny_mid_quantity: JohnnyMidQuantity
    johnny_high_threshold: JohnnyHighThreshold
    johnny_high_item: JohnnyHighItem
    johnny_high_quantity: JohnnyHighQuantity
    sightscope_all: SightscopeAll
    forced_sightscope: ForcedSightscope
    shuffle_enemies: ShuffleEnemies
    default_fast_loc_movement: DefaultFastLocMovement
    default_fast_ow_movement: DefaultFastOwMovement
    default_fast_epoch_movement: DefaultFastEpochMovement
    battle_speed: BattleSpeed
    message_speed: MessageSpeed
    battle_memory_cursor: BattleMemoryCursor
    menu_memory_cursor: MenuMemoryCursor
    window_background: WindowBackground
    use_l_select_warp: UseLSelectWarp
    use_msu1: UseMsu1
    crono_palette: CronoPalette
    marle_palette: MarlePalette
    lucca_palette: LuccaPalette
    robo_palette: RoboPalette
    frog_palette: FrogPalette
    ayla_palette: AylaPalette
    magus_palette: MagusPalette
    remove_flashes: RemoveFlashes
    ds_replacement_chance: DsReplacementChance
    bronze_fist_policy: BronzeFistPolicy
    weapon_rando_effect_scheme: WeaponRandoEffectScheme
    weapon_rando_stat_boost_scheme: WeaponRandoStatBoostScheme
    random_weapon_effect_spec: RandomWeaponEffectSpec
    random_weapon_stat_boost_spec: RandomWeaponStatBoostSpec
    weapon_rando_effect_scheme_2: WeaponRandoEffectScheme2
    weapon_rando_stat_boost_scheme_2: WeaponRandoStatBoostScheme2
    random_weapon_effect_spec_2: RandomWeaponEffectSpec2
    random_weapon_stat_boost_spec_2: RandomWeaponStatBoostSpec2
    weapon_rando_effect_scheme_3: WeaponRandoEffectScheme3
    weapon_rando_stat_boost_scheme_3: WeaponRandoStatBoostScheme3
    random_weapon_effect_spec_3: RandomWeaponEffectSpec3
    random_weapon_stat_boost_spec_3: RandomWeaponStatBoostSpec3
    use_phys_marle: UsePhysMarle
    use_haste_all: UseHasteAll
    use_phys_lucca: UsePhysLucca
    use_protect_all: UseProtectAll
    use_reraise: UseReraise
    use_magus_dual_techs: UseMagusDualTechs
    use_daltonized_magus: UseDaltonizedMagus
    dalton_level: DaltonLevel
    dalton_plus_level: DaltonPlusLevel
    elder_spawn_level: ElderSpawnLevel
    flea_level: FleaLevel
    giga_mutant_level: GigaMutantLevel
    golem_level: GolemLevel
    golem_boss_level: GolemBossLevel
    heckran_level: HeckranLevel
    lavos_spawn_level: LavosSpawnLevel
    mammon_machine_level: MammonMachineLevel
    magus_nc_level: MagusNcLevel
    masa_mune_level: MasaMuneLevel
    mega_mutant_level: MegaMutantLevel
    mud_imp_level: MudImpLevel
    nizbel_level: NizbelLevel
    nizbel_2_level: Nizbel2Level
    retinite_level: RetiniteLevel
    r_series_level: RSeriesLevel
    rust_tyrano_level: RustTyranoLevel
    slash_level: SlashLevel
    son_of_sun_level: SonOfSunLevel
    terra_mutant_level: TerraMutantLevel
    yakra_level: YakraLevel
    yakra_xiii_level: YakraXiiiLevel
    zombor_level: ZomborLevel
    dragon_tank_level: DragonTankLevel
    giga_gaia_level: GigaGaiaLevel
    guardian_level: GuardianLevel
    magus_level: MagusLevel
    black_tyrano_level: BlackTyranoLevel
    ozzie_trio_level: OzzieTrioLevel
    atropos_level: AtroposLevel
    flea_plus_level: FleaPlusLevel
    super_slash_level: SuperSlashLevel
    krawlie_level: KrawlieLevel
    gato_level: GatoLevel
    zeal2_level: Zeal2Level


option_groups: list[OptionGroup] = [

    OptionGroup(
        "Battle Rewards",
        [
            XpScale,
            TpScale,
            SplitTp,
            FixTpDoubling,
            XpPenaltyLevel,
            XpPenaltyPercent,
            LevelCap,
            BossXpFactor,
            MidbossRewardFactor,
            NormalizeBossXp,
            DropEnemyPool,
            DropRewardPool,
            DropRate,
            MarkDroppingEnemies,
            CharmEnemyPool,
            CharmRewardPool,
            CharmRate,
            MarkCharmableEnemies,

        ]
    ),

    OptionGroup(
        "Tech Options",
        [
            TechOrder,
            TechDamage,
            TechDamageRandomFactorMin,
            TechDamageRandomFactorMax,
            PreserveMagic,
            BlackHoleFactor,
            BlackHoleMin,
            ShowFullTechList,
            BalanceTechMps,

        ]
    ),

    OptionGroup(
        "Scaling Options",
        [
            DynamicScalingScheme,
            LevelsPerBoss,
            LevelsPerQuest,
            LevelsPerKeyItem,
            LevelsPerObjective,
            LevelsPerCharacter,
            MaxScalingLevel,
            DynamicScaleLavos,
            DynamicScaleLavosGauntlet,
            DefenseSafetyMinLevel,
            DefenseSafetyMaxLevel,
            ObstacleSafetyLevel,
            NormalEnemyHpScale,
            StaticBossHpScale,
            StaticHpScaleLavos,
            ElementSafetyLevel,
            MillennialFairMod,
            GuardiaForest1000Mod,
            GuardiaForest600Mod,
            CronoTrialMod,
            HeckranCaveMod,
            TruceCanyonMod,
            ManoriaCathedralMod,
            DenadoroMountainsMod,
            CursedWoodsMod,
            Lab16Mod,
            Lab32Mod,
            SewersMod,
            DeathPeakMod,
            ArrisDomeMod,
            ProtoDomeMod,
            FactoryRuinsMod,
            MysticMountainsMod,
            HuntingRangeMod,
            DactylNestMod,
            ShellTrialMod,
            ZenanBridgeMod,
            NorthernRuinsMod,
            GiantsClawMod,
            OzziesFortMod,
            MagusCastleMod,
            MagicCaveMod,
            SunkenDesertMod,
            SunPalaceMod,
            GenoDomeMod,
            ForestMazeMod,
            ReptiteLairMod,
            TyranoLairMod,
            BlackOmenMod,
            NorthCapeMod,
            EpochBattleMod,
            BlackbirdMod,
            EnhasaMod,
            OceanPalaceMod,
            MtWoeMod,

        ]
    ),

    OptionGroup(
        "Logic Options",
        [
            IncentiveFactor,
            HardLavosEndBoss,
            BoatsOfTime,
            JetsOfTime,

        ]
    ),

    OptionGroup(
        "Boss Rando Options",
        [
            BossRandomizationType,
            MidbossRandomizationType,

        ]
    ),

    OptionGroup(
        "Shop Options",
        [
            ShopInventoryRandomization,
            ShopCapacityRandomization,
            ItemBasePrices,
            ItemPriceRandomization,
            ItemPriceMinMultiplier,
            ItemPriceMaxMultiplier,

        ]
    ),

    OptionGroup(
        "Objective Options",
        [
            NumAlgettyPortalObjectives,
            NumOmenObjectives,
            NumBucketObjectives,
            NumGauntletObjectives,
            NumTimegaugeObjectives,
            Objective1,
            Objective2,
            Objective3,
            Objective4,
            Objective5,
            Objective6,
            Objective7,
            Objective8,

        ]
    ),

    OptionGroup(
        "Entrance Options",
        [
            ShuffleEntrances,
            RestVanilla,

        ]
    ),

    OptionGroup(
        "Recruit Options",
        [
            StarterMinLevel,
            StarterMinTechlevel,
            FairMinLevel,
            FairMinTechlevel,
            CathedralMinLevel,
            CathedralMinTechlevel,
            CastleMinLevel,
            CastleMinTechlevel,
            TrialMinLevel,
            TrialMinTechlevel,
            ProtoMinLevel,
            ProtoMinTechlevel,
            NorthCapeMinLevel,
            NorthCapeMinTechlevel,
            BurrowMinLevel,
            BurrowMinTechlevel,
            DactylMinLevel,
            DactylMinTechlevel,
            DeathPeakMinLevel,
            DeathPeakMinTechlevel,
            YakraBoxMinLevel,
            YakraBoxMinTechlevel,
            MinimumRecruits,
            ScaleLevelToLeader,
            ScaleTechlevelToLeader,
            ScaleGear,

        ]
    ),

    OptionGroup(
        "Treasure Options",
        [
            LootPool,
            CustomLootPool,
            LootAssignmentScheme,
            GoodLootRate,
            PostAssignShuffleRate,
            TradingPostBaseCost,
            TradingPostUpgradeCost,
            TradingPostSpecialCost,
            JohnnyKeyThreshold,
            JohnnyLowThreshold,
            JohnnyLowItem,
            JohnnyLowQuantity,
            JohnnyMidThreshold,
            JohnnyMidItem,
            JohnnyMidQuantity,
            JohnnyHighThreshold,
            JohnnyHighItem,
            JohnnyHighQuantity,

        ]
    ),

    OptionGroup(
        "Enemy Options",
        [
            SightscopeAll,
            ForcedSightscope,
            ShuffleEnemies,

        ]
    ),

    OptionGroup(
        "Post Rando Options",
        [
            DefaultFastLocMovement,
            DefaultFastOwMovement,
            DefaultFastEpochMovement,
            BattleSpeed,
            MessageSpeed,
            BattleMemoryCursor,
            MenuMemoryCursor,
            WindowBackground,
            UseLSelectWarp,
            UseMsu1,
            CronoPalette,
            MarlePalette,
            LuccaPalette,
            RoboPalette,
            FrogPalette,
            AylaPalette,
            MagusPalette,
            RemoveFlashes,

        ]
    ),

    OptionGroup(
        "Gear Rando Options",
        [
            DsReplacementChance,
            BronzeFistPolicy,
            WeaponRandoEffectScheme,
            WeaponRandoStatBoostScheme,
            RandomWeaponEffectSpec,
            RandomWeaponStatBoostSpec,
            WeaponRandoEffectScheme2,
            WeaponRandoStatBoostScheme2,
            RandomWeaponEffectSpec2,
            RandomWeaponStatBoostSpec2,
            WeaponRandoEffectScheme3,
            WeaponRandoStatBoostScheme3,
            RandomWeaponEffectSpec3,
            RandomWeaponStatBoostSpec3,

        ]
    ),

    OptionGroup(
        "Character Options",
        [
            UsePhysMarle,
            UseHasteAll,
            UsePhysLucca,
            UseProtectAll,
            UseReraise,
            UseMagusDualTechs,
            UseDaltonizedMagus,

        ]
    ),

    OptionGroup(
        "Boss Scaling Options",
        [
            DaltonLevel,
            DaltonPlusLevel,
            ElderSpawnLevel,
            FleaLevel,
            GigaMutantLevel,
            GolemLevel,
            GolemBossLevel,
            HeckranLevel,
            LavosSpawnLevel,
            MammonMachineLevel,
            MagusNcLevel,
            MasaMuneLevel,
            MegaMutantLevel,
            MudImpLevel,
            NizbelLevel,
            Nizbel2Level,
            RetiniteLevel,
            RSeriesLevel,
            RustTyranoLevel,
            SlashLevel,
            SonOfSunLevel,
            TerraMutantLevel,
            YakraLevel,
            YakraXiiiLevel,
            ZomborLevel,
            DragonTankLevel,
            GigaGaiaLevel,
            GuardianLevel,
            MagusLevel,
            BlackTyranoLevel,
            OzzieTrioLevel,
            AtroposLevel,
            FleaPlusLevel,
            SuperSlashLevel,
            KrawlieLevel,
            GatoLevel,
            Zeal2Level,

        ]
    )
]
