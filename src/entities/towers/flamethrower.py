from src.entities.enemies.enemy import Enemy
from typing import ClassVar

import pygame

from src.core.utils import load_asset
from src.entities.projectiles.ballistic_projectile import BallisticProjectileType, BallisticProjectile
from src.entities.projectiles.fireball import Fireball
from src.entities.towers.tower import Tower


class FlamethrowerTower(Tower):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    display_name = "Flamethrower"
    description = "Shoots fireballs fireballs at enemies. Causes damage to multiple enemies and makes them burn."
    cost: ClassVar[tuple[int, ...]] = (175, 240, 330)
    damage: ClassVar[tuple[float, ...]] = (2, 5, 7)
    shooting_speed: ClassVar[tuple[float, ...]] = (2.8, 2.3, 1.8)
    area_radius: ClassVar[tuple[float, ...]] = (115, 140, 165)

    projectile: ClassVar[BallisticProjectileType] = Fireball

    shards_cost: ClassVar[int] = 20

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