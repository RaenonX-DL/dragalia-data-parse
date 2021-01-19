# Ability condtion enums

`AbilityCondition`

Condition for an ability to be effective.

## Usage

Asset: `AbilityData.json`

Field: `_ConditionType`

> There are 2 additional subfields `_ConditionValue` and `_ConditionValue2` for this.
> These fields will have non-zero values if the condition needs it.
>
> For the documentation of this, check the [value reference](#value-reference) section below.

## Table

<pre>
00. NONE
<a href="#01---hp_more">01. HP_MORE</a>
02. HP_LESS
03. BUFF_SKILL1
04. BUFF_SKILL2
05. DRAGON_MODE
06. BREAKDOWN
07. GET_BUFF_ATK
<a href="#08---get_buff_def">08. GET_BUFF_DEF</a>
09. TOTAL_HITCOUNT_MORE
10. TOTAL_HITCOUNT_LESS
11. KILL_ENEMY
12. TRANSFORM_DRAGON
13. HP_MORE_MOMENT
14. HP_LESS_MOMENT
<a href="#15---quest_start">15. QUEST_START</a>
16. OVERDRIVE
17. ABNORMAL_STATUS
<a href="#18---tension_max">18. TENSION_MAX</a>
<a href="#19---tension_max_moment">19. TENSION_MAX_MOMENT</a>
20. DEBUFF_SLIP_HP
21. HITCOUNT_MOMENT
22. GET_HEAL_SKILL
23. SP1_OVER
24. SP1_UNDER
25. SP1_LESS
26. SP2_OVER
27. SP2_UNDER
28. SP2_LESS
29. CAUSE_ABNORMAL_STATUS
<a href="#30---damaged_abnormal_status">30. DAMAGED_ABNORMAL_STATUS</a>
31. DRAGONSHIFT_MOMENT
32. PARTY_ALIVE_NUM_OVER
33. PARTY_ALIVE_NUM_UNDER
34. TENSION_LV
35. TENSION_LV_MOMENT
36. GET_BUFF_TENSION
<a href="#37---hp_noreach">37. HP_NOREACH</a>
38. HP_NOREACH_MOMENT
39. SKILLCONNECT_SKILL1_MOMENT
40. SKILLCONNECT_SKILL2_MOMENT
41. DRAGON_MODE2
42. CAUSE_DEBUFF_ATK
43. CAUSE_DEBUFF_DEF
44. CHANGE_BUFF_TYPE_COUNT
45. CAUSE_CRITICAL
46. TAKE_DAMAGE_REACTION
47. NO_DAMAGE_REACTION_TIME
<a href="#48---buffed_specific_id">48. BUFFED_SPECIFIC_ID</a>
49. DAMAGED
50. DEBUFF
<a href="#51---release_dragonshift">51. RELEASE_DRAGONSHIFT</a>
52. UNIQUE_TRANS_MODE
53. DAMAGED_MYSELF
54. SP1_MORE_MOMENT
55. SP1_UNDER_MOMENT
56. SP2_MORE_MOMENT
57. SP2_UNDER_MOMENT
58. HP_MORE_NOT_EQ_MOMENT
59. HP_LESS_NOT_EQ_MOMENT
<a href="#60---hp_more_no_support_chara">60. HP_MORE_NO_SUPPORT_CHARA</a>
<a href="#61---hp_noreach_no_support_chara">61. HP_NOREACH_NO_SUPPORT_CHARA</a>
62. CP1_CONDITION
63. CP2_CONDITION
64. REQUIRED_BUFF_AND_SP1_MORE
65. REQUIRED_BUFF_AND_SP2_MORE
66. ENEMY_HP_MORE
67. ENEMY_HP_LESS
68. ALWAYS_REACTION_TIME
69. ON_ABNORMAL_STATUS_RESISTED
70. BUFF_DISAPPEARED
71. BUFFED_SPECIFIC_ID_COUNT
72. CHARGE_LOOP_REACTION_TIME
<a href="#73---butterflybullet_num_over">73. BUTTERFLYBULLET_NUM_OVER</a>
74. AVOID
75. CAUSE_DEBUFF_SLIP_HP
76. CP1_OVER
77. CP2_OVER
78. CP1_UNDER
79. CP2_UNDER
80. BUFF_COUNT_MORE_THAN
81. BUFF_CONSUMED
82. HP_BETWEEN
83. DAMAGED_WITHOUT_MYSELF
84. BURST_ATTACK_REGULAR_INTERVAL
85. BURST_ATTACK_FINISHED
86. REBORN_COUNT_LESS_MOMENT
87. DISPEL_SUCCEEDED
88. ON_BUFF_FIELD
89. ENTER_EXIT_BUFF_FIELD
90. GET_DP
91. GET_BUFF_FOR_PD_LINK
92. GET_HEAL
</pre>

## Value Reference

If the enum is not specified below, it means **no documentation** has been created yet, rather than condition values
not used.

Missing value(s) means that the corresponding value is not used.

### `01` - `HP_MORE`

Effective if the user's HP is >= a certain threshold.

`Val 1 = 40` means that the condition holds if the user's HP is >= 40%.

- **Val 1**: HP threshold.

### `08` - `GET_BUFF_DEF`

Triggered once when the user receives a buff.

### `15` - `QUEST_START`

Triggered once at the beginning of the quest.

### `18` - `TENSION_MAX`

Effective if the user **is** energized.

Note that the effect will be effective as long as the user is energized. This is different
from [`19. TENSION_MAX_MOMENT`](#19---tension_max_moment), which only triggers when the user got energized.

### `19` - `TENSION_MAX_MOMENT`

Triggered once when the user **got** energized.

Note that the effect will be granted once the user got energized. This is different
from [`18. TENSION_MAX`](#18---tension_max), which effects will be effective as long as the user is energized.

> This is only used by Nadine (`10550102`) as of 2020/12/12.

- **Val 1**: *Used but meaning unknown. Could be the count of effects to grant.*

  For all usages as of 2020/12/12, this only has a value of `1`.

### `30` - `DAMAGED_ABNORMAL_STATUS`

Triggered once when the user is hit by an attack with the specified affliction status.

`Val 1 = 6` means that the ability will be triggered once the user is hit by an attack that stuns the target.

- **Val 1**: Enum number of the affliction status to trigger this condition.
  Check [the enum of the affliction statuses](/dlparse/enums/status.py) for the ID correspondence.

### `37` - `HP_NOREACH`

Effective if the user's HP is < a certain threshold.

`Val 1 = 40` means that the condition holds if the user's HP is < 40%.

- **Val 1**: HP threshold.

### `48` - `BUFFED_SPECIFIC_ID`

Effective if the user has a certain buff.

`Val 1 = 977` means that the user needs to have the action condition ID `977` for making the ability effective.

If both `val 1` and `val 2` are specified, the user needs to have them **BOTH**. Otherwise, ``val 2`` will be set
to ``0`` meaning that the field is not in use.

- **Val 1**: action condition ID of the required buff.

- **Val 2**: secondary action condition ID of the required buff. `0` means ineffective.

### `51` - `RELEASE_DRAGONSHIFT`

Triggered once when the user completed shapeshifting.

### `60` - `HP_MORE_NO_SUPPORT_CHARA`

Another branch of [`01. HP_MORE`](#01---hp_more).

However, this condition always fail if the unit is being used as a helper.

> Awaits confirmation. One known usage is Grace (`10850503`).
> The meaning of **no support** here can also mean "no shared skill" available.
> although it doesn't make sense that why this needs an individual condition type.

### `61` - `HP_NOREACH_NO_SUPPORT_CHARA`

Another branch of [`37. HP_NOREACH`](#37---hp_noreach).

However, this condition always fail if the unit is being used as a helper.

> Awaits confirmation. One known usage is Grace (`10850503`).
> The meaning of **no support** here can also mean "no shared skill" available,
> although it doesn't make sense that why this needs an individual condition type.

### `73` - `BUTTERFLYBULLET_NUM_OVER`

Effective if the butterflies on the map is over a certain threshold.

`Val 1 = 6` means that the condition holds if the butterfly count is > 6.

- **Val 1**: Butterfly bullet count threshold.

#### Appearance

- Menee (`1302` from `1204` from ability 2 of CID `10650303`)
