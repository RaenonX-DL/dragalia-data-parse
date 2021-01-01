"""Various custom data models."""
from .ability import AbilityData
from .ability_var import AbilityVariantData, AbilityVariantEffectPayload, AbilityVariantEffectUnit
from .action_cond_conv import ActionCondEffectConvertPayload, ActionCondEffectConvertible
from .action_cond_effect import HitActionConditionEffectUnit, HitAfflictionEffectUnitHit
from .base import HitData, SkillDataBase, SkillEntryBase
from .buff_boost import BuffCountBoostData, BuffZoneBoostData
from .hit_buff import BuffingHitData
from .hit_dmg import DamagingHitData
from .skill_atk import AttackingSkillData, AttackingSkillDataEntry
from .skill_sup import SupportiveSkillData, SupportiveSkillEntry
from .unit_cancel import SkillCancelActionUnit
