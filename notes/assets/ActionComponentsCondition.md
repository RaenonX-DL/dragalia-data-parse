# Player Action Component Condition Type

Condition for an action component to be effective.

## Usage

Asset: Each player action data, `PlayerAction_NNNNNNNN.json`
where NNNNNNNN is an 8-digit number representing the player action ID.

Field: `_conditionData._ConditionType`

> For each `_conditionData._conditionValue`, there are also 4 additional places
> to store the numbers (parameters). Check the [additional info](#additional-info)
> section for more details.

## Table

<pre>
<a href="#00---none">00. NONE</a>
<a href="#01---action_condition_count">01. ACTION_CONDITION_COUNT</a>
<a href="#06---action_cancel">06. ACTION_CANCEL</a>
<a href="#07---seimei_shikigami_level">07. SEIMEI_SHIKIGAMI_LEVEL</a>
</pre>

> If the number is missing, it just means that the usage has not been found or identified.

## Additional Info

Each `_conditionData._conditionValue` has 4 slots. They will be mentioned as value 0, value 1, value 2 and value 3
below.

For the values that are not being mentioned, it just means that the usage of that slot has not been classified. If a
slot is identified to be unused, it will be explicitly mentioned.

### `00` - `NONE`

The action component is always effective.

#### Value 0~3

*Not used.*

### `01` - `ACTION_CONDITION_COUNT`

The action component is effective only if the user has certain instances of the action condition.

For example, value 0 = `1152` and value 2 = `1` means that the action component is effective only if the user has one
instance (> or = unknown) of action condition ID `1152`.

> This is a real-life example of Nevin S2 (SID `103505042`, AID `391330`).

#### Value 0

Action condition ID to check.

#### Value 2

Instance count of the action condition ID.

### `06` - `ACTION_CANCEL`

The action component is effective only if the action is used to cancel the other action.

For example, value 0 = `991070` means that the action component is effective only if the action containing this action
component (AID `991060`, **NOT** the action component) is used to cancel the action `991070`.

> This is a real-life example of Formal Joachim S1 (SID `109503011`, AID `991060`).

#### Value 0

The action ID being canceled.

### `07` - `SEIMEI_SHIKIGAMI_LEVEL`

The action component effectiveness depends on Seimei's Shikigami level.

For example, value 0 = `0` and value 1 = `2` means that the action component is effective only if the shikigami level
is `2`.

There are only 2 known cases for Seimei S2 (SID `107501042`, AID `791270`) as of 2021/01/08:

- `[5, 1, 0, 0]`: Effective only if the Shikigami is less than or equal to level 1.
    - Note that despite the operator used is `<=`, the skill needs the Shikigami up. Therefore, this can be considered
      as Shikigami **is** level 1.

- `[0, 2, 0, 0]`: Effective only if the Shikigami is level 2.

> This is only used by Seimei S2 (SID `107501042`, AID `791270` as of 2021/01/08).

#### Value 0

Comparison operator.

- `0`: `=`
- `5`: `<=`

> Check `Assembly-CSharp/Gluon/ActionData/ActionParts.cs`
> of [`RaenonX-DL/dragalia-decompile`](https://github.com/RaenonX-DL/dragalia-decompile) for more details.

#### Value 1

Comparator of the Seimei's Shikigami level.
