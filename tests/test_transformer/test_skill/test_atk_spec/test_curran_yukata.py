import pytest

from dlparse.enums import SkillCondition, SkillConditionComposite, SkillConditionCategories
from dlparse.errors import BulletEndOfLifeError
from dlparse.transformer import SkillTransformer
from tests.utils import approx_matrix


def test_s1_over_bullet_count(transformer_skill: SkillTransformer):
    # Yukata Curran S1
    # https://dragalialost.gamepedia.com/Yukata_Curran
    skill_data_base = transformer_skill.transform_attacking(103504041)

    # 7 Bullets (already ended)
    with pytest.raises(BulletEndOfLifeError):
        skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.BULLET_HIT_7))
    # 8 Bullets (already ended)
    with pytest.raises(BulletEndOfLifeError):
        skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.BULLET_HIT_8))


def test_s1_unmasked_no_affliction(transformer_skill: SkillTransformer):
    # Yukata Curran S1 - Unmasked
    # https://dragalialost.gamepedia.com/Yukata_Curran
    skill_data_base = transformer_skill.transform_attacking(103504041)

    level_1_base_expected = 1.32
    level_2_base_expected = 1.49
    level_3_base_expected = 1.65

    hits_expected = 3

    # Base data - (1 hit for each bullets)
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [hits_expected, hits_expected, hits_expected]
    assert skill_data.hit_count_at_max == hits_expected
    assert skill_data.total_mod == pytest.approx([
        level_1_base_expected * hits_expected,
        level_2_base_expected * hits_expected,
        level_3_base_expected * hits_expected
    ])
    assert skill_data.total_mod_at_max == pytest.approx(level_3_base_expected * hits_expected)
    assert skill_data.mods == [
        [level_1_base_expected] * hits_expected,
        [level_2_base_expected] * hits_expected,
        [level_3_base_expected] * hits_expected
    ]
    assert skill_data.mods_at_max == [level_3_base_expected] * hits_expected
    assert skill_data.max_level == 3

    # Different bullet hit count
    dmg_up_rate = {
        SkillCondition.BULLET_HIT_1: sum(0.55 ** deterioration_count for deterioration_count in range(1)),
        SkillCondition.BULLET_HIT_2: sum(0.55 ** deterioration_count for deterioration_count in range(2)),
        SkillCondition.BULLET_HIT_3: sum(0.55 ** deterioration_count for deterioration_count in range(3)),
        SkillCondition.BULLET_HIT_4: sum(0.55 ** deterioration_count for deterioration_count in range(4)),
        SkillCondition.BULLET_HIT_5: sum(0.55 ** deterioration_count for deterioration_count in range(5)),
        SkillCondition.BULLET_HIT_6: sum(0.55 ** deterioration_count for deterioration_count in range(6)),
    }

    for condition, up_rate in dmg_up_rate.items():
        skill_data = skill_data_base.with_conditions(SkillConditionComposite(condition))

        bullet_hit_count = SkillConditionCategories.skill_bullet_hit.convert(condition)
        hits_conditioned = hits_expected * bullet_hit_count

        assert skill_data.hit_count == [hits_conditioned, hits_conditioned, hits_conditioned]
        assert skill_data.hit_count_at_max == hits_conditioned
        assert skill_data.total_mod == pytest.approx([
            level_1_base_expected * hits_expected * up_rate,
            level_2_base_expected * hits_expected * up_rate,
            level_3_base_expected * hits_expected * up_rate
        ])
        assert skill_data.total_mod_at_max == pytest.approx(level_3_base_expected * hits_expected * up_rate)
        assert skill_data.mods == approx_matrix([
            [
                level_1_base_expected * 0.55 ** deterioration
                for deterioration in range(bullet_hit_count) for _ in range(hits_expected)
            ],
            [
                level_2_base_expected * 0.55 ** deterioration
                for deterioration in range(bullet_hit_count) for _ in range(hits_expected)
            ],
            [
                level_3_base_expected * 0.55 ** deterioration
                for deterioration in range(bullet_hit_count) for _ in range(hits_expected)
            ],
        ])
        assert skill_data.mods_at_max == [
            level_3_base_expected * 0.55 ** deterioration
            for deterioration in range(bullet_hit_count) for _ in range(hits_expected)
        ]
        assert skill_data.max_level == 3


