import pygame

from src.core.utils import load_asset
from src.entities.projectiles.arrow import Arrow
from src.entities.turrets.turret import Turret


class CrossbowTurret(Turret):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    display_name = "Crossbow"
    description = "An automatic crossbow. Slowly shoots arrows at enemies."
    cost = 100

    def __init__(self, x_position: int, y_position: int):
        image = load_asset("crossbow")

        super().__init__(
            display_name=self.display_name,
            description=self.description,
            cost=self.cost,
            x_position=x_position,
            y_position=y_position,
            turret_image=image,
            projectile=Arrow,
            shooting_speed=1.25,
            area_radius=50,
        )
