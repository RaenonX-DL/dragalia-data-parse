"""Base classes for the entries."""
from .chara import CharaEntryBase
from .effect import EffectUnitEntryBase
from .effect_ability import AbilityVariantEffectEntry
from .entry import CsvExportableEntryBase, HashableEntryBase, JsonExportableEntryBase
from .skill import SkillExportEntryBase
from .text import TextEntry
from .unit_info import UnitInfoEntryBase
