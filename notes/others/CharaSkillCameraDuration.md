# Character Skill Camera Duration

The process of finding the skill animation is as follows:

- Check for player active cancel action. If found, return it.

- Check the animation clip.

## Active cancel action

Check for the component `ActionPartsActiveCancel` in the player action components.

## Animation Clip

Check for the animation clip name named as:

```
WWW_SKL_MMMMM_BBBBBBVV
```

where:

- `W`: Weapon code.
    - `SWD`: Sword
    - `KAT`: Katana
    - `DAG`: Dagger
    - `AXE`: Axe
    - `LAN`: Lance
    - `BOW`: Bow
    - `ROD`: Rod (Damaging Mage)
    - `CAN`: Cane (Healing Mage)
    - `GUN`: Gun

- `SKL`: Seems to be the constant to denote the skill animation clip.

- `M`: Motion name. The name length varies, although commonly seen as `01_01`. This can be extracted from the
  field `_motionState` of the action component `ActionPartsMotion`. A commonly seen value of `_motionState`
  is `skill_unique_01_01`. In this case, the motion name is `01_01`.

- `B`: Character base ID. This is a 6-digit number. This can be found in the character data.

- `V`: Character variation ID. This should be a 2-digit number. If the ID is a single-digit number, pad it to 2 digits.
  This can be found in the character data.

## Known issues

- There are a thing named `AnimationController` that actually handle this (by [Mushymato]).

- There are some skills failed to match using this stepflow (by [Mushymato]):
    - Gala Mym - S2
    - Megaman - All skills

[Mushymato]: https://github.com/Mushymato
