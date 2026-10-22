from typing import ClassVar

from src.core.utils import load_asset
from src.entities.projectiles.arrow import Arrow
from src.entities.projectiles.ballistic_projectile import BallisticProjectileType
from src.entities.towers.tower import Tower


class CrossbowTower(Tower):
    display_name = "Crossbow"
    description = "An automatic crossbow. Slowly shoots arrows at enemies."

    cost: ClassVar[tuple[int, ...]] = (95, 145, 210)
    damage: ClassVar[tuple[float, ...]] = (6, 9, 12)
    shooting_speed: ClassVar[tuple[float, ...]] = (0.95, 0.72, 0.52)
    area_radius: ClassVar[tuple[float, ...]] = (95, 115, 135)
    shards_cost: ClassVar[int] = 0

    projectile: ClassVar[BallisticProjectileType] = Arrow


    def __init__(self, x_position: int, y_position: int) -> None:
        images = [
            load_asset("crossbow_0"),
            load_asset("crossbow_1"),
            load_asset("crossbow_2"),
        ]

        super().__init__(
            x_position=x_position,
            y_position=y_position,
            tower_image=images,
        )
