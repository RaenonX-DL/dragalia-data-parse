"""Implementations for an entry which can be used to discover all possible skills."""
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING, Union

from dlparse.enums import SkillChainCondition, SkillNumber
from dlparse.errors import ActionDataNotFoundError, InvalidSkillIdentifierLabelError
from .skill import SkillEntry

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager
    from dlparse.mono.asset import AbilityEntry, SkillDataEntry, DragonDataEntry

__all__ = ("SkillIdentifierLabel", "SkillIdEntry", "SkillDiscoverableEntry")


class SkillIdentifierLabel:
    """
    Class for skill identifier labels.

    The label name will be used in `translation.json` for different locale at the frontend side.
    Therefore, the naming format may be different.

    Quick reference
    ===============
    Base S1: ``s1_base``

    Base S2: ``s2_base``

    Helper: ``helper``

    S1 in Mode #5: ``s1_mode_5``

    S1 enhanced by S2: ``s1_enhanced_by_s2``

    FS enhanced by S1: ``fs_enhanced_by_s1``

    S1 in phase 3: ``s1_p3``
    """

    S1_BASE = "s1_base"
    S2_BASE = "s2_base"
    S1_DRAGON = "s1_dragon"
    S2_DRAGON = "s2_dragon"
    SHARED = "shared"
    HELPER = "helper"

    @staticmethod
    def of_mode(skill_num: SkillNumber, mode_id: int) -> str:
        """Get the identifier label of the skill ``skill_num`` in mode ``mode_id``."""
        return f"{skill_num.repr}_mode_{mode_id}"

    @staticmethod
    def of_phase(skill_num: SkillNumber, phase_num: int) -> str:
        """Get the identifier label of ``skill_num`` in phase ``phase_num``."""
        return f"{skill_num.repr}_p{phase_num}"

    @staticmethod
    def of_chain(skill_num: SkillNumber, chain_cond: SkillChainCondition):
        """Get the identifier label of chained skill ``skill_num`` given condition ``chain_cond``."""
        return f"{skill_num.repr}_chain_{chain_cond.repr}"

    @staticmethod
    def skill_enhanced_by_skill(receiver_skill_num: SkillNumber, enhancer_skill_num: SkillNumber) -> str:
        """
        Get the identifier label of the skill ``receiver_skill_num`` enhanced by ``enhancer_skill_num``.

        :raises InvalidSkillIdentifierLabelError: if the enhancer skill and the receiver skill is the same
        """
        if receiver_skill_num == enhancer_skill_num:
            raise InvalidSkillIdentifierLabelError("Skill that enhances itself should be considered as phase changing")

        return f"{receiver_skill_num.repr}_enhanced_by_{enhancer_skill_num.repr}"

    @staticmethod
    def skill_enhanced_by_ability(skill_num: SkillNumber, ability_id: int) -> str:
        """Get the identifier label of the skill ``skill_num`` enhanced by the ability ``ability_id``."""
        return f"{skill_num.repr}_enhanced_by_ab{ability_id}"

    @staticmethod
    def fs_enhanced_by_skill(enhancer_skill_num: SkillNumber) -> str:
        """Get the identifier label of FS enhanced by ``enhancer_skill_num``."""
        return f"fs_enhanced_by_{enhancer_skill_num.repr}"


@dataclass
class SkillIdEntry:
    """Class for a skill ID entry."""

    skill_id: int
    """Skill ID."""
    skill_num: SkillNumber
    """Skill number."""
    skill_identifier_labels: Union[str, list[str]]
    """
    A list of skill identifier labels.

    These will be translated at the frontend side for easier identification.

    If a skill has multiple purposes (for example, served as shared variant and also S1 base, which is common),
    all of the purposes will be listed.
    """

    def __post_init__(self):
        # Force labels to be a list
        if isinstance(self.skill_identifier_labels, str):
            self.skill_identifier_labels = [self.skill_identifier_labels]

    @staticmethod
    def merge(entries: list["SkillIdEntry"]) -> list["SkillIdEntry"]:
        """
        Merge duplicated skill ID ``entries``.

        If there are multiple entries sharing the same ``skill_id``,
        they will be merged into one by merging ``skill_identifier_labels``.
        """
        entries_to_be_processed = defaultdict(list)

        for entry in entries:
            entries_to_be_processed[entry.skill_id].append(entry)

        ret: list[SkillIdEntry] = []

        for _, entry_list in sorted(entries_to_be_processed.items(), key=lambda item: item[0]):
            entry: SkillIdEntry = entry_list[0]

            for subsequent_entry in entry_list[1:]:
                # Filter out duplicated entries while preserving its order
                entry.skill_identifier_labels.extend(
                    label for label in subsequent_entry.skill_identifier_labels
                    if label not in entry.skill_identifier_labels
                )

            ret.append(entry)

        return ret


