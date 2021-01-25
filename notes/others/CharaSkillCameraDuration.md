# Character Skill Camera Duration

The process of finding the skill animation is as follows:

- Check for player active cancel action. If found, return it.

- Check the animation clip stop time.

## Active cancel action

Check for the component `ActionPartsActiveCancel` in the player action components.

## Animation Clip

The skill animations are controlled by `AnimatorController` and `AnimatorOverrideController`.

To get the stop time of an animation clip used by a skill, follow the steps below:

1. Obtain the motion state used by the action.

    - This can be found via `ActionPartsMotion._motionState` of each action.

    - Let's say we found that as `skill_unique_01_01`.

2. Get the `AnimatorController` used by the character who performs the action.

    - The desired `AnimatorController` will be named by the character's [weapon code](#weapon-code).

    - If the character who performs the action is a sword user, the `AnimatorController` will be named as `swd`.

3. Get the `AnimatorOverrideController` that overrides the action in the `AnimatorController`.

    - The desired `AnimatorOverrideController` will be named in the following format `WWW_BBBBBBVV`
      where `W` is the [weapon code](#weapon-code) like the previous step, `B` is the character base ID (`_BaseId`),
      and `V` is the character variation ID (`_VariationId`) padded with 0s.

    - If a character whose weapon is Sword, their base ID is `110337`, and their variation ID is `6`, the name of the
      desired `AnimatorOverrideController` will be `swd_11033706`.

4. Find the original animation clip of the motion state obtained at step 1 in the `AnimatorController` found in step 2.

    - The path ID of the original animation clip of a certain motion state can be obtained by the following steps:

    - Head to `m_TOS` of the `AnimatorController`.
      `Key` is the motion name, `Value` is the name ID of the corresponding motion state.

      Let's say an entry with `Key` as `skill_unique_01_01` and `Value` as `1234567890` is found.

    - Head to `m_Controller.m_StateMachineArray.[0].data.m_StateConstantArray`. Check each element for
      the `data.m_NameID` that matches the name ID obtained in the previous step.
      `m_BlendTreeConstantArray.[0].data.m_NodeArray.[0].data.m_ClipID` is the animation clip data index.

      Let's say an entry with `data.m_NameID` as `1234567890` and `...data.m_ClipID` as `3` is found.

    - Get the animation clip data at the index obtained in the previous step in `m_AnimationClips`.

      Note that the index we obtained is 0-based.

      The number with key `m_PathID` is the original animation clip path ID.

      Let's say an entry at index 3 has `-9876543210987654321` as `m_PathID` of the data.

5. Find the override animation clip of the motion state obtained at step 1 in the `AnimatorOverrideController` found in
   step 3 (if any).

    - If the animation clip overriding data is not found, then the action is using the original animation clip.

    - The path ID of the override animation clip can be obtained from `m_Clips`.

      In each element, the animation clip at path ID of `data.m_OverrideClip` will override the animation clip at path
      ID of `data.m_OriginalClip`.

    - If there's an animation clip at path ID `-9876543210987654321`, and an override data is found, which overrides
      this animation clip by the other animation clip at path ID `-1234567890123456789`, then the animation clip
      at `-1234567890123456789` is the one that is actually used for the motion `skill_unique_01_01`.

      Otherwise, the animation clip at path ID `-9876543210987654321` is used for the motion `skill_unique_01_01`.

6. Find the animation stop time in the corresponding animation clip.

    - The animation stop time is located at `m_MuscleClip.m_StopTime` in seconds.

The implementations of these steps can be found [here](/dlparse/mono/asset/motion).

------

# Appendix

### Weapon code

- `SWD`: Sword
- `KAT`: Blade (Katana)
- `DAG`: Dagger
- `AXE`: Axe
- `LAN`: Lance
- `BOW`: Bow
- `ROD`: Rod (Damaging Mage)
- `CAN`: Staff (Cane - Healing Mage)
- `GUN`: Manacaster (Gun)

### Credits

Thanks to [Mushymato] for providing hints for finding the exact pattern, and the data to validate the correctness.

[Mushymato]: https://github.com/Mushymato
