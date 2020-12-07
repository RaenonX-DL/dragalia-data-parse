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
08. GET_BUFF_DEF
09. TOTAL_HITCOUNT_MORE
10. TOTAL_HITCOUNT_LESS
11. KILL_ENEMY
12. TRANSFORM_DRAGON
13. HP_MORE_MOMENT
14. HP_LESS_MOMENT
15. QUEST_START
16. OVERDRIVE
17. ABNORMAL_STATUS
18. TENSION_MAX
19. TENSION_MAX_MOMENT
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
30. DAMAGED_ABNORMAL_STATUS
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
48. BUFFED_SPECIFIC_ID
49. DAMAGED
50. DEBUFF
51. RELEASE_DRAGONSHIFT
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

Check if the user's HP is > a certain threshold.

`Val 1 = 40` means that the condition holds if the user's HP is > 40%.

- **Val 1**: HP threshold.

### `37` - `HP_NOREACH`

Check if the user's HP is < a certain threshold.

`Val 1 = 40` means that the condition holds if the user's HP is < 40%.

- **Val 1**: HP threshold.

### `60` - `HP_MORE_NO_SUPPORT_CHARA`

Another branch of [`01. HP_MORE`](#01---hp_more).

However, this condition always fail if the unit is being used as a helper.

> Awaits confirmation. One known usage is Grace (`10850503`).
> The meaning of **no support** here can also mean "no shared skill" available.
> although it doesn't make sense that why this needs an individual condition type.

### `61` - `HP_NOREACH_NO_SUPPORT_CHARA`

Another branch of [`37. HP_NOREACH`](#37---hp_noreach). However, this condition always fail if the unit is being used
as a helper.

> Awaits confirmation. One known usage is Grace (`10850503`).
> The meaning of **no support** here can also mean "no shared skill" available,
> although it doesn't make sense that why this needs an individual condition type.

### `73` - `BUTTERFLYBULLET_NUM_OVER`

Check if the butterflies on the map is over a certain threshold.

`Val 1 = 6` means that the condition holds if the butterfly count is > 6.

- **Val 1**: Butterfly bullet count threshold.

#### Appearance

- Menee (`1302` from `1204` from ability 2 of CID `10650303`)
