from dlparse.transformer import SkillTransformer


def test_single_effect_area(transformer_skill: SkillTransformer):
    # Gala Cleo S1-FS
    # https://dragalialost.gamepedia.com/Gala_Cleo
    skill_data_base = transformer_skill.transform_supportive(101503021)

    # AB ID - 279
    # - Ab Type 14
    # - Var 1A - 131
    #
    # AC ID - 131
    # - EFS ID - 709017
    #
    # PA ID - 709017
    # - Placement Hit Label - ROD_CHR_04_H01_LV01

    # assert skill_data_base.max_level == 3
    #
    # expected_buffs_lv_1 = {
    #     SupportiveSkillUnit(
    #         target=HitTargetSimple.AREA,
    #         parameter=BuffParameter.HEAL_RP,
    #         rate=0.16,
    #         duration_time=10,
    #         duration_count=0,
    #         hit_attr_label="SWD_110_04_REJENE_FLD_LV01",
    #         action_cond_id=110
    #     ),
    # }
    # expected_base_buffs = [expected_buffs_lv_1, expected_buffs_lv_2, expected_buffs_lv_3]
    #
    # for skill_lv in range(skill_data_base.max_level):
    #     skill_data = skill_data_base.with_conditions()
    #
    #     expected_buffs = expected_base_buffs[skill_lv]
    #     actual_buffs = skill_data.buffs[skill_lv]
    #
    #     assert actual_buffs == expected_buffs, expected_buffs.symmetric_difference(actual_buffs)
