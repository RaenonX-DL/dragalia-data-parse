# Notes on Player Action Components


## Attacking Components 

> Components that actually attacks the target.


### ``ActionPartsBullet``

Single attacking projectile of a skill.

A single component corresponds to a single attack.


### ``ActionPartsHit``

An attacking action that comes from the player of a skill.

A single component corresponds to a single attack.

#### Attribute notes

- Hit label = `CMN_AVOID` seems to mean invincible, which may appear for projectile attack (Euden S2 - `101401012`).


### ``ActionPartsPivotBullet``

Needs investigation. Should relate to ``ActionPartsBullet``.


## Active Components

> Components that users can actively trigger whenever it's possible.


### ``ActionPartsActiveCancel``

Needs investigation. Possibly active canceling action.

May be used for calculating camera duration.


## Effecting Components

> Components that are the side effects (affecting the gameplay) of the action.


### ``ActionPartsSettingHit``

Sets an area with some special effects. (Wedding Elisanne S1 / S2)

This does **not** deal damage.

#### Attribute notes

- `_lifetime` is the duration of the area.


## Camera Controlling Components

> Components that are related to the camera control / camera duration.


### ``ActionPartsCameraMotion``

Needs investigation. Could be just the camera movement.

May be used for calculating camera duration.


### ``ActionPartsHitStop``

Needs investigation. Frozen action after ``ActionPartsHit``.

May be used for calculating camera duration.


## Miscellaneous / Unknown

> Components that cannot be / have not been categorized.


### ``ActionPartsEffect``

Seems to be the skill effect.

May be used for calculating camera duration.


### ``ActionPartsMotion``

Needs investigation.

May be used for calculating camera duration.


### ``ActionPartsMoveTimeCurve``

Needs investigation. Possibly the variant of ``ActionPartsMotion`` but based on some other parameter, 
or the character movement curving function (could check Summer Julietta S1).

May be used for calculating camera duration.


### ``ActionPartsRotateTarget``

Needs investigation.


### ``ActionPartsSound``

SE of the action.


### ``ActionPartsSendSignal``

Needs investigation.
