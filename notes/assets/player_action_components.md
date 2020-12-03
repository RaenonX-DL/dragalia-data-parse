# Notes on Player Action Components


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

#### Attribute notes

- `_bulletNum`: count of bullets. This seems to share the same hit label (`_hitAttrLabel`).


### ``ActionPartsStockBullet``

Fire the bullet which is actually an action.

#### Apperance notes

- Gala Laxi (`103501022`) 

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


### ``ActionPartsHeadText``

Seems to be the texts appear above the head.

This appears in Karina S1 (`104402011`), which could be the text of **boost x N**.


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

-----

## Additional Resources

- [Command Type Enum (from DL DPS sim by Mushymato)](https://github.com/dl-stuff/dl-datamine/blob/master/loader/Actions.py)
