import pytest

from dlparse.enums import SkillConditionCategories, SkillConditionComposite
from dlparse.transformer import SkillTransformer


def test_s1(transformer_skill: SkillTransformer):
    # Original Amane S1
    # https://dragalialost.gamepedia.com/Amane
    skill_data_base = transformer_skill.transform_attacking(107404011)

    base_mods = [
        [7.182] * 2,
        [7.974] * 2,
        [8.856] * 2,
        [8.856] * 2
    ]
    per_buff_mods = [0, 0, 0, 1.05]
    per_buff_max = [0, 0, 0, 2]

    for buff_count in range(10):  # Arbitrarily chosen, should not give any errors
        buff_count_cond = SkillConditionCategories.self_buff_count.convert_reversed(buff_count)

        skill_data = skill_data_base.with_conditions(SkillConditionComposite(buff_count_cond))

        expected_hits = [len(mods_lv) + min(buff_count, per_buff_max[lv_idx])
                         for lv_idx, mods_lv in enumerate(base_mods)]
        expected_mods = [mods_lv + [per_buff_mods[lv_idx]] * min(buff_count, per_buff_max[lv_idx])
                         for lv_idx, mods_lv in enumerate(base_mods)]
        expected_total_mods = [sum(mods_lv) for mods_lv in expected_mods]

        assert skill_data.hit_count == expected_hits
        assert skill_data.hit_count_at_max == expected_hits[-1]
        assert skill_data.total_mod == pytest.approx(expected_total_mods)
        assert skill_data.total_mod_at_max == pytest.approx(expected_total_mods[-1])

        # Checking the mods distribution here is sufficient because the additional hits were dealt at the same time
        for actual_mods_lv, expected_mods_lv in zip(skill_data.mods, expected_mods):
            assert sorted(actual_mods_lv) == sorted(expected_mods_lv)
        assert sorted(skill_data.mods_at_max) == sorted(expected_mods[-1])

        assert skill_data.max_level == 4
