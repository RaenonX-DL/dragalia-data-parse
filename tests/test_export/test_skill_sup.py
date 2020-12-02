from dlparse.enums import SkillCondition, SkillConditionComposite, HitTargetSimple, BuffParameter
from dlparse.export import export_sup_skills_as_entries
from dlparse.mono.asset import CharaDataAsset, CharaModeAsset, TextAsset
from dlparse.transformer import SkillTransformer
from tests.expected_skills_lookup import skill_ids_sup

ExpectedInfoType = dict[tuple[int, SkillConditionComposite], set[tuple[HitTargetSimple, BuffParameter, float]]]

expected_contained_info: ExpectedInfoType = {
    # Kirsty S2
    (105503022, SkillConditionComposite()): {
        (HitTargetSimple.TEAM, BuffParameter.ATK, 0.2)
    },
    # Patia S1
    (105405021, SkillConditionComposite()): {
        (HitTargetSimple.TEAM, BuffParameter.ATK, 0.15),
        (HitTargetSimple.TEAM, BuffParameter.DEF, 0.25)
    },
    # S!Julietta S2 P3
    (104502014, SkillConditionComposite()): {
        (HitTargetSimple.SELF_SURROUNDING, BuffParameter.ATK, 0.15),
        (HitTargetSimple.SELF_SURROUNDING, BuffParameter.CRT_RATE, 0.13),
        (HitTargetSimple.SELF_SURROUNDING, BuffParameter.SHIELD_SINGLE_DMG, 0.4)
    },
    # S!Cleo S2
    (106504012, SkillConditionComposite(SkillCondition.COVER_TEAMMATE_3)): {
        (HitTargetSimple.SELF_SURROUNDING, BuffParameter.ATK, 0.05),
        (HitTargetSimple.SELF_SURROUNDING, BuffParameter.CRT_RATE, 0.03),
        (HitTargetSimple.SELF_SURROUNDING, BuffParameter.SKILL_DAMAGE, 0.1),
        (HitTargetSimple.SELF_SURROUNDING, BuffParameter.SP_RATE, 0.1),
        (HitTargetSimple.SELF, BuffParameter.DEF, 0.1),
        (HitTargetSimple.SELF, BuffParameter.CRT_DAMAGE, 0.1),
        (HitTargetSimple.SELF, BuffParameter.SP_CHARGE_PCT_S1, 1),
    },
    # Emma S1
    (105401031, SkillConditionComposite(SkillCondition.TARGET_ELEM_FLAME)): {
        (HitTargetSimple.TEAM, BuffParameter.ATK, 0.25),
    }
}


def test_exported_entries(asset_chara: CharaDataAsset, asset_chara_mode: CharaModeAsset, asset_text: TextAsset,
                          transformer_skill: SkillTransformer):
    entries = export_sup_skills_as_entries(asset_chara, asset_chara_mode, asset_text, transformer_skill)

    assert len(entries) > 0

    skill_ids_missing: dict[int, str] = skill_ids_sup.copy()
    skill_info_missing: ExpectedInfoType = expected_contained_info.copy()

    for entry in entries:
        skill_ids_missing.pop(entry.skill_internal_id, None)

        key = (entry.skill_internal_id, entry.skill_condition_comp)

        if expected_effects := skill_info_missing.get(key):
            expected_effects.remove((entry.target, entry.buff_parameter, entry.rate))

            if not expected_effects:
                skill_info_missing.pop(key)

    assert len(skill_ids_missing) == 0, f"Skill IDs missing: {skill_ids_missing}"
    assert len(skill_info_missing) == 0, f"Info missing: {skill_info_missing}"
