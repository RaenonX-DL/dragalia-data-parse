"""Various custom data models."""
from .ability import AbilityData
from .ability_var_conv import AbilityVariantEffectConvertible, AbilityVariantEffectPayload
from .action_cond_conv import ActionCondEffectConvertPayload, ActionCondEffectConvertible
from .buff_boost import BuffCountBoostData, BuffZoneBoostData
from .effect_ability import AbilityVariantEffectUnit
from .effect_action_cond import HitActionConditionEffectUnit, HitAfflictionEffectUnitHit
from .effect_base import EffectUnitBase
from .hit_base import HitData
from .hit_buff import BuffingHitData
from .hit_dmg import DamagingHitData
from .skill_atk import AttackingSkillData, AttackingSkillDataEntry
from .skill_base import SkillDataBase, SkillEntryBase
from .skill_sup import SupportiveSkillData, SupportiveSkillEntry
