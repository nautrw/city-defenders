import pygame

from src.core.utils import load_asset
from src.entities.projectiles.cannon_ball import CannonBall
from src.entities.towers.tower import Tower


class CannonTower(Tower):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    display_name = "Cannon"
    description = "Shoots cannon balls at turrets. Explosion does massive amounts of damage to multiple enemies."
    initial_cost = 175

    def __init__(self, x_position: int, y_position: int) -> None:
        images = [
            load_asset("cannon_0"),
            load_asset("cannon_1"),
            load_asset("cannon_2"),
        ]

        super().__init__(
            display_name=self.display_name,
            description=self.description,
            cost=[self.initial_cost, 240, 330],
            damage=[22, 35, 52],
            x_position=x_position,
            y_position=y_position,
            tower_image=images,
            projectile=CannonBall,
            shooting_speed=[2.8, 2.3, 1.8],
            area_radius=[115, 140, 165],
        )
