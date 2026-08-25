import pygame

from src.core.utils import load_asset
from src.entities.enemies.enemy import Enemy


class Slime(Enemy):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self, path_waypoints: list[tuple[float, float]]):
        image = load_asset("slime")

        super().__init__(
            image=image, movement_speed=50, max_health=10, path_waypoints=path_waypoints
        )
