from src.core.utils import load_asset
from src.entities.enemies.enemy import Enemy


class FastSlime(Enemy):
    def __init__(self, path_waypoints: list[tuple[float, float]]) -> None:
        animation = [load_asset("fastslime1"), load_asset("fastslime2")]

        super().__init__(
            animation=animation,
            movement_speed=90,
            animation_duration=0.15,
            max_health=24,
            path_waypoints=path_waypoints,
            coins_drop=18,
        )
