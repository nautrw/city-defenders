import pygame

from src.core.utils import load_asset
from src.entities.enemies.enemy import Enemy


class FastSlime(Enemy):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self, path_waypoints: list[tuple[float, float]]):
        animation = [load_asset("fastslime1"), load_asset("fastslime2")]

        super().__init__(
            animation=animation,
            movement_speed=150,
            animation_duration=0.1,
            max_health=10,
            path_waypoints=path_waypoints,
            coins_drop=30,
        )
