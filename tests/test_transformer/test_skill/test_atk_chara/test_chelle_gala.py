import pytest

from dlparse.enums import ConditionCategories, ConditionComposite
from dlparse.transformer import SkillTransformer


def test_s1(transformer_skill: SkillTransformer):
    # Gala Chelle
    # https://dragalialost.wiki/w/Gala_Chelle
    skill_data_base = transformer_skill.transform_attacking(109505011)

    base_mods = [
        [9.52] + [0.65] * 11,
        [10.58] + [0.72] * 11,
        [11.75] + [0.8] * 11
    ]
    per_buff_mods = [0.2, 0.23, 0.25]
    per_buff_max = [15, 15, 15]

    for condition in sorted(ConditionCategories.self_buff_count.members):
        buff_count = ConditionCategories.self_buff_count.convert(condition)

        skill_data = skill_data_base.with_conditions(ConditionComposite(condition))

        expected_hits = [
            len(mods_lv) + min(buff_count, per_buff_max[lv_idx]) for lv_idx, mods_lv in enumerate(base_mods)
        ]
        expected_mods = [
            mods_lv + [per_buff_mods[lv_idx]] * min(buff_count, per_buff_max[lv_idx])
            for lv_idx, mods_lv in enumerate(base_mods)
        ]
        expected_total_mods = [sum(mods_lv) for mods_lv in expected_mods]

        assert skill_data.hit_count == expected_hits, condition
        assert skill_data.hit_count_at_max == expected_hits[-1], condition

        # Checking the mods distribution here is sufficient because the additional hits were dealt at the same time
        for actual_mods_lv, expected_mods_lv in zip(skill_data.mods, expected_mods):
            assert sorted(actual_mods_lv) == sorted(expected_mods_lv), condition
        assert sorted(skill_data.mods_at_max) == sorted(expected_mods[-1]), condition

        assert skill_data.total_mod == pytest.approx(expected_total_mods), condition
        assert skill_data.total_mod_at_max == pytest.approx(expected_total_mods[-1]), condition

        assert skill_data.max_level == 3, condition
