from typing import ClassVar
import pygame

from src.core.utils import load_asset
from src.entities.projectiles.arrow import Arrow
from src.entities.towers.tower import Tower


class CrossbowTower(Tower):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    display_name = "Crossbow"
    description = "An automatic crossbow. Slowly shoots arrows at enemies."
    cost: ClassVar[tuple[float, ...]] = (85, 125, 185)
    damage: ClassVar[tuple[float, ...]] = (7, 11, 17)
    shooting_speed: ClassVar[tuple[float, ...]] = (0.85, 0.65, 0.45)
    area_radius: ClassVar[tuple[float, ...]] = (105, 125, 150)

    def __init__(self, x_position: int, y_position: int) -> None:
        images = [
            load_asset("crossbow_0"),
            load_asset("crossbow_1"),
            load_asset("crossbow_2"),
        ]

        super().__init__(
            display_name=self.display_name,
            description=self.description,
            cost=self.cost,
            damage=self.damage,
            x_position=x_position,
            y_position=y_position,
            tower_image=images,
            projectile=Arrow,
            shooting_speed=self.shooting_speed,
            area_radius=self.area_radius,
        )