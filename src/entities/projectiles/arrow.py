from os import path

import pygame

from src.core.utils import Coordinate
from src.entities.projectiles.ballistic_projectile import BallisticProjectile


class Arrow(BallisticProjectile):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self, x_position: int, y_position: int, target: Coordinate):
        image = pygame.image.load(path.join("src", "assets", "entities", "projectiles", "arrow.png"))

        super().__init__(x_position=x_position, y_position=y_position, target=target, image=image, movement_speed=50)
