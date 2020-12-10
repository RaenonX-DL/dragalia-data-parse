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
<a href="#01---action_condition">01. ACTION_CONDITION</a>
<a href="#06---action_cancel">06. ACTION_CANCEL</a>
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

### `01` - `ACTION_CONDITION`

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
