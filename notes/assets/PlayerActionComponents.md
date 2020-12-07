# Player Action Components

## General

- `_seconds` is the action component execution starting time.

- `_duration` is the action component execution time length. This could be ``0``, which means that the execution is
  either momental, or the action flow is embedded somewhere.

## Attacking Components 

> Components that actually attacks the target.


### ``ActionPartsBullet``

Single attacking projectile of a skill.

A single component corresponds to a single attack.


### ``ActionPartsFireStockBullet``

Fire the same bullet multiple times.

#### Apperance notes

- Nefaria S1 (`106505011`)

- Yukata Curran S1 (`103504041` for unmasked, `103504043` for masked, with damage deterioration effect)

- Gala Sarisse S1 (`106501011`, AID `691030`)
  - `_fireStockPattern` = `2`
  - Max count 7

- Summer Cleo S1 Lv.1 ~ Lv.3 (`106504011`, AID `691070`)
  - `_fireStockPattern` = `2`
  - Max count 4

- Summer Cleo S1 Lv.4 (`106504011`, AID `691071`)
  - `_fireStockPattern` = `2`
  - Max count 5

- Chelle S2 (`106505032`, AID `691220`)
  - `_fireStockPattern` = `2`
  - Max count 8

- Amane S1 Lv.4 (`107404011`, AID `722003`)
  - `_fireStockPattern` = `2`
  - Max count 2

#### Attribute notes

- `_bulletNum`: count of bullets. This seems to use the same hit label (`_hitAttrLabel`).

- `_fireStockPattern`: Usage pattern of the bullets.

  - `2` means that the bullet will only fire according to the user buff count.
    If the user does not have any buff, the bullet will **not** fire.


### ``ActionPartsStockBullet``

Fire the bullet which is actually an action.

#### Apperance notes

- Gala Laxi S2 (Fig) (`103501022`)

#### Attribute notes

- `_autoFireActionId`: ID of the action to be fired.

- `_autoFireInterval`: Action firing interval in seconds.


### ``ActionPartsHit``

An attacking action that comes from the player of a skill.

A single component corresponds to a single attack.

#### Attribute notes

- Hit label = `CMN_AVOID` seems to mean invincible, which may appear for projectile attack (Euden S2 - `101401012`).


### ``ActionPartsPivotBullet``

Another type of bullets. Distinction unknown.

#### Appearance notes

- Wedding Aoi S1 (`103503011`)


### ``ActionPartsFormationBullet``

Another type of bullets. Distinction unknown.

#### Apperance notes

- Yukata Curran S2 Masked (`103504044`)

- OG!Zena S2 (`107505042`)

> Only these skills use this component. (as of 2020/11/23)


### ``ActionPartsMultiBullet``

Another type of bullets. Distinction unknown.

#### Apperance notes

- Bellina S1 Enhanced (`103505033`)


### ``ActionPartsParabolaBullet``

Another type of bullets. Distinction unknown.

#### Apperance notes

- Ilia S2 @ Alchemy (`103505033`)


### ``ActionPartsBuffFieldAttachment``

Add a damaging hit if according to the buff field count.

#### Apperance notes

- Nevin S2 @ Sigil Released (`103505044`)

#### Attribute notes

- `_isAttachToSelfBuffField`: if the counting toward the buff field that the user built.
  - `0` for the ally built
  - `1` for the self built  


### ``ActionSettingHit``

An action which sets an area.

#### Apperance notes

- Wedding Elisanne S1 (`101503021`)

## Active Components

> Components that users can actively trigger whenever it's possible.

### ``ActionPartsActiveCancel``

This cancels the action. Trigger this by tapping the screen.

#### Attribute notes

- `_seconds` is the actual starting time for the cancel to be allowed.

- `_actionId` is the specific action allowed to be used for the canceling.

  If this is given (not `0`), the given action needs to be executed in order to cancel the action.

  For example, if this is `110000`, commands that perform action ID `110000` is required.

  - `6` is common a common action ID meaning **dodge / roll**.


## Effecting Components

> Components that are the gameplay-affecting side effects of the action.


### ``ActionPartsSettingHit``

Sets an area with some special effects. (Wedding Elisanne S1 / S2)

This does **not** deal damage.

#### Attribute notes

- `_lifetime` is the duration of the area.

## Unit Action Controlling Components

> Components that are related to the action of the units.

### ``ActionPartsMotion``

Some motion connects to animation clip (by [Mushymato]).

#### Attribute notes

- `_motionState` **may** corresponds to some AnimationClip.

  This may be used for camera duration calculation.

  - `skill_A` takes exactly 1 second, which is commonly used for buffs.


### ``ActionPartsHitStop``

Needs investigation. Could be the frozen action after ``ActionPartsHit``.

May be used for calculating camera duration.

### ``ActionPartsHeadText``

Seems to be the texts appear above the head.

#### Apperance notes

- Karina S1 (`104402011`) for the text of **boost x N**.

## Miscellaneous / Unknown

> Components that cannot be / have not been categorized.

### ``ActionPartsEffect``

Seems to be the skill effect.


### ``ActionPartsMotion``

Unknown.


### ``ActionPartsMoveTimeCurve``

Unknown.


### ``ActionPartsRotateTarget``

Unknown.

### ``ActionPartsSound``

SE of the action.

### ``ActionPartsSendSignal``

Component used for communicating with the other components.


-----

## Additional Resources

- [Command Type Enum (from DL DPS sim by Mushymato)](https://github.com/dl-stuff/dl-datamine/blob/master/loader/Actions.py)

[Mushymato]: https://github.com/Mushymato
