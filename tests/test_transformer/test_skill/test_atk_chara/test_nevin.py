from itertools import product

import pytest

from dlparse.enums import SkillCondition, SkillConditionComposite
from dlparse.transformer import SkillTransformer


def test_s2_locked(transformer_skill: SkillTransformer):
    # Nevin S2 @ Sigil locked
    # https://dragalialost.gamepedia.com/Nevin
    skill_data_base = transformer_skill.transform_attacking(103505042)

    # For some reason, the in-game data has sigil-locked and sigil-released variant
    # Both of these has condition data to limit it.

    # Base data
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [0, 0]
    assert skill_data.hit_count_at_max == 0
    assert skill_data.total_mod == pytest.approx([0, 0])
    assert skill_data.total_mod_at_max == pytest.approx(0)
    assert skill_data.mods == [[], []]
    assert skill_data.mods_at_max == []
    assert skill_data.max_level == 2

    # Sigil locked
    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.SELF_SIGIL_LOCKED))

    assert skill_data.hit_count == [1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == pytest.approx([9, 10])
    assert skill_data.total_mod_at_max == pytest.approx(10)
    assert skill_data.mods == [[9], [10]]
    assert skill_data.mods_at_max == [10]
    assert skill_data.max_level == 2

    # Sigil released (in the actual gameplay, sigil release changed the unit's mode, this variant won't be used)
    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.SELF_SIGIL_RELEASED))

    assert skill_data.hit_count == [1, 1]
    assert skill_data.hit_count_at_max == 1
    assert skill_data.total_mod == pytest.approx([9, 10])
    assert skill_data.total_mod_at_max == pytest.approx(10)
    assert skill_data.mods == [[9], [10]]
    assert skill_data.mods_at_max == [10]
    assert skill_data.max_level == 2


def test_s2_released(transformer_skill: SkillTransformer):
    # Nevin S2 @ Sigil released
    # https://dragalialost.gamepedia.com/Nevin
    skill_data_base = transformer_skill.transform_attacking(103505044)

    additional_mods_self = {
        SkillConditionComposite(): [
            [],
            []
        ],
        SkillConditionComposite(SkillCondition.SELF_IN_BUFF_ZONE_BY_SELF_1): [
            [2.7],
            [3]
        ],
        SkillConditionComposite(SkillCondition.SELF_IN_BUFF_ZONE_BY_SELF_2): [
            [2.7] * 2,
            [3] * 2
        ],
    }
    additional_mods_ally = {
        SkillConditionComposite(): [
            [],
            []
        ],
        SkillConditionComposite(SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_1): [
            [0.9],
            [1]
        ],
        SkillConditionComposite(SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_2): [
            [0.9] * 2,
            [1] * 2
        ],
        SkillConditionComposite(SkillCondition.SELF_IN_BUFF_ZONE_BY_ALLY_3): [
            [0.9] * 3,
            [1] * 3
        ],
    }

    for dmg_self_cond, dmg_ally_cond in product(additional_mods_self, additional_mods_ally):
        addl_dmg_self = additional_mods_self[dmg_self_cond]
        addl_dmg_ally = additional_mods_ally[dmg_ally_cond]

        skill_data = skill_data_base.with_conditions(dmg_self_cond + dmg_ally_cond)

        expected_hit_mtx = [hit_lv + len(self_lv) + len(ally_lv) for hit_lv, self_lv, ally_lv
                            in zip([1, 1], addl_dmg_self, addl_dmg_ally)]
        expected_total_mods = [hit_lv + sum(self_lv) + sum(ally_lv) for hit_lv, self_lv, ally_lv
                               in zip([9, 10], addl_dmg_self, addl_dmg_ally)]
        expected_mods_mtx = [hit_lv + self_lv + ally_lv for hit_lv, self_lv, ally_lv
                             in zip([[9], [10]], addl_dmg_self, addl_dmg_ally)]

        assert skill_data.hit_count == expected_hit_mtx
        assert skill_data.hit_count_at_max == expected_hit_mtx[-1]
        assert skill_data.total_mod == pytest.approx(expected_total_mods)
        assert skill_data.total_mod_at_max == pytest.approx(expected_total_mods[-1])

        # Checking the mods distribution here is sufficient because the additional hits were dealt at the same time
        for actual_mods_lv, expected_mods_lv in zip(skill_data.mods, expected_mods_mtx):
            assert sorted(actual_mods_lv) == sorted(expected_mods_lv)
        assert sorted(skill_data.mods_at_max) == sorted(expected_mods_mtx[-1])

        assert skill_data.max_level == 2
