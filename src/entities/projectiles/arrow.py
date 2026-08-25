import pygame

from src.core.utils import load_asset
from src.entities.projectiles.ballistic_projectile import BallisticProjectile


class Arrow(BallisticProjectile):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(
        self, x_position: float, y_position: float, target_x: float, target_y: float
    ):
        image = load_asset("arrow")

        super().__init__(
            x_position=x_position,
            y_position=y_position,
            target_x=target_x,
            target_y=target_y,
            image=image,
            movement_speed=10,
            damage=5,
        )
