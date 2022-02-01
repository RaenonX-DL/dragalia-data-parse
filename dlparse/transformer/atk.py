"""
Implementations for all other attacking actions.

This includes things like:
# TODO: Check test notes for special actions
- Special attacking actions
    - Sazanka S2-FS
    - Ilia S2-FS (`10950401`) / Roll
    - OG!Vanessa S1-FS
- Special supportive actions
    - Gala Cleo S1-FS
- Normal attack info
"""
from typing import Optional, TYPE_CHECKING

from dlparse.errors import ActionDataNotFoundError
from dlparse.model import NormalAttackChain, NormalAttackCombo

if TYPE_CHECKING:
    from dlparse.mono.manager import AssetManager

__all__ = ("AttackingActionTransformer",)


class AttackingActionTransformer:
    """
    Attacking action transformer.

    This transforms the items below to be exported:

    - Normal attack combo
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, asset_manager: "AssetManager"):
        self._asset_manager: "AssetManager" = asset_manager

    @staticmethod
    def _is_allowed_empty_combo(action_id: int) -> bool:
        return action_id in [10183140]

    def transform_normal_attack_or_fs(
            self, root_action_id: int, level: int = None, /,
            ability_ids: list[int] = None
    ) -> Optional[NormalAttackChain]:
        """Get the normal attack or FS info rooted from ``root_action_id``."""
        try:
            current_prefab = self._asset_manager.loader_action.get_prefab(root_action_id)
        except ActionDataNotFoundError as ex:
            if self._is_allowed_empty_combo(root_action_id):
                return NormalAttackChain([])

            raise ex

        parsed_action_ids = set()
        combos = []

        while current_prefab.action_id not in parsed_action_ids:
            combo = NormalAttackCombo(self._asset_manager, current_prefab, level=level, ability_ids=ability_ids)
            combos.append(combo)

            parsed_action_ids.add(current_prefab.action_id)

            # Next prefab
            if not combo.next_combo_action_id:
                break
            current_prefab = self._asset_manager.loader_action.get_prefab(combo.next_combo_action_id)

        return NormalAttackChain(combos)
