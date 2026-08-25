from os import path

import pygame

from src.entities.projectiles.arrow import Arrow
from src.entities.turrets.turret import Turret


class CrossbowTurret(Turret):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self, x_position: int, y_position: int):
        image = pygame.image.load(
            path.join("src", "assets", "entities", "turrets", "crossbow.png")
        )

        super().__init__(
            x_position=x_position,
            y_position=y_position,
            turret_image=image,
            projectile=Arrow,
            shooting_speed=1.25,
            area_radius=50,
        )
