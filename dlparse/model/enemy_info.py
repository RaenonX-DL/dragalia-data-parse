"""Models for an enemy info."""
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING

from dlparse.enums import Element, Status

if TYPE_CHECKING:
    from dlparse.mono.asset import EnemyParamEntry
    from dlparse.mono.manager import AssetManager

__all__ = ("EnemyInfoSingle",)


@dataclass
class EnemyInfoSingle:
    """
    Single transformed enemy info.

    Note that this does not handle the 2nd form of the enemy.
    Please refer to the ``forms`` field of :class:`EnemyData` for more details.
    """

    asset_manager: InitVar["AssetManager"]

    enemy_param: "EnemyParamEntry"

    enemy_param_id: int = field(init=False)
    initial_element: Element = field(init=False)

    hp: int = field(init=False)
    defense: int = field(init=False)
    base_od: int = field(init=False)
    base_bk: int = field(init=False)
    od_def_rate: float = field(init=False)
    od_atk_rate: float = field(init=False)
    bk_def_rate: float = field(init=False)
    bk_duration_sec: float = field(init=False)

    affliction_resistance_pct: dict[Status, int] = field(init=False)

    parts: list["EnemyInfoSingle"] = field(init=False)
    children: list["EnemyInfoSingle"] = field(init=False)

    def __post_init__(self, asset_manager: "AssetManager"):
        enemy_data = asset_manager.asset_enemy_data.get_data_by_id(self.enemy_param.enemy_data_id)

        self.enemy_param_id = self.enemy_param.id
        self.initial_element = enemy_data.initial_element
        self.hp = self.enemy_param.hp
        self.defense = self.enemy_param.defense
        self.base_od = self.enemy_param.base_od
        self.base_bk = self.enemy_param.base_bk
        self.od_def_rate = enemy_data.od_def_rate or 1.0  # `0` in enemy data means no change
        self.od_atk_rate = enemy_data.od_atk_rate
        self.bk_def_rate = enemy_data.bk_def_rate
        self.bk_duration_sec = enemy_data.bk_duration_sec
        self.affliction_resistance_pct = self.enemy_param.affliction_resistance_pct

        self.parts = [
            EnemyInfoSingle(asset_manager, asset_manager.asset_enemy_param.get_data_by_id(part_param_id))
            for part_param_id in self.enemy_param.part_param_ids
        ]
        self.children = [
            EnemyInfoSingleChildren(
                asset_manager=asset_manager,
                enemy_param=asset_manager.asset_enemy_param.get_data_by_id(child_param_id),
                count=child_count
            )
            for child_param_id, child_count in self.enemy_param.children_param_ids_and_count
        ]


@dataclass
class EnemyInfoSingleChildren(EnemyInfoSingle):
    """Single transformed enemy children info."""

    count: int
