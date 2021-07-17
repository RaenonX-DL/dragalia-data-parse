"""Base classes for the entries."""
from .cancel import SkillCancelInfoEntry
from .effect import EffectUnitEntryBase
from .effect_ability import AbilityVariantEffectEntry
from .entry import CsvExportableEntryBase, HashableEntryBase, JsonExportableEntryBase
from .ex_ability import ExAbiltiesEntry
from .named import NamedEntry
from .skill import SkillExportEntryBase
from .text import TextEntry
from .type import JsonBody, JsonSchema
from .unit import UnitEntryBase
from .unit_info import UnitInfoEntryBase