def test_s1_unmasked_paralyzed(transformer_skill: SkillTransformer):
    # Yukata Curran S1 - Unmasked
    # https://dragalialost.gamepedia.com/Yukata_Curran
    skill_data_base = transformer_skill.transform_attacking(103504041)

    level_1_base_expected = 1.716
    level_2_base_expected = 1.937
    level_3_base_expected = 2.145

    hits_expected = 3

    # Base data - (1 hit for each bullets)
    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.TARGET_PARALYZED))

    assert skill_data.hit_count == [hits_expected, hits_expected, hits_expected]
    assert skill_data.hit_count_at_max == hits_expected
    assert skill_data.total_mod == pytest.approx([
        level_1_base_expected * hits_expected,
        level_2_base_expected * hits_expected,
        level_3_base_expected * hits_expected
    ])
    assert skill_data.total_mod_at_max == pytest.approx(level_3_base_expected * hits_expected)
    assert skill_data.mods == approx_matrix([
        [level_1_base_expected] * hits_expected,
        [level_2_base_expected] * hits_expected,
        [level_3_base_expected] * hits_expected
    ])
    assert skill_data.mods_at_max == pytest.approx([level_3_base_expected] * hits_expected)
    assert skill_data.max_level == 3

    # Different bullet hit count
    dmg_up_rate = {
        SkillCondition.BULLET_HIT_1: sum(0.55 ** deterioration_count for deterioration_count in range(1)),
        SkillCondition.BULLET_HIT_2: sum(0.55 ** deterioration_count for deterioration_count in range(2)),
        SkillCondition.BULLET_HIT_3: sum(0.55 ** deterioration_count for deterioration_count in range(3)),
        SkillCondition.BULLET_HIT_4: sum(0.55 ** deterioration_count for deterioration_count in range(4)),
        SkillCondition.BULLET_HIT_5: sum(0.55 ** deterioration_count for deterioration_count in range(5)),
        SkillCondition.BULLET_HIT_6: sum(0.55 ** deterioration_count for deterioration_count in range(6)),
    }

    for condition, up_rate in dmg_up_rate.items():
        skill_data = skill_data_base.with_conditions(
            SkillConditionComposite((SkillCondition.TARGET_PARALYZED, condition)))

        bullet_hit_count = SkillConditionCategories.skill_bullet_hit.convert(condition)
        hits_conditioned = hits_expected * bullet_hit_count

        assert skill_data.hit_count == [hits_conditioned, hits_conditioned, hits_conditioned]
        assert skill_data.hit_count_at_max == hits_conditioned
        assert skill_data.total_mod == pytest.approx([
            level_1_base_expected * hits_expected * up_rate,
            level_2_base_expected * hits_expected * up_rate,
            level_3_base_expected * hits_expected * up_rate
        ])
        assert skill_data.total_mod_at_max == pytest.approx(level_3_base_expected * hits_expected * up_rate)
        assert skill_data.mods == approx_matrix([
            [
                level_1_base_expected * 0.55 ** deterioration
                for deterioration in range(bullet_hit_count) for _ in range(hits_expected)
            ],
            [
                level_2_base_expected * 0.55 ** deterioration
                for deterioration in range(bullet_hit_count) for _ in range(hits_expected)
            ],
            [
                level_3_base_expected * 0.55 ** deterioration
                for deterioration in range(bullet_hit_count) for _ in range(hits_expected)
            ],
        ])
        assert skill_data.mods_at_max == pytest.approx([
            level_3_base_expected * 0.55 ** deterioration
            for deterioration in range(bullet_hit_count) for _ in range(hits_expected)
        ])
        assert skill_data.max_level == 3


