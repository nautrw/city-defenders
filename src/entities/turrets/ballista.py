import pygame

from src.core.utils import load_asset
from src.entities.projectiles.arrow import Arrow
from src.entities.turrets.turret import Turret


class BallistaTurret(Turret):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    display_name = "Ballista"
    description = "Shoots bolts at a slow rate but with great force."
    cost = 250

    def __init__(self, x_position: int, y_position: int):
        image = load_asset("ballista")

        super().__init__(
            display_name=self.display_name,
            description=self.description,
            cost=self.cost,
            x_position=x_position,
            y_position=y_position,
            turret_image=image,
            projectile=Arrow,
            shooting_speed=2.5,
            area_radius=75,
        )
