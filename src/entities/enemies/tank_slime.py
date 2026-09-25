from src.entities.health_bar import HealthBar
import pygame

from src.core.utils import load_asset
from src.entities.enemies.enemy import Enemy
import src.core.config as Config


class TankSlime(Enemy):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self, path_waypoints: list[tuple[float, float]]) -> None:
        animation = [load_asset("tankslime1"), load_asset("tankslime2")]

        super().__init__(
            animation=animation,
            movement_speed=10,
            animation_duration=0.25,
            max_health=100,
            path_waypoints=path_waypoints,
            coins_drop=250,
        )

        self.health_bar = HealthBar(
            width=Config.DEFAULT_HEALTH_BAR_WIDTH * 2,
            height=Config.DEFAULT_HEALTH_BAR_HEIGHT * 2,
        )
