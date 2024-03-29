from dlparse.enums import ConditionComposite, SkillCancelAction, SkillCancelType
from dlparse.model import SkillCancelActionUnit
from dlparse.mono.manager import AssetManager


def test_ult_cancel_action(asset_manager: AssetManager):
    data = {
        "Arsene": (20050522, 10138150, 3.30000019, SkillCancelAction.MOTION_ENDS),
        "Mars": (20050113, 90009150, 2.066667, SkillCancelAction.ANY_ACTION),  # Expect 2.2
        "Gozu Tenno": (20050116, 10136150, 2.0, SkillCancelAction.ANY_ACTION)
    }

    dragon_id, action_id, stop_time, cancel_action = data["Mars"]

    prefab = asset_manager.loader_action.get_prefab(action_id)

    units = SkillCancelActionUnit.from_player_action_motion(
        asset_manager.loader_dragon_motion, asset_manager.asset_dragon_data.get_data_by_id(dragon_id), prefab
    )
    assert units == [SkillCancelActionUnit(
        action=cancel_action,
        action_id=None,
        cancel_type=SkillCancelType.NONE,
        time=stop_time,
        pre_conditions=ConditionComposite(),
    )]