def test_s1_masked_no_affliction(transformer_skill: SkillTransformer):
    # Yukata Curran S1 - Masked
    # https://dragalialost.gamepedia.com/Yukata_Curran
    skill_data_base = transformer_skill.transform_attacking(103504043)

    level_1_base_expected = 1.44
    level_2_base_expected = 1.62
    level_3_base_expected = 1.82

    hits_expected = 5

    # Base data - (1 hit for each bullets)
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [hits_expected, hits_expected, hits_expected]
    assert skill_data.hit_count_at_max == hits_expected
    assert skill_data.total_mod == pytest.approx([
        level_1_base_expected * hits_expected,
        level_2_base_expected * hits_expected,
        level_3_base_expected * hits_expected
    ])
    assert skill_data.total_mod_at_max == pytest.approx(level_3_base_expected * hits_expected)
    assert skill_data.mods == approx_matrix([
        [level_1_base_expected] * hits_expected,
        [level_2_base_expected] * hits_expected,
        [level_3_base_expected] * hits_expected
    ])
    assert skill_data.mods_at_max == pytest.approx([level_3_base_expected] * hits_expected)
    assert skill_data.max_level == 3

    # Different bullet hit count
    dmg_up_rate = {
        SkillCondition.BULLET_HIT_1: sum(0.55 ** deterioration_count for deterioration_count in range(1)),
        SkillCondition.BULLET_HIT_2: sum(0.55 ** deterioration_count for deterioration_count in range(2)),
        SkillCondition.BULLET_HIT_3: sum(0.55 ** deterioration_count for deterioration_count in range(3)),
        SkillCondition.BULLET_HIT_4: sum(0.55 ** deterioration_count for deterioration_count in range(4)),
        SkillCondition.BULLET_HIT_5: sum(0.55 ** deterioration_count for deterioration_count in range(5)),
        SkillCondition.BULLET_HIT_6: sum(0.55 ** deterioration_count for deterioration_count in range(6)),
    }

    for condition, up_rate in dmg_up_rate.items():
        skill_data = skill_data_base.with_conditions(SkillConditionComposite(condition))

        bullet_hit_count = SkillConditionCategories.skill_bullet_hit.convert(condition)
        hits_conditioned = hits_expected * bullet_hit_count

        assert skill_data.hit_count == [hits_conditioned, hits_conditioned, hits_conditioned]
        assert skill_data.hit_count_at_max == hits_conditioned
        assert skill_data.total_mod == pytest.approx([
            level_1_base_expected * hits_expected * up_rate,
            level_2_base_expected * hits_expected * up_rate,
            level_3_base_expected * hits_expected * up_rate
        ])
        assert skill_data.total_mod_at_max == pytest.approx(level_3_base_expected * hits_expected * up_rate)
        assert skill_data.mods == approx_matrix([
            [
                level_1_base_expected * 0.55 ** deterioration
                for deterioration in range(bullet_hit_count) for _ in range(hits_expected)
            ],
            [
                level_2_base_expected * 0.55 ** deterioration
                for deterioration in range(bullet_hit_count) for _ in range(hits_expected)
            ],
            [
                level_3_base_expected * 0.55 ** deterioration
                for deterioration in range(bullet_hit_count) for _ in range(hits_expected)
            ],
        ])
        assert skill_data.mods_at_max == pytest.approx([
            level_3_base_expected * 0.55 ** deterioration
            for deterioration in range(bullet_hit_count) for _ in range(hits_expected)
        ])
        assert skill_data.max_level == 3


