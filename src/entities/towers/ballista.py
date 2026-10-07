from typing import ClassVar

import pygame

from src.core.utils import load_asset
from src.entities.projectiles.bolt import Bolt
from src.entities.towers.tower import Tower


class BallistaTower(Tower):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    display_name = "Ballista"
    description = "Shoots bolts at a slow rate but with great force."
    cost: ClassVar[tuple[int, ...]] = (135, 185, 260)
    damage: ClassVar[tuple[float, ...]] = (24, 38, 58)
    shooting_speed: ClassVar[tuple[float, ...]] = (2.0, 1.65, 1.3)
    area_radius: ClassVar[tuple[float, ...]] = (150, 175, 205)

    def __init__(self, x_position: int, y_position: int) -> None:
        images = [
            load_asset("ballista_0"),
            load_asset("ballista_1"),
            load_asset("ballista_2"),
        ]

        super().__init__(
            display_name=self.display_name,
            description=self.description,
            cost=self.cost,
            damage=self.damage,
            x_position=x_position,
            y_position=y_position,
            tower_image=images,
            projectile=Bolt,
            shooting_speed=self.shooting_speed,
            area_radius=self.area_radius,
        )
