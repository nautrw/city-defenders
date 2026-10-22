from typing import ClassVar

from src.core.utils import load_asset
from src.entities.projectiles.ballistic_projectile import BallisticProjectileType
from src.entities.projectiles.bolt import Bolt
from src.entities.towers.tower import Tower


class BallistaTower(Tower):
    display_name = "Ballista"
    description = "Shoots bolts at a slow rate but with great force."

    cost: ClassVar[tuple[int, ...]] = (130, 160, 200)
    damage: ClassVar[tuple[float, ...]] = (24, 38, 54)
    shooting_speed: ClassVar[tuple[float, ...]] = (2.2, 1.8, 1.45)
    area_radius: ClassVar[tuple[float, ...]] = (135, 160, 185)

    projectile: ClassVar[BallisticProjectileType] = Bolt

    shards_cost: ClassVar[int] = 75

    def __init__(self, x_position: int, y_position: int) -> None:
        images = [
            load_asset("ballista_0"),
            load_asset("ballista_1"),
            load_asset("ballista_2"),
        ]

        super().__init__(
            x_position=x_position,
            y_position=y_position,
            tower_image=images,
        )
