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

### Variant Limited Group

Each variant has at most 1 group ID affliated. `0` for not used.

Field: `_AbilityLimitedGroupIdN`. For example, `_AbilityLimitedGroupId1` for the 1st variant.

### Variant Target Action

Each variant has at most 1 target action ID affiliated. `0` for not used.

Field: `_TargetActionN`. For example, `_TargetAction1` for the 1st variant.

# Variant Up Value

Each variant has at most 1 up value affiliated. `0.0` for not used. Note that different from others, this seems to
store a float number instead of an integer like the other numeric fields.

Field: `_AbilityTypeNUpValue`. For example, `_AbilityType1UpValue` for the 1st variant.

## Table

### Type enums

<pre>
00. None
01. StatusUp
02. ResistAbs
03. ActAddAbs
04. ResistTribe
05. ActKillerTribe
06. ActDamageUp
07. ActCriticalUp
08. ActRecoveryUp
09. ActBreakUp
10. ResistTrap
11. AddRecoverySp
12. AddRecoveryDp
13. RecoveryHpOnHitCount
14. ChangeState
15. ResistInstantDeath
16. DebuffGrantUp
17. SpCharge
18. BuffExtension
19. DebuffExtension
20. AbnormalKiller
21. UserExpUp
22. CharaExpUp
23. CoinUp
24. ManaUp
25. ActionGrant
26. CriticalDamageUp
27. DpCharge
28. ResistElement
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
40. ActiveGaugeStatusUp
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
54. ActDamageUpDependsOnHitCount
55. ChainTimeExtension
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
66. RebornHpRateUp
67. AttackBaseOnHPUpRate
68. ChangeStateHostile
69. CpContinuationDown
70. AddCpRate
</pre>

## Variant info

For the missing enums below, it means that the **documentation has not been created** yet, rather than fields not used.

If the fields are not explicitly mentioned, it means that the unmentioned fields are not used.

### `43` - `ReferenceOther`

Refer to the other ability.

#### Variant ID - A

The other ability ID. A value of `1307` means that there is an additional ability which ID is `1307`.

### `44` - `EnhancedSkill`

Enhance a skill.

#### Variant ID - A

The skill ID to be used after the enhancement. A value of `106503036` means that the skill `106503036` will be used
after the enhancement.

#### Target Action ID

**Unsure for now.** This may means the skill to be enhanced.

For Menee (`10650303`), Enhanced S1 (`106503033`, available if 6+ butterflies exist on the map) have this as `3` while
Enhanced S2 (`106503036`, available if 6+ butterflies exist on the map) have this as `4`.