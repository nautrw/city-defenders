import pygame

from src.core.utils import load_asset
from src.entities.enemies.enemy import Enemy


class Ghost(Enemy):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self, path_waypoints: list[tuple[float, float]]) -> None:
        animation = [
            load_asset("ghost1"),
            load_asset("ghost2"),
            load_asset("ghost3"),
            load_asset("ghost4"),
            load_asset("ghost5"),
            load_asset("ghost4"),
            load_asset("ghost3"),
            load_asset("ghost2"),
        ]

        super().__init__(
            animation=animation,
            movement_speed=50,
            max_health=10,
            path_waypoints=path_waypoints,
            coins_drop=25,
        )
