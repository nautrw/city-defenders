import pygame

from src.core.utils import load_asset
from src.entities.enemies.enemy import Enemy


class Bat(Enemy):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self, path_waypoints: list[tuple[float, float]]) -> None:
        animation = [load_asset("bat1"), load_asset("bat2")]

        super().__init__(
            animation=animation,
            movement_speed=125,
            animation_duration=0.125,
            max_health=9,
            path_waypoints=path_waypoints,
            coins_drop=18,
        )