def test_s1_masked_paralyzed(transformer_skill: SkillTransformer):
    # Yukata Curran S1 - Masked
    # https://dragalialost.gamepedia.com/Yukata_Curran
    skill_data_base = transformer_skill.transform_attacking(103504043)

    level_1_base_expected = 1.872
    level_2_base_expected = 2.106
    level_3_base_expected = 2.366

    hits_expected = 5

    # Base data - (1 hit for each bullets)
    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.TARGET_PARALYZED))

    assert skill_data.hit_count == [hits_expected, hits_expected, hits_expected]
    assert skill_data.hit_count_at_max == hits_expected
    assert skill_data.total_mod == pytest.approx([
        level_1_base_expected * hits_expected,
        level_2_base_expected * hits_expected,
        level_3_base_expected * hits_expected
    ])
    assert skill_data.total_mod_at_max == pytest.approx(level_3_base_expected * hits_expected)
    assert skill_data.mods == approx_matrix([
        [level_1_base_expected] * hits_expected,
        [level_2_base_expected] * hits_expected,
        [level_3_base_expected] * hits_expected
    ])
    assert skill_data.mods_at_max == pytest.approx([level_3_base_expected] * hits_expected)
    assert skill_data.max_level == 3

    # Different bullet hit count
    dmg_up_rate = {
        SkillCondition.BULLET_HIT_1: sum(0.55 ** deterioration_count for deterioration_count in range(1)),
        SkillCondition.BULLET_HIT_2: sum(0.55 ** deterioration_count for deterioration_count in range(2)),
        SkillCondition.BULLET_HIT_3: sum(0.55 ** deterioration_count for deterioration_count in range(3)),
        SkillCondition.BULLET_HIT_4: sum(0.55 ** deterioration_count for deterioration_count in range(4)),
        SkillCondition.BULLET_HIT_5: sum(0.55 ** deterioration_count for deterioration_count in range(5)),
        SkillCondition.BULLET_HIT_6: sum(0.55 ** deterioration_count for deterioration_count in range(6)),
    }

    for condition, up_rate in dmg_up_rate.items():
        skill_data = skill_data_base.with_conditions(
            SkillConditionComposite((SkillCondition.TARGET_PARALYZED, condition)))

        bullet_hit_count = SkillConditionCategories.skill_bullet_hit.convert(condition)
        hits_conditioned = hits_expected * bullet_hit_count

        assert skill_data.hit_count == [hits_conditioned, hits_conditioned, hits_conditioned]
        assert skill_data.hit_count_at_max == hits_conditioned
        assert skill_data.total_mod == pytest.approx([
            level_1_base_expected * hits_expected * up_rate,
            level_2_base_expected * hits_expected * up_rate,
            level_3_base_expected * hits_expected * up_rate
        ])
        assert skill_data.total_mod_at_max == pytest.approx(level_3_base_expected * hits_expected * up_rate)
        assert skill_data.mods == approx_matrix([
            [
                level_1_base_expected * 0.55 ** deterioration
                for deterioration in range(bullet_hit_count) for _ in range(hits_expected)
            ],
            [
                level_2_base_expected * 0.55 ** deterioration
                for deterioration in range(bullet_hit_count) for _ in range(hits_expected)
            ],
            [
                level_3_base_expected * 0.55 ** deterioration
                for deterioration in range(bullet_hit_count) for _ in range(hits_expected)
            ],
        ])
        assert skill_data.mods_at_max == pytest.approx([
            level_3_base_expected * 0.55 ** deterioration
            for deterioration in range(bullet_hit_count) for _ in range(hits_expected)
        ])
        assert skill_data.max_level == 3


def test_s2_masked_no_affliction(transformer_skill: SkillTransformer):
    # Yukata Curran S2 - Masked
    # https://dragalialost.gamepedia.com/Yukata_Curran
    skill_data_base = transformer_skill.transform_attacking(103504044)

    level_1_base_expected = 0.72
    level_2_base_expected = 0.9

    hits_expected = 30

    # Base data - (1 hit for each bullets)
    skill_data = skill_data_base.with_conditions()

    assert skill_data.hit_count == [hits_expected, hits_expected]
    assert skill_data.hit_count_at_max == hits_expected
    assert skill_data.total_mod == pytest.approx([
        level_1_base_expected * hits_expected,
        level_2_base_expected * hits_expected
    ])
    assert skill_data.total_mod_at_max == pytest.approx(level_2_base_expected * hits_expected)
    assert skill_data.mods == approx_matrix([
        [level_1_base_expected] * hits_expected,
        [level_2_base_expected] * hits_expected,
    ])
    assert skill_data.mods_at_max == pytest.approx([level_2_base_expected] * hits_expected)
    assert skill_data.max_level == 2


def test_s2_masked_paralyzed(transformer_skill: SkillTransformer):
    # Yukata Curran S2 - Masked
    # https://dragalialost.gamepedia.com/Yukata_Curran
    skill_data_base = transformer_skill.transform_attacking(103504044)

    level_1_base_expected = 0.864
    level_2_base_expected = 1.08

    hits_expected = 30

    # Base data - (1 hit for each bullets)
    skill_data = skill_data_base.with_conditions(SkillConditionComposite(SkillCondition.TARGET_PARALYZED))

    assert skill_data.hit_count == [hits_expected, hits_expected]
    assert skill_data.hit_count_at_max == hits_expected
    assert skill_data.total_mod == pytest.approx([
        level_1_base_expected * hits_expected,
        level_2_base_expected * hits_expected
    ])
    assert skill_data.total_mod_at_max == pytest.approx(level_2_base_expected * hits_expected)
    assert skill_data.mods == approx_matrix([
        [level_1_base_expected] * hits_expected,
        [level_2_base_expected] * hits_expected
    ])
    assert skill_data.mods_at_max == pytest.approx([level_2_base_expected] * hits_expected)
    assert skill_data.max_level == 2
