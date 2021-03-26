"""Models for a quest data."""
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING

from dlparse.enums import Element, QuestMode

if TYPE_CHECKING:
    from dlparse.mono.asset import QuestDataEntry
    from dlparse.mono.manager import AssetManager

__all__ = ("QuestData",)


@dataclass
class QuestData:
    """A transformed quest data."""

    asset_manager: InitVar["AssetManager"]

    quest_data: "QuestDataEntry"

    quest_mode: QuestMode = field(init=False)
    elements: list[Element] = field(init=False)
    elements_limit: list[Element] = field(init=False)

    max_clear_time_sec: int = field(init=False)
    max_revive_allowed: int = field(init=False)
    area_1_name: str = field(init=False)
    spawn_enemy_param_ids: list[int] = field(init=False)

    def __post_init__(self, asset_manager: "AssetManager"):
        # Quest basic properties
        self.quest_mode = self.quest_data.quest_mode
        self.elements = [
            Element(elem) for elem
            in (self.quest_data.element_1, self.quest_data.element_2)
            if elem.is_valid
        ]
        self.elements_limit = [
            Element(elem) for elem
            in (self.quest_data.element_1_limit, self.quest_data.element_2_limit)
            if elem.is_valid
        ]

        self.max_clear_time_sec = self.quest_data.max_time_sec
        self.max_revive_allowed = self.quest_data.max_revive

        # Quest dungeon area
        self.area_1_name = self.quest_data.area_1_name
        dungeon_plan = asset_manager.asset_dungeon_planner.get_data_by_id(self.area_1_name)

        # --- ``variation_idx`` is 1-based index

        self.spawn_enemy_param_ids = dungeon_plan.enemy_param_ids[self.quest_data.variation_idx - 1]
        if not self.spawn_enemy_param_ids:
            # In Legend Ciella quest, variation type is 4 while the only enemy parameter related is located at 0
            # This will attempt to take the data at variation 0
            self.spawn_enemy_param_ids = dungeon_plan.enemy_param_ids[0]
