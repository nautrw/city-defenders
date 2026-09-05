import pygame

from src.core.utils import load_asset
from src.entities.enemies.enemy import Enemy


class Slime(Enemy):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self, path_waypoints: list[tuple[float, float]]):
        animation = [load_asset("slime1"), load_asset("slime2")]

        super().__init__(
            animation=animation, movement_speed=50, max_health=10, path_waypoints=path_waypoints, coins_drop=10
        )
