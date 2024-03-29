# Ability condtion enums

`AbilityCondition`

Condition for an ability to be effective.

## Usage

Asset: `AbilityData.json`

Field: `_ConditionType`

> There are 3 additional subfields: `_ConditionValue`, `_ConditionValue2`, and `_TargetAction` for this.
> These fields will have non-zero values if the condition requires it.
>
> For the documentation of this, check the [value reference](#value-reference) section below.

## Table

<pre>
00. NONE
<a href="#01---hp_more">01. HP_MORE</a>
<a href="#02---hp_less">02. HP_LESS</a>
03. BUFF_SKILL1
04. BUFF_SKILL2
<a href="#05---dragon_mode">05. DRAGON_MODE</a>
06. BREAKDOWN
07. GET_BUFF_ATK
<a href="#08---get_buff_def">08. GET_BUFF_DEF</a>
<a href="#09---total_hitcount_more">09. TOTAL_HITCOUNT_MORE</a>
10. TOTAL_HITCOUNT_LESS
11. KILL_ENEMY
<a href="#12---transform_dragon">12. TRANSFORM_DRAGON</a>
<a href="#13---hp_more_moment">13. HP_MORE_MOMENT</a>
<a href="#14---hp_less_moment">14. HP_LESS_MOMENT</a>
<a href="#15---quest_start">15. QUEST_START</a>
<a href="#16---overdrive">16. OVERDRIVE</a>
17. ABNORMAL_STATUS
<a href="#18---tension_max">18. TENSION_MAX</a>
<a href="#19---tension_max_moment">19. TENSION_MAX_MOMENT</a>
20. DEBUFF_SLIP_HP
<a href="#21---hitcount_moment">21. HITCOUNT_MOMENT</a>
22. GET_HEAL_SKILL
23. SP1_OVER
24. SP1_UNDER
<a href="#25---sp1_less">25. SP1_LESS</a>
26. SP2_OVER
27. SP2_UNDER
<a href="#28---sp2_less">28. SP2_LESS</a>
<a href="#29---cause_abnormal_status">29. CAUSE_ABNORMAL_STATUS</a>
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
<a href="#43---cause_debuff_def">43. CAUSE_DEBUFF_DEF</a>
44. CHANGE_BUFF_TYPE_COUNT
45. CAUSE_CRITICAL
46. TAKE_DAMAGE_REACTION
47. NO_DAMAGE_REACTION_TIME
<a href="#48---buffed_specific_id">48. BUFFED_SPECIFIC_ID</a>
<a href="#49---damaged">49. DAMAGED</a>
<a href="#50---debuff">50. DEBUFF</a>
<a href="#51---release_dragonshift">51. RELEASE_DRAGONSHIFT</a>
52. UNIQUE_TRANS_MODE
53. DAMAGED_MYSELF
54. SP1_MORE_MOMENT
55. SP1_UNDER_MOMENT
56. SP2_MORE_MOMENT
57. SP2_UNDER_MOMENT
<a href="#58---hp_more_not_eq_moment">58. HP_MORE_NOT_EQ_MOMENT</a>
<a href="#59---hp_less_not_eq_moment">59. HP_LESS_NOT_EQ_MOMENT</a>
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
<a href="#88---on_buff_field">88. ON_BUFF_FIELD</a>
89. ENTER_EXIT_BUFF_FIELD
90. GET_DP
91. GET_BUFF_FOR_PD_LINK
<a href="#92---get_heal">92. GET_HEAL</a>
93. CHARGE_TIME_MORE_MOMENT
94. EVERY_TIME_HIT_OCCURS
<a href="#95---hitcount_moment_timesrate">95. HITCOUNT_MOMENT_TIMESRATE</a>
<a href="#96---just_avoid">96. JUST_AVOID</a>
97. GET_BRITEM
98. DUP_BUFF_ALWAYS_TIMESRATE
99. BUFFED_SPECIFIC_ID_COUNT_MORE_ALWAYS_CHECK
100. GET_BUFF_FROM_SKILL
101. HP_RECOVERED_BETWEEN
102. RELEASE_DIVINEDRAGONSHIFT
103. HAS_AURA_TYPE
104. SELF_AURA_LEVEL_MORE
105. PARTY_AURA_LEVEL_MORE
106. DRAGONSHIFT
107. DRAGON_MODE_STRICTLY
</pre>

## Value Reference

If the enum is not specified below, it means **no documentation** has been created yet, rather than condition values
not used.

Missing value(s) means that the corresponding value is not used.

-----

### `01` - `HP_MORE`

Effective if the user's HP is greater than a certain threshold.

`Val 1 = 40` means that the ability is effective if the user's HP is > 40%.

- **Val 1**: HP threshold.

-----

### `02` - `HP_LESS`

Triggered once when the user's HP drops below a certain threshold.

`Val 1 = 40` means that the ability will be triggered upon the user's HP < 40%.

> Despite that `01. HP_MORE` is effective instead of triggering, Grace (`10850503`) CEX (`400000657`),
> which is using this condition, is triggered upon HP drops below a certain threshold, instead of effective.

- **Val 1**: HP threshold.

-----

### `05` - `DRAGON_MODE`

Effective if the user is in dragon shape. Certain shapeshift count is also required if `Val 1` is set.

`Val 1 = 2` means that the ability is effective if the user has been shapeshifted for 2 times or more, including the
current shapeshifting action.

Note that `Val 1` can be `0`, which means that the shapeshift count doesn't matter. The ability is always active.

- **Val 1**: Minimum dragon transform count required.

-----

### `08` - `GET_BUFF_DEF`

Triggered once when the user receives a buff.

-----

### `09` - `TOTAL_HITCOUNT_MORE`

Triggered once when the user's combo count goes beyond or equal to the designated combo count.

`Val 1 = 20` means that the ability will be triggered upon the user's combo count goes beyond 20.

- **Val 1**: Minimum combo count required.

-----

### `10` - `TOTAL_HITCOUNT_LESS`

Triggered once when the user's combo count drops below the designated combo count.

`Val 1 = 20` means that the ability will be triggered upon the user's combo count drops below 20.

- **Val 1**: Combo count threshold to trigger the ability.

  - Usually all values are applicable, since combo counter is directly set to `0` upon expired.

-----

### `12` - `TRANSFORM_DRAGON`

Triggered once when the user shapeshifts and has been shapeshifted for a certain amount of times, including the one
that triggers this.

`Val 1 = 2` means that the ability will be triggered once the user shapeshifted and already shapeshifted twice,
including the one that triggers this.

- **Val 1**: Amount of dragon transformed.

  - As of 2021/01/19, all abilities only have this as `1`.

-----

### `13` - `HP_MORE_MOMENT`

Triggered once when the user's HP goes beyond a certain threshold.

`Val 1 = 30` means that the ability will be triggered once when the user's HP is > 30%.

- **Val 1**: HP threshold.

-----

### `14` - `HP_LESS_MOMENT`

Triggered once when the user's HP drops under a certain threshold.

`Val 1 = 30` means that the ability will be triggered once when the user's HP drops < 30%.

- **Val 1**: HP threshold.

-----

### `15` - `QUEST_START`

Triggered once at the beginning of the quest.

-----

### `16` - `OVERDRIVE`

Effective if the target is in Overdrive state.

-----

### `18` - `TENSION_MAX`

Effective if the user **is** energized.

Note that the effect will be effective as long as the user is energized. This is different
from [`19. TENSION_MAX_MOMENT`](#19---tension_max_moment), which only triggers when the user got energized.

-----

### `19` - `TENSION_MAX_MOMENT`

Triggered once when the user **got** energized.

Note that the effect will be granted once the user got energized. This is different
from [`18. TENSION_MAX`](#18---tension_max), which effects will be effective as long as the user is energized.

> This is only used by Nadine (`10550102`) as of 2020/12/12.

- **Val 1**: *Used but meaning unknown. Could be the count of effects to grant.*

  For all usages as of 2020/12/12, this only has a value of `1`.

-----

### `21` - `HITCOUNT_MOMENT`

Triggered once for every X combo, where X is a designated number of combo count.

`Val 1 = 20` means that the ability will be triggered once for every 20 combo.

- **Val 1**: Combo count base number to trigger the ability.
- **Target Action**: The combo count only count from this action.

-----

### `25` - `SP1_LESS`

Effective if the SP of S1 is less than a certain %.

`Val 1 = 20` means that the ability will be effective if S1 SP% is less than 20.

- **Val 1**: SP % for the ability to be effective.

-----

### `28` - `SP2_LESS`

Effective if the SP of S2 is less than a certain %.

`Val 1 = 20` means that the ability will be effective if S2 SP% is less than 20.

- **Val 1**: SP % for the ability to be effective.

-----

### `29` - `CAUSE_ABNORMAL_STATUS`

Triggered once when the user successfully inflicted a certain affliction status.

`Val 1 = 2` means that the ability will be triggered once when the user successfully burned the target (`2` is the enum
value of burn).

- **Val 1**: Enum value of the affliction status to trigger.
  Check [the implementation of the enum](/dlparse/enums/status.py) for the correspondence.

-----

### `30` - `DAMAGED_ABNORMAL_STATUS`

Triggered once when the user is hit by an attack with the specified affliction status.

`Val 1 = 6` means that the ability will be triggered once the user is hit by an attack that stuns the target.

- **Val 1**: Enum number of the affliction status to trigger this condition.
  Check [the enum of the affliction statuses](/dlparse/enums/status.py) for the ID correspondence.

-----

### `31` - `DRAGONSHIFT_MOMENT`

Triggered once when the user shapeshifts and has been shapeshifted for a certain amount of times, including the one
that triggers this.

`Val 1 = 2` means that the ability will be triggered once the user shapeshifted and already shapeshifted twice,
including the one that triggers this.

- **Val 1**: Amount of dragon transformed.

-----

### `36` - `GET_BUFF_TENSION`

Triggered once when the user's energy level is increased, regardless how many level it is.

-----

### `37` - `HP_NOREACH`

Effective if the user's HP is < a certain threshold.

`Val 1 = 40` means that the condition holds if the user's HP is < 40%.

- **Val 1**: HP threshold.

-----

### `43` - `CAUSE_DEBUFF_DEF`

Triggered once when the user successfully debuffed the enemy with DEF down.

-----

### `48` - `BUFFED_SPECIFIC_ID`

Effective if the user has a certain buff.

`Val 1 = 977` means that the user needs to have the action condition ID `977` for making the ability effective.

If both `val 1` and `val 2` are specified, the user needs to have them **BOTH**. Otherwise, ``val 2`` will be set
to ``0`` meaning that the field is not in use.

- **Val 1**: action condition ID of the required buff.

- **Val 2**: secondary action condition ID of the required buff. `0` means ineffective.

-----

### `49` - `DAMAGED`

Triggered once when the user got hit.

-----

### `50` - `DEBUFF`

Effective if the enemy is in a certain type of the debuff.

`Val 1 = 3` means that the ability is effective if the enemy DEF is debuffed.

- `3` corresponds to ``ActionDefDebuff.Defense``.

- **Val 1**: Type of the debuff. For the ID correspondence,
  check [the implementation of the enum.](/dlparse/enums/action_debuff_type.py)

-----

### `51` - `RELEASE_DRAGONSHIFT`

Triggered once when the user completed shapeshifting.

-----

### `58` - `HP_MORE_NOT_EQ_MOMENT`

Triggered once when the user's HP goes beyond or equal to a certain threshold.

`Val 1 = 30` means that the ability will be triggered once when the user's HP is >= 30%.

- **Val 1**: HP threshold.

-----

### `59` - `HP_LESS_NOT_EQ_MOMENT`

Triggered once when the user's HP drops under or equal to a certain threshold.

`Val 1 = 30` means that the ability will be triggered once when the user's HP is <= 30%.

- **Val 1**: HP threshold.

-----

### `60` - `HP_MORE_NO_SUPPORT_CHARA`

Another branch of [`01. HP_MORE`](#01---hp_more).

However, this condition always fail if the unit is being used as a helper.

> Awaits confirmation. One known usage is Grace (`10850503`).
> The meaning of **no support** here can also mean "no shared skill" available.
> although it doesn't make sense that why this needs an individual condition type.

-----

### `61` - `HP_NOREACH_NO_SUPPORT_CHARA`

Another branch of [`37. HP_NOREACH`](#37---hp_noreach).

However, this condition always fail if the unit is being used as a helper.

> Awaits confirmation. One known usage is Grace (`10850503`).
> The meaning of **no support** here can also mean "no shared skill" available,
> although it doesn't make sense that why this needs an individual condition type.

-----

### `73` - `BUTTERFLYBULLET_NUM_OVER`

Effective if the butterflies on the map is over a certain threshold.

`Val 1 = 6` means that the condition holds if the butterfly count is > 6.

- **Val 1**: Butterfly bullet count threshold.

#### Appearance

- Menee (`1302` from `1204` from ability 2 of CID `10650303`)

-----

### `88` - `ON_BUFF_FIELD`

Effective if the user is inside a buff field.

- **Val 1**: *Used but meaning unknown. Could be the minimum count of the buff fields.*

  For all usages as of 2021/01/23, this only has a value of `1`.

- **Val 2**: *Used but meaning unknown. Could be the maximum count of the buff fields.*

  For all usages as of 2021/01/23, this only has a value of either `1` or `2`.

-----

### `92` - `GET_HEAL`

Triggered once when the user got healed.

### `92` - `GET_HEAL`

Triggered once when the user got healed.

-----

### `95` - `HITCOUNT_MOMENT_TIMESRATE`

Triggered once for every X combo with a limited count. X is a designated number of combo count.

If `Val 1 = 10`, `Val 2 = 20`, then it means that the ability will be triggered once for every 10 combo, with a limit
of 20 times. (actual example of Kimono Elisanne `10550103` chained EX `400000838`)

- **Val 1**: Combo count base number to trigger the ability.

- **Val 2**: Maximum count of effects allowed.

-----

### `95` - `HITCOUNT_MOMENT_TIMESRATE`

Triggered once for every X combo with a limited count of stacks. X is a designated number of combo count.

If `Val 1 = 10`, `Val 2 = 20`, then it means that the ability will be triggered once for every 10 combo, with a limit
of 20 times. (actual example of Kimono Elisanne `10550103` chained EX `400000838`)

- **Val 1**: Combo count base number to trigger the ability.

- **Val 2**: Maximum stacks of effects allowed.

-----

### `96` - `JUST_AVOID`

Triggered once the user successfully dodged a red attack.

-----

### `103` - `HAS_AURA_TYPE`

Effective if the user has a certain type of amp.

As of 2021/04/17, the only known appearances are Myriam (EXID `400000906`, CID `10750303`)
and Child Ranzal (EXID `400000912`, CID `10450103`). Both of them have both of the values set to `2`

- **Val 1**: (Unknown)

- **Val 2**: (Unknown)

-----

### `105` - `PARTY_AURA_LEVEL_MORE`

Effective if the user's team amp is up.

The usage of the values is unknown.

As of 2021/04/17, the only appearance is Humanoid Mercury (EXID `400000922`, CID `10350204`). Her chained co-ab
description did not mention the level threshold, while its values are set as follows: Val 1 = `2`; Val 2 = `1`.

> It might mean team amp (val 1 = `2`) level 1 (val 2 = `1`).

- **Val 1**: (Unknown)

- **Val 2**: (Unknown)