@dataclass
class SkillDiscoverableEntry(SkillEntry, ABC):
    """An interface that allows an entry to discover its possible skills."""

    ss_skill_id: int
    ss_skill_num: SkillNumber

    unique_dragon_id: int

    @property
    @abstractmethod
    def ability_ids_all_level(self) -> list[int]:
        """Get a list of effective (non-zero) ability / passive IDs at all levels."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def mode_ids(self) -> list[int]:
        """
        Get a list of effective mode IDs.

        This could include but not limited to:

        - Enhance mode (Bellina)

        - Buff stacks (Catherine)
        """
        raise NotImplementedError()

    @abstractmethod
    def max_skill_level(self, skill_num: SkillNumber) -> int:
        """
        Get the maximum skill level of a skill.

        :raises InvalidSkillNumError: if `skill_num` is invalid (unhandled)
        """
        raise NotImplementedError()

    @property
    def has_unique_dragon(self) -> bool:
        """Check if the character has an unique dragon."""
        return self.unique_dragon_id != 0

    def _get_hit_labels(
            self, asset_manager: "AssetManager", skill_data: "SkillDataEntry", skill_num: SkillNumber
    ) -> dict[str, SkillNumber]:
        """
        Get a :class:`dict` which key is the hit labels of ``skill_data`` and value is ``skill_num``.

        ``skill_num`` indicates the source skill number of the corresponding hit label.
        """
        hit_labels: dict[str, SkillNumber] = {}

        # Load all hit labels of the skill
        for action_id in skill_data.action_id_1_by_level:
            for skill_lv in range(1, self.max_skill_level(skill_num) + 1):
                try:
                    prefab = asset_manager.loader_action.get_prefab(action_id)
                    for hit_label, _ in prefab.get_hit_actions(skill_lv):
                        hit_labels[hit_label] = skill_num
                except ActionDataNotFoundError:
                    pass  # If prefab file not found, nothing should happen

        return hit_labels

    def _get_hit_label_entry(
            self, asset_manager: "AssetManager", skill_id: int, skill_num: SkillNumber,
            src_skill_num: SkillNumber, hit_labels: dict[str, SkillNumber], phase_counter: dict[SkillNumber, int]
    ) -> SkillIdEntry:
        """
        Get the skill ID entry which originated from ``src_skill_num``.

        Both ``skill_id`` and ``skill_num`` are the enhanced skill identity, **not** the enhancement source.

        ``hit_labels`` will be updated with the possible hit labels of the enhanced skill ``skill_id``
        after this method call.

        ``skill_num`` of ``phase_counter`` will be incremented if the skill is hit_data-enhancing,
        i.e. ``src_skill_num = ``skill_num``).
        """
        # Get the label to be used
        if src_skill_num == skill_num:
            # Self-enhancing, considered as phase instead
            label = SkillIdentifierLabel.of_phase(skill_num, phase_counter[skill_num])
            phase_counter[skill_num] += 1
        else:
            # Enhanced by other skill
            label = SkillIdentifierLabel.skill_enhanced_by_skill(skill_num, src_skill_num)

        # Get the other hit labels (if available) for further discovery
        skill_data = asset_manager.asset_skill_data.get_data_by_id(skill_id)
        hit_labels.update(self._get_hit_labels(asset_manager, skill_data, skill_num))

        # Return enhanced skill ID entry
        return SkillIdEntry(skill_id, skill_num, label)

    def _from_hit_labels(
            self, asset_manager: "AssetManager", skill_data: "SkillDataEntry", skill_num: SkillNumber
    ) -> list[SkillIdEntry]:
        """
        Get all possible skills from the hit labels of ``skill_id``.

        ``skill_num`` should correspond to the skill number of ``skill_id``.
        """
        ret: list[SkillIdEntry] = []

        # Initial hit labels to be discovered
        hit_labels = self._get_hit_labels(asset_manager, skill_data, skill_num)
        hit_labels_searched: set[str] = set()

        # Counter to be used if the skill is hit_data-enhancing (consider as phased skills instead)
        # Such case appears on Xander (`10150201`)
        phase_counter = {SkillNumber.S1: 2, SkillNumber.S2: 2}

        # Check each hit labels to see if there are any skill enhancements
        while hit_labels:
            hit_label, src_skill_num = hit_labels.popitem()

            if hit_label in hit_labels_searched:
                continue  # Hit label already searched, skipping

            hit_labels_searched.add(hit_label)

            if hit_label not in asset_manager.asset_hit_attr:
                continue  # Hit label could be missing - officials inserted dummy data

            action_cond_id = asset_manager.asset_hit_attr.get_data_by_id(hit_label).action_condition_id
            if not action_cond_id:
                continue  # Action condition ID = 0 - not used

            action_cond = asset_manager.asset_action_cond.get_data_by_id(action_cond_id)
            if not action_cond:
                continue  # Action condition data not found - officials inserted dummy action condition data

            enhance_targets = [
                (SkillNumber.S1, action_cond.enhance_skill_1_id),
                (SkillNumber.S2, action_cond.enhance_skill_2_id)
            ]

            for target_skill_num, target_skill_id in enhance_targets:
                if not target_skill_id:
                    continue  # Enhance target skill ID not set (= 0)

                ret.append(self._get_hit_label_entry(
                    asset_manager, target_skill_id, target_skill_num, src_skill_num, hit_labels, phase_counter
                ))

        return ret

    @staticmethod
    def _from_helper(skill_data: "SkillDataEntry") -> list[SkillIdEntry]:
        """Get the helper variant of ``skill_data``."""
        ret: list[SkillIdEntry] = []

        if skill_data.has_helper_variant:
            ret.append(SkillIdEntry(
                skill_data.as_helper_skill_id,
                SkillNumber.S1,  # Assumes that all helper skill is S1
                SkillIdentifierLabel.HELPER
            ))

        return ret

    @staticmethod
    def _phase_single(
            skill_data: "SkillDataEntry", asset_manager: "AssetManager", skill_num: SkillNumber
    ) -> list[SkillIdEntry]:
        """Get all possible skills after phase changing for ``skill_data``, excluding the source skill."""
        if not skill_data.has_phase_variant:
            return []

        ret: list[SkillIdEntry] = []
        added_skill_id: set[int] = set()
        current_source: "SkillDataEntry" = skill_data

        while trans_skill_data := asset_manager.asset_skill_data.get_data_by_id(current_source.trans_skill_id):
            if trans_skill_data.id == skill_data.id:
                break  # Changed to source skill data

            if trans_skill_data.id in added_skill_id:
                break  # Phase looped back

            phase_num = len(ret) + 2

            ret.append(SkillIdEntry(
                trans_skill_data.id,
                skill_num,
                SkillIdentifierLabel.of_phase(skill_num, phase_num)
            ))
            added_skill_id.add(trans_skill_data.id)

            current_source = trans_skill_data

        return ret

    def _from_phase(
            self, asset_manager: "AssetManager", skill_1_data: "SkillDataEntry", skill_2_data: "SkillDataEntry"
    ) -> list[SkillIdEntry]:
        """Get all phased skill variants of both ``skill_1_data`` and ``skill_2_data``."""
        ret: list[SkillIdEntry] = []

        if skill_1_data.has_phase_variant:
            ret.extend(self._phase_single(skill_1_data, asset_manager, SkillNumber.S1))

        if skill_2_data.has_phase_variant:
            ret.extend(self._phase_single(skill_2_data, asset_manager, SkillNumber.S2))

        return ret

    @staticmethod
    def _chain_single(
            skill_data: "SkillDataEntry", asset_manager: "AssetManager", skill_num: SkillNumber
    ) -> list[SkillIdEntry]:
        """Get all possible chained skill variants, excluding the source skill."""
        if not skill_data.has_chain_variant:
            return []

        ret: list[SkillIdEntry] = []

        chain_data_list = asset_manager.asset_skill_chain.get_data_by_group_id(skill_data.chain_group_id)
        for chain_data in chain_data_list:
            ret.append(SkillIdEntry(
                chain_data.id,
                skill_num,
                SkillIdentifierLabel.of_chain(skill_num, chain_data.chain_condition)
            ))

        return ret

    def _from_chain(
            self, asset_manager: "AssetManager", skill_1_data: "SkillDataEntry", skill_2_data: "SkillDataEntry"
    ) -> list[SkillIdEntry]:
        """Get all chained skill variants of both ``skill_1_data`` and ``skill_2_data``."""
        ret: list[SkillIdEntry] = []

        if skill_1_data.has_chain_variant:
            ret.extend(self._chain_single(skill_1_data, asset_manager, SkillNumber.S1))

        if skill_2_data.has_chain_variant:
            ret.extend(self._chain_single(skill_2_data, asset_manager, SkillNumber.S2))

        return ret

    def _get_all_ability(self, asset_manager: "AssetManager") -> dict[int, "AbilityEntry"]:
        """Get all ability data that may be used by this entry."""
        ret: dict[int, "AbilityEntry"] = {}

        ability_asset = asset_manager.asset_ability_data

        for ability_id in self.ability_ids_all_level:
            ret.update(ability_asset.get_data_by_id(ability_id).get_all_ability(ability_asset))

        return ret

    def _skill_additional_single(
            self, asset_manager: "AssetManager", skill_data: "SkillDataEntry", skill_num: SkillNumber
    ) -> list[SkillIdEntry]:
        """
        Get all possible variants of a ``skill_data``.

        This includes phase variant, chain variant and the variants from the skill hit labels;
        does not include the skill data being passed in.
        """
        ret: list[SkillIdEntry] = []

        if skill_data.has_phase_variant:
            ret.extend(self._phase_single(skill_data, asset_manager, skill_num))

        if skill_data.has_chain_variant:
            ret.extend(self._chain_single(skill_data, asset_manager, skill_num))

        ret.extend(self._from_hit_labels(asset_manager, skill_data, skill_num))

        return ret

    def _from_base(self) -> list[SkillIdEntry]:
        """Get the base skills."""
        ret: list[SkillIdEntry] = [
            SkillIdEntry(self.skill_1_id, SkillNumber.S1, SkillIdentifierLabel.S1_BASE),
            SkillIdEntry(self.skill_2_id, SkillNumber.S2, SkillIdentifierLabel.S2_BASE)
        ]

        if self.ss_skill_id:
            ret.append(SkillIdEntry(self.ss_skill_id, self.ss_skill_num, SkillIdentifierLabel.SHARED))

        return ret

    def _from_mode(self, asset_manager: "AssetManager") -> list[SkillIdEntry]:
        """Get all possible skills from all possible modes."""
        ret: list[SkillIdEntry] = []

        for mode_id in self.mode_ids:
            if mode_data := asset_manager.asset_chara_mode.get_data_by_id(mode_id):
                if model_skill_1_id := mode_data.skill_id_1:
                    ret.append(SkillIdEntry(
                        model_skill_1_id, SkillNumber.S1, SkillIdentifierLabel.of_mode(SkillNumber.S1, mode_id)
                    ))

                if model_skill_2_id := mode_data.skill_id_2:
                    ret.append(SkillIdEntry(
                        model_skill_2_id, SkillNumber.S2, SkillIdentifierLabel.of_mode(SkillNumber.S2, mode_id)
                    ))

        return ret

    def _from_dragon(self, asset_manager: "AssetManager") -> list[SkillIdEntry]:
        """Get all possible skills from the dragon, if it's unique for the unit."""
        if not self.has_unique_dragon:
            return []

        ret: list[SkillIdEntry] = []

        unique_dragon_data: "DragonDataEntry" = asset_manager.asset_dragon.get_data_by_id(self.unique_dragon_id)

        skill_1_data: "SkillDataEntry" = asset_manager.asset_skill_data.get_data_by_id(unique_dragon_data.skill_1_id)
        ret.append(SkillIdEntry(
            unique_dragon_data.skill_1_id, SkillNumber.S1_DRAGON, SkillIdentifierLabel.S1_DRAGON
        ))
        ret.extend(self._skill_additional_single(asset_manager, skill_1_data, SkillNumber.S1_DRAGON))

        # Dragon usually does not have 2 skills (except Tiki's)
        if skill_2_data := asset_manager.asset_skill_data.get_data_by_id(unique_dragon_data.skill_2_id):
            ret.append(SkillIdEntry(
                unique_dragon_data.skill_2_id, SkillNumber.S2_DRAGON, SkillIdentifierLabel.S2_DRAGON
            ))
            ret.extend(self._skill_additional_single(asset_manager, skill_2_data, SkillNumber.S2_DRAGON))

        return ret

    def _from_skill_ext(self, asset_manager: "AssetManager") -> list[SkillIdEntry]:
        """
        Get all possible skills extended from base S1 and S2. This also returns the helper variant, if any.

        Note that base S1 and S2 will not be included.
        """
        ret: list[SkillIdEntry] = []

        skill_1_data: "SkillDataEntry" = asset_manager.asset_skill_data.get_data_by_id(self.skill_1_id)
        skill_2_data: "SkillDataEntry" = asset_manager.asset_skill_data.get_data_by_id(self.skill_2_id)

        ret.extend(self._skill_additional_single(asset_manager, skill_1_data, SkillNumber.S1))
        ret.extend(self._skill_additional_single(asset_manager, skill_2_data, SkillNumber.S2))
        ret.extend(self._from_helper(skill_1_data))

        return ret

    def _from_ability(self, asset_manager: "AssetManager") -> list[SkillIdEntry]:
        """Get all possible skills from the ability of ``chara_data``."""
        ret: list[SkillIdEntry] = []

        ability_data_dict: dict[int, "AbilityEntry"] = self._get_all_ability(asset_manager)

        for ability_id, ability_data in ability_data_dict.items():
            # Add skill IDs enhanced by the ability
            for skill_id, skill_num in ability_data.enhanced_skills:
                ret.append(SkillIdEntry(
                    skill_id, skill_num, SkillIdentifierLabel.skill_enhanced_by_ability(skill_num, ability_id)
                ))

            # Add skill IDs enhanced by the action condition from the ability
            for action_cond_id in ability_data.action_conditions:
                action_cond = asset_manager.asset_action_cond.get_data_by_id(action_cond_id)

                if action_cond.enhance_skill_1_id:
                    ret.append(SkillIdEntry(
                        action_cond.enhance_skill_1_id, SkillNumber.S1,
                        SkillIdentifierLabel.skill_enhanced_by_ability(SkillNumber.S1, ability_id)
                    ))
                    ret.extend(self._from_hit_labels(
                        asset_manager, asset_manager.asset_skill_data.get_data_by_id(action_cond.enhance_skill_1_id),
                        SkillNumber.S1
                    ))
                if action_cond.enhance_skill_2_id:
                    ret.append(SkillIdEntry(
                        action_cond.enhance_skill_2_id, SkillNumber.S2,
                        SkillIdentifierLabel.skill_enhanced_by_ability(SkillNumber.S2, ability_id)
                    ))
                    ret.extend(self._from_hit_labels(
                        asset_manager, asset_manager.asset_skill_data.get_data_by_id(action_cond.enhance_skill_2_id),
                        SkillNumber.S2
                    ))

        return ret

    def get_skill_id_entries(self, asset_manager: "AssetManager") -> list[SkillIdEntry]:
        """Get all possible skill ID entries of a character."""
        ret: list[SkillIdEntry] = self._from_base()

        ret.extend(self._from_mode(asset_manager))
        ret.extend(self._from_dragon(asset_manager))
        ret.extend(self._from_skill_ext(asset_manager))
        ret.extend(self._from_ability(asset_manager))

        return SkillIdEntry.merge(ret)
