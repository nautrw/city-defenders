import pygame

from src.core.utils import load_asset
from src.entities.projectiles.bolt import Bolt
from src.entities.towers.tower import Tower


class BallistaTower(Tower):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    display_name = "Ballista"
    description = "Shoots bolts at a slow rate but with great force."
    initial_cost = 150

    def __init__(self, x_position: int, y_position: int) -> None:
        images = [
            load_asset("ballista_0"),
            load_asset("ballista_1"),
            load_asset("ballista_2"),
        ]

        super().__init__(
            display_name=self.display_name,
            description=self.description,
            cost=[self.initial_cost, 200, 250],
            damage=[10, 15, 25],
            x_position=x_position,
            y_position=y_position,
            tower_image=images,
            projectile=Bolt,
            shooting_speed=[2.5, 2, 1.5],
            area_radius=[75, 150, 200],
        )
