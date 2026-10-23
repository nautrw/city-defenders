from typing import ClassVar

from src.core.utils import load_asset
from src.entities.projectiles.ballistic_projectile import BallisticProjectileType
from src.entities.projectiles.cannon_ball import CannonBall
from src.entities.towers.tower import Tower


class CannonTower(Tower):
    display_name = "Cannon"
    description = "Shoots cannon balls at turrets. Explosion does massive amounts of damage to multiple enemies."

    cost: ClassVar[tuple[int, ...]] = (195, 225, 300)
    damage: ClassVar[tuple[float, ...]] = (22, 26, 30)
    shooting_speed: ClassVar[tuple[float, ...]] = (2.5, 2.0, 1.5)
    area_radius: ClassVar[tuple[float, ...]] = (110, 135, 160)
    shards_cost: ClassVar[int] = 150

    projectile: ClassVar[BallisticProjectileType] = CannonBall

    def __init__(self, x_position: int, y_position: int) -> None:
        images = [
            load_asset("cannon_0"),
            load_asset("cannon_1"),
            load_asset("cannon_2"),
        ]

        super().__init__(
            x_position=x_position,
            y_position=y_position,
            tower_image=images,
        )
