# Ability variant enums

`AbilityType` for the type of single variant.

This will be used to connect to any other things in the game assets. Related fields provides additional clues of what
to be used. Check the [variant info](#variant-info) section for how the values are used.

## Usage

Asset: `AbilityData.json`

Each ability has at most 3 variants. Each variant contains the fields listed below.

### Variant Type

Each variant has exactly **one** type.

Field: `_AbilityTypeN`. For example, `_AbilityType1` or `_AbilityType2`.

### Variant ID

Each variant has at most 3 ID fields affiliated. `0` for not used.

Fields: `_VariousIdNa`, `_VariousIdNb` and `_VariousIdNc` for a single variant.

For example, `_VariousId1a` and `_VariousId1b` correspond to the 1st and the 2nd ID of the 1st variant.

### Variant String

Each variant has at most 1 string affiliated. Empty string `""` for not used.

Field: `_VariousIdNstr`. For example, `_VariousId1str` for the string affiliated of the 1st variant.

### Variant Limit Group

Each variant has at most 1 group ID affliated. `0` for not used.

Field: `_AbilityLimitedGroupIdN`. For example, `_AbilityLimitedGroupId1` for the 1st variant.

> This is used for limiting the value. Data correspondence of the ID can be found in `AbilityLimitedGroup.json`.

This is **only used** when up variant up value is given, for limiting the max value.

### Variant Target Action

Each variant has at most 1 target action ID affiliated. `0` for not used.

Field: `_TargetActionN`. For example, `_TargetAction1` for the 1st variant.

Check [the documentation for target action](/notes/enums/TargetAction.md) for more details.

# Variant Up Value

Each variant has at most 1 up value affiliated. `0.0` for not used. Note that different from others, this seems to
store a float number instead of an integer like the other numeric fields.

Field: `_AbilityTypeNUpValue`. For example, `_AbilityType1UpValue` for the 1st variant.

## Table

### Type enums

<pre>
00. None
<a href="#01---statusup">01. StatusUp</a>
<a href="#02---resistabs">02. ResistAbs</a>
03. ActAddAbs
04. ResistTribe
05. ActKillerTribe
<a href="#06---actdamageup">06. ActDamageUp</a>
<a href="#07---actcriticalup">07. ActCriticalUp</a>
<a href="#08---actrecoveryup">08. ActRecoveryUp</a>
<a href="#09---actbreakup">09. ActBreakUp</a>
10. ResistTrap
11. AddRecoverySp
12. AddRecoveryDp
13. RecoveryHpOnHitCount
<a href="#14---changestate">14. ChangeState</a>
15. ResistInstantDeath
16. DebuffGrantUp
<a href="#17---spcharge">17. SpCharge</a>
<a href="#18---buffextension">18. BuffExtension</a>
19. DebuffExtension
<a href="#20---abnormalkiller">20. AbnormalKiller</a>
<a href="#21---userexpup">21. UserExpUp</a>
22. CharaExpUp
23. CoinUp
24. ManaUp
<a href="#25---actiongrant">25. ActionGrant</a>
<a href="#26---criticaldamageup">26. CriticalDamageUp</a>
27. DpCharge
<a href="#28---resistelement">28. ResistElement</a>
29. ResistUnique
30. UniqueKiller
31. Dummy01
32. Dummy02
33. Dummy03
34. Dummy04
35. ModeGaugeSuppression
36. DragonDamageUp
37. EnemyAbilityKiller
38. HitAttribute
39. PassiveGrant
<a href="#40---activegaugestatusup">40. ActiveGaugeStatusUp</a>
41. Dummy05
42. HitAttributeShift
<a href="#43---referenceother">43. ReferenceOther</a>
<a href="#44---enhancedskill">44. EnhancedSkill</a>
45. EnhancedBurstAttack
46. DragonTimeForParty
47. AbnoramlExtension
48. DragonTimeSpeedRate
49. DpChargeMyParty
50. DontAct
51. RandomBuff
52. CriticalUpDependsOnBuffTypeCount
53. InvalidDragonAbility
<a href="#54---actdamageupdependsonhitcount">54. ActDamageUpDependsOnHitCount</a>
<a href="#55---chaintimeextension">55. ChainTimeExtension</a>
56. UniqueTransform
57. EnhancedElementDamage
58. UtpCharge
59. DebuffTimeExtensionForSpecificDebuffs
60. RemoveAllStockBullets
61. ChangeMode
62. RandomBuffNoTDuplicate_Param1Times
63. ModifyBuffDebuffDurationTime
64. CpCoef
65. UniqueAvoid
<a href="#66---rebornhprateup">66. RebornHpRateUp</a>
67. AttackBaseOnHPUpRate
68. ChangeStateHostile
69. CpContinuationDown
70. AddCpRate
</pre>

## Variant info

For the missing enums below, it means that the **documentation has not been created** yet, rather than fields not used.

If the fields are not explicitly mentioned (except for limit group ID), it means that the unmentioned fields are not
used.

-----

### `00` - `None`

The variant is not used.

-----

### `01` - `StatusUp`

Raise a certain status.

If ID-A is `2`; up value is `10`, then it means `ATK +10%`.

#### Variant ID - A

Parameter to be raised. Check [the documentation of the target parameter](/notes/enums/TargetParam.md)
for the ID correspondence.

A value of `2` means to raise ATK.

#### Variant Up Value

Parameter raising rate.

A value of `10` means to raise the parameter by 10%.

-----

### `02` - `ResistAbs`

Gives resistance toward a certain affliction status.

If ID-A is `6`; up value is `25`, then it means `Stun Resistance +25%`
(`6` corresponds to the affliction code of Stun).

#### Variant ID - A

Code of the affliction to resist. Check [the enum of the affliction statuses](/dlparse/enums/status.py)
for the ID correspondence.

A value of `6` means to resist Stun.

#### Variant Up Value

Probability rate of the affliction resistance in percentage.

A value of `50` means to resist a certain affliction by 50%.

-----

### `06` - `ActDamageUp`

Buff the target action damage. If the variant is inside an ex ability entry, the effect is team-wide.

#### Variant Target Action

Action to receive the damage boost.

For the number correspondance, check [the ability target action implementation.](/dlparse/enums/action.py)

#### Variant Up Value

Skill damage boost in percentage.

A value of `10` means SDMG +10%.

-----

### `07` - `ActCriticalUp`

Buff the character's CRT rate. If the variant is inside an ex ability entry, the effect is team-wide.

#### Variant Up Value

Critical rate boost in percentage.

A value of `10` means CRT +10%.

-----

### `08` - `ActRecoveryUp`

Buff the character's recovery potency of their skills. If the variant is inside an ex ability entry, the effect is
team-wide.

#### Variant Up Value

Recovery potency boost in percentage.

A value of `10` means RP +10%.

-----

### `09` - `ActBreakUp`

Buff the damage dealt toward the OD gauge. If the variant is inside an ex ability entry, the effect is team-wide.

#### Variant Up Value

Damage boost toward the OD gauge in percentage.

A value of `10` means OD gauge damage +10%.

-----

### `14` - `ChangeState`

Call the assigned items, which may be:

- Single action condition if given ID-A

- Multiple action conditions if given ID-A, ID-B and ID-C

  - This only happens for Dragon's Claws. ID-A, ID-B and ID-C will be called sequentially. Loopback to ID-A or not is
    unknown because `_MaxCount` is set to `3` for all variant type `14` with ID-A, ID-B and ID-C assigned, as of
    2020/01/19.

- Hit attribute if given in the string field

#### Variant ID - A

If ID-B and ID-C is not given, this is the action condition ID to be called.

If ID-B and ID-C is given, this is the 1st action condition ID to be called. Action condition of ID-B will be the next
one to be called.

A value of `888` means that to call the action condition ID `888` once the condition satifies.

#### Variant ID - B

Action condition ID to be called, after the action condition of ID-A is called, and the condition satisfies again.

A value of `889` means that to call the action condition ID `889` once the condition satifies, and the action condition
of ID-A is already called.

#### Variant ID - C

Action condition ID to be called, after the action condition of ID-B is called, and the condition satisfies again.

A value of `890` means that to call the action condition ID `890` once the condition satifies, and the action condition
of ID-B is already called.

#### Variant String

The hit attribute to be called (if given).

A value of `BUF_222_LV01` means that to call the hit attribute `BUF_222_LV01` once the condition satisifes.

-----

### `17` - `SpCharge`

Charge all SP gauges.

#### Variant Up Value

The percentage of the SP to charge for all skills.

A value of `100` means to charge all skills with 100% SP (immediately ready the skill).

-----

##### `18` - `BuffExtension`

Extend the buff effective time. If the variant is inside an ex ability entry, the effect is team-wide.

This only applies to the buffs that are directly applied to the user. Zoned buff like Gala Euden S1 (`10150403`) will
not be affected by this.

#### Variant Up Value

Buff extension ratio in percentage.

A value of `20` means to extend the buff time by 20%.

-----

### `20` - `AbnormalKiller`

Apply punisher damage boost if the target has the specific affliction status.

If `ID-A = 4`, `Up value = 8.0`, then if the damage will be boosted by 8% if the target is afflicted with paralysis
(actual example of Sharena (`10550404`) EX `120040008`).

#### Variant ID - A

Affliction status enum. For the ID correspondance, check [the implementation of the enum](/dlparse/enums/status.py).

#### Variant Up Value

Rate of the damage boost in percentage.

A value of `20` means damage boost 20%.

-----

### `21` - `UserExpUp`

Raise the player EXP gain upon clearing a quest.

#### Variant Up Value

The percentage of the player EXP gain.

A value of `10` means to gain additional 10% of the player EXP upon clearing a quest.

-----

### `25` - `ActionGrant`

Grant the user an action condition to a certain action.

#### Variant ID - A

ID of the action to grant. This ID links to the asset `ActionGrant`.

In this asset, the ID of the action condition ID, target action, and the duration is specified.

A value of `16` means to grant the effect listed in `ActionGrant` where ID is `16`.

- ID `16` in `ActionGrant` will allow the user's auto
  (`_TargetAction` = 1, corresponds to `Gluon.AbilityTargetAction`)
  to have the effect of action condition ID `1497`.

-----

### `26` - `CriticalDamageUp`

Buff the character's critical damage. If the variant is inside an ex ability entry, the effect is team-wide.

#### Variant Up Value

Critical damage boost rate in percentage.

A value of `20` means CRT DMG (CDMG) +20%.

-----

### `28` - `ResistElement`

Buff the character's damage resistance by the specified element.

If `ID-A = 1`, `Up value = 8`, then it means flame elemental damage resistance +8%.
(`1` in `ID-A` corresponds to flame)

#### Variant ID - A

Element of the damage resistance. Check [the implementation of the enum](/dlparse/enums/element.py) for the ID
corresponance.

#### Variant Up Value

Elemental damage resistance rate in percentage.

A value of `20` means damage resistance +20%.

-----

### `36` - `DragonDamageUp`

Buff the damage dealt by the dragon.

#### Variant Up Value

Dragon damage boost rate in percentage.

A value of `20` means dragon damage +20%.

-----

### `40` - `ActiveGaugeStatusUp`

Get the status up information according to the user gauge status.

> This actually appears (and only appears) on Gala Ranzal (`10150301`) as of 2020/12/11.

#### Variant ID - A, Variant ID - B

*Both are 1, but usage and meaning unknown.*

#### Variant String

Data of the DEF boost and the target action damage boost.

A value of `5_10/15_50` means:

Gauge(s) filled | DEF | Action Damage Boost
:---: | :---: | :---:
1 | +5% | +15%
2 | +10% | +50%

#### Variant Target Action

Action to receive the damage boost.

For the number correspondance, check [the ability target action implementation.](/dlparse/enums/action.py)

-----

### `42` - `HitAttributeShift`

Shift the hit attribute.

This does not have any parameters.

This is only used by Lathna passive 1 (`752` at level 3 of `10550502`)
and Gala Mym passive 1 (`237` at level 1 of `10550101` / `238` at level 2 of `10550101`), as of 2020/01/20.

This causes some "shifts" to the hit attributes (including autos and the skill) of the unique Mym (of Gala Mym) and the
unique Nyarlathotep (of Lathna), so these unique dragons are stronger.

-----

### `43` - `ReferenceOther`

Refer to the other ability.

#### Variant ID - A

The other ability ID. A value of `1307` means that there is an additional ability which ID is `1307`.

-----

### `44` - `EnhancedSkill`

Enhance a skill.

#### Variant ID - A

The skill ID to be used after the enhancement. A value of `106503036` means that the skill `106503036` will be used
after the enhancement.

#### Target Action ID

**Unsure for now.** This may means the skill to be enhanced.

For Menee (`10650303`), Enhanced S1 (`106503033`, available if 6+ butterflies exist on the map) have this as `3` while
Enhanced S2 (`106503036`, available if 6+ butterflies exist on the map) have this as `4`.

-----

### `54` - `ActDamageUpDependsOnHitCount`

Raise the damage depends on the user's hit count.

Check the doc of the variant string for more details.

> This actually appears on Mitsuhide S2 (`103504022`).

#### Variant String

Data of the damage boost.

A value of `5_5/10_10/15_20/20_30/25_40/30_50` means that:

- +5% damage if combo >= 5

- +10% damage if combo >= 10

- +20% damage if combo >= 15

- +30% damage if combo >= 20

- +40% damage if combo >= 25

- +50% damage if combo >= 30

The highest damage boost will be picked. For example, if the user's combo count is 27, then the damage boost is 40%.

-----

### `55` - `ChainTimeExtension`

Extend the valid time of the combo counter.

#### Variant Up Value

Time to extned in seconds.

A value of `2.5` means combo counter valid time +2.5 secs.

-----

### `57` - `EnhancedElementDamage`

Buff the elemental damage.

`ID-A = 4` with `Up Value = 20` means light elemental damage +20% (actual example of Peony EX - `157570408`).

#### Variant ID - A

Element enum. For the ID correspondance, check [the implementation of the enum](/dlparse/enums/element.py).

#### Variant Up Value

Rate of the damage boost in percentage.

A value of `20` means elemental damage +20%.

-----

### `66` - `RebornHpRateUp`

Recover an additional portion of the HP based on the healing receiver's max HP upon revival.

#### Variant Up Value

Rate of the additional healing based on the headling receiver's max HP upon revival in percentage.

A value of `10` means to gain additional 10% of the max HP upon revival.
