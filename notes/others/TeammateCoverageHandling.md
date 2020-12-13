# Teammate Coverage Handling

This document records how the skills involving teammate coverage was handled in-game supposedly.

## Skills to be discussed

- Nadine S1 (`105501021`)

  > This skill deals additional damage according to the count of teammates covered.

- Summer Cleo S2 (`106504012`)

  > This skill grants additional buffs according to the count of teammates covered.

- Laranoa S2 (`106502012`)

  > This skill grants additional buffs according to the count of teammates covered.

- Chelle S1 (`106505031`)

  > This skill does **not** have any in-game effect according to the count of teammates covered.
  > However, this skill has a field that is only considered in the teammate coverage calculation set to `1`.

## Fields involved in teammate coverage calculation

### Player Hit Attribute Data (`PlayerActionHitAttribute.json`)

- `_IsAddCombo`: This will be set to `1` if the corresponding hit label should add a combo whenever the skill effect is
  effective.

  This is mainly used by Nadine S1 (`105501021`). Summer Cleo S2 (`106504012`) has this set to `1` to let the other
  teammate-coverage labels to be effective. Chelle S1 (`106505031`) also has this flag set to `1`, but the reason is
  unknown, since her skill does not care about hit counts.

  As a side note, despite Laranoa S2 (`106502012`) also has teammate coverage condition, she does not have this field
  set to `1`. Instead, she simply uses hit condition to handle that.

- `_HitConditionType`: This currently has a value of either `1` or `2`.

  Laranoa S2 (`106502012`) has this set to `1`.

  Nadine S1 (`105501021`), Summer Cleo S2 (`106504012`) and Chelle S1 (`106505031`) has this set to `2`.

  `1` means directly count the teammates covered;
  `2` means determine the effectiveness by the skill hit count. Check the introduction of each skill for more details.

- `_HitConditionP1`: The 1st parameter of the hit condition. Usually the lower inclusive bound of the hit count.

- `_HitConditionP2`: The 2nd parameter of the hit condition. Usually the upper inclusive bound of the hit count.

> Search for the field name in the code should bring you to the place parsing this field.
> Search for the reference of the parsed fields should give you more details about how this parser handles them.

## Nadine S1 (`105501021`)

This skill has an additional hit label `LAN_127_04_ALLY_LV01` for adding dummy hit count.

Then for each additional hit labels (`LAN_127_04_H02_1_LV01`, `LAN_127_04_H02_2_LV01` and `LAN_127_04_H02_3_LV01`)
according to the hit count, they will have `_HitConditionType` set to `2`; `_HitConditionP1` and `_HitConditionP2`
set to the bound of the hit count for the hit label to be effective.

For example, `LAN_127_04_H02_2_LV01` is only effective if there are 4 or 5 hits by the skill
(excluding the additional dummy hit count). In this case, field `_HitConditionType` is `2`; `_HitConditionP1`
and `_HitConditionP2` are `4`, `5`.

## Summer Cleo S2 (`106504012`)

This skill has `BOW_108_04_DEF_LV03` (DEF+) for 0 teammates covered,
`BOW_108_04_CRTDMG_LV03` (CDMG+) for 1 teammate covered and `BOW_108_04_SP_LV03` (S1 ready) for 2 teammates covered.

Each of these labels has `_HitConditionType` set to `2`, with the minimum teammate coverage count set
as `_HitConditionP1`, including the user themselves.

Additionally, `BOW_108_04_ATK_LV03` has `_IsAddCombo` set to `1`
to let the teammate coverage related labels effective.

The assumption here is that the addition of the dummy hit count by `BOW_108_04_ATK_LV03`
indirectly determines the effectiveness of the other teammate coverage related labels.

For example, `BOW_108_04_CRTDMG_LV03` has `_HitConditionP1` set to `2`, meaning that if 2 person (1 teammate) were
covered by the skill effect (the skill deals 2 hits internally), then `BOW_108_04_CRTDMG_LV03` is effective.

As Side note, Laranoa S2 (`106502012`) has a very similar mechanism in-game. However, `_IsAddCombo` of all the hit
labels are `0`.

## Laranoa S2 (`106502012`)

This skill has `BUF_138_DEF_LV03` for 0 teammates covered, `BUF_138_CRT_LV03` for 1 teammate covered and
`BUF_138_SP_LV03` for 2 teammates covered.

Each of these labels has `_HitConditionType` set to `1`, with the minimum teammate coverage count set
as `_HitConditionP1`, including the user themselves.

For example, `BUF_138_CRT_LV03` has `_HitConditionP1` set to `2`, meaning that if 2 person (1 teammate) were covered by
the skill effect, then `BUF_138_CRT_LV03` is effective.

The difference of game internal handling mechaism between Summer Cleo S2 (`106504012`) is that Summer Cleo determines
the effectiveness based on the internal skill hit count, whereas Laranoa S2 (`106502012`)
seems to directly calculate the count of teammates covered, i.e. determined by `_HitConditionType`.

## Chelle S1 (`106505031`)

Despite the skill (or the character) does not have any teammate coverage related skills or abilities, her S1
has `_IsAddCombo` set to `1`. The reason is *unknown*.
