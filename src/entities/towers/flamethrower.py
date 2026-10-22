from typing import ClassVar

from src.core.utils import load_asset
from src.entities.projectiles.ballistic_projectile import BallisticProjectileType
from src.entities.projectiles.fireball import Fireball
from src.entities.towers.tower import Tower


class FlamethrowerTower(Tower):
    display_name = "Flamethrower"
    description = "Shoots fireballs fireballs at enemies. Causes damage to multiple enemies and makes them burn."

    cost: ClassVar[tuple[int, ...]] = (350, 470, 620)
    damage: ClassVar[tuple[float, ...]] = (5, 7, 10)
    shooting_speed: ClassVar[tuple[float, ...]] = (2.5, 2.0, 1.6)
    area_radius: ClassVar[tuple[float, ...]] = (135, 165, 195)
    shards_cost: ClassVar[int] = 425

    projectile: ClassVar[BallisticProjectileType] = Fireball

    def __init__(self, x_position: int, y_position: int) -> None:
        images = [
            load_asset("flamethrower_0"),
            load_asset("flamethrower_1"),
            load_asset("flamethrower_2"),
        ]

        super().__init__(
            x_position=x_position,
            y_position=y_position,
            tower_image=images,
        )
