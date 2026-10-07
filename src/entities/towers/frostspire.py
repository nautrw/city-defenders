from typing import ClassVar
import pygame

from src.core.utils import load_asset
from src.entities.projectiles.ice_shard import IceShard
from src.entities.towers.tower import Tower


class FrostspireTower(Tower):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    display_name = "Frostspire"
    description = (
        "Slows down enemies by making them cold. Does not damage enemies by itself."
    )
    cost: ClassVar[tuple[int, ...]] = (145, 205, 285)
    damage: ClassVar[tuple[float, ...]] = (0, 0, 0)
    shooting_speed: ClassVar[tuple[float, ...]] = (2.6, 2.1, 1.6)
    area_radius: ClassVar[tuple[float, ...]] = (105, 135, 165)

    def __init__(self, x_position: int, y_position: int) -> None:
        images = [
            load_asset("frostspire_0"),
            load_asset("frostspire_1"),
            load_asset("frostspire_2"),
        ]

        super().__init__(
            display_name=self.display_name,
            description=self.description,
            cost=self.cost,
            damage=self.damage,
            x_position=x_position,
            y_position=y_position,
            tower_image=images,
            projectile=IceShard,
            shooting_speed=self.shooting_speed,
            area_radius=self.area_radius,
        )
