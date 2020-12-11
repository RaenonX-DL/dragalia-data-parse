"""
Player action component classes.

Check the document at ``notes/assets/player_action_components.md`` for details of each type of the components.
"""
from .buff_bomb import ActionBuffBomb
from .buff_field import ActionBuffField
from .bullet import ActionBullet
from .bullet_arrange import ActionBulletArranged
from .bullet_multi import ActionBulletMulti
from .bullet_stock_fire import ActionBulletStockFire
from .parts_list import ActionPartsListAsset, ActionPartsListEntry
from .prefab import PlayerActionPrefab
from .set_hit import ActionSettingHit
