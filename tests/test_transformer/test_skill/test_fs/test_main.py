from dlparse.transformer import SkillTransformer


def test_fs_atk(transformer_skill: SkillTransformer):
    # Sazanka S2-FS
    # https://dragalialost.gamepedia.com/Sazanka
    # skill_data_base = transformer_skill.transform_attacking(104405012)
    pass

    # FIXME - Sazanka S2-FS
    #   BUF_123_LV01
    #   310011301
    #   _EnhancedBurstAttack - FS
    #   AID - 409017
    #
    #   AXE_CHR_04_H01_LV01
    #   "_ToOdDmgRate": 1.0, - OD Punisher
    #   "_ToBreakDmgRate": 3.08, - BK Punisher?
    #
    #   BUF_229_01_LV01

    # # Base data
    # skill_data = skill_data_base.with_conditions()
    #
    # assert skill_data.is_fs
    # assert skill_data.allowed_counts == 3
    # assert skill_data.hit_count == [1, 1]
    # assert skill_data.hit_count_at_max == 1
    # assert skill_data.total_mod == pytest.approx([5.96 * 2, 6.63 * 2, 7.36 * 2, 8.18 * 2])
    # assert skill_data.total_mod_at_max == pytest.approx(16.36)
    # assert skill_data.mods == [[5.96] * 2, [6.63] * 2, [7.36] * 2, [8.18] * 2]
    # assert skill_data.mods_at_max == [8.18] * 2
    # assert skill_data.max_level == 4
