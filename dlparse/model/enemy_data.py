"""Models for an enemy info."""
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING

from .enemy_info import EnemyInfoSingle

if TYPE_CHECKING:
    from dlparse.mono.asset import EnemyParamEntry
    from dlparse.mono.manager import AssetManager

__all__ = ("EnemyData",)


@dataclass
class EnemyData:
    """
    Transformed enemy data.

    This contains the data in different forms of a single enemy.

    Note that if ``enemy_param`` is the 2nd form,
    ``forms`` will only contain 1 enemy info, instead of 2.
    Therefore, it's recommended to instantiate with the 1st form.
    """

    asset_manager: InitVar["AssetManager"]

    enemy_param: "EnemyParamEntry"

    forms: list[EnemyInfoSingle] = field(init=False)

    def __post_init__(self, asset_manager: "AssetManager"):
        current = self.enemy_param
        self.forms = [EnemyInfoSingle(asset_manager, current)]

        while current.form_2nd_param_id:
            current = asset_manager.asset_enemy_param.get_data_by_id(current.form_2nd_param_id)
            self.forms.append(EnemyInfoSingle(asset_manager, current))

    @property
    def form_count(self) -> int:
        """
        Total form count of this enemy.

        In general, Agito expert will have ``2``.
        """
        return len(self.forms)
