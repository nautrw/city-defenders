import pygame

from src.core.utils import load_asset
from src.entities.enemies.enemy import Enemy
from src.entities.projectiles.ballistic_projectile import BallisticProjectile


class Arrow(BallisticProjectile):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(
        self, damage: float, x_position: float, y_position: float, target: Enemy
    ) -> None:
        image = load_asset("arrow")

        super().__init__(
            x_position=x_position,
            y_position=y_position,
            target=target,
            image=image,
            damage=damage,
        )
