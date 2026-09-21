import pygame

from src.core.utils import load_asset
from src.entities.projectiles.arrow import Arrow
from src.entities.towers.tower import Tower


class CrossbowTower(Tower):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    display_name = "Crossbow"
    description = "An automatic crossbow. Slowly shoots arrows at enemies."
    initial_cost = 100

    def __init__(self, x_position: int, y_position: int) -> None:
        images = [load_asset("crossbow_0"), load_asset("crossbow_1"), load_asset("crossbow_2")]

        super().__init__(
            display_name=self.display_name,
            description=self.description,
            cost=[self.initial_cost, 150, 200],
            damage=[5, 10, 15],
            x_position=x_position,
            y_position=y_position,
            tower_image=images,
            projectile=Arrow,
            shooting_speed=[1.5, 1, 0.5],
            area_radius=[75, 150, 225],
        )
