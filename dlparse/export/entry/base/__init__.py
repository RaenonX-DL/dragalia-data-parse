"""Base classes for the entries."""
from .chara import CharaEntryBase
from .effect import EffectUnitEntryBase
from .effect_ability import AbilityVariantEffectEntry
from .entry import CsvExportableEntryBase, HashableEntryBase, JsonExportableEntryBase
from .named import NamedEntry
from .skill import SkillExportEntryBase
from .text import TextEntry
from .type import JsonBody, JsonSchema
from .unit_info import UnitInfoEntryBase
