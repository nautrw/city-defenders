from src.core.utils import load_asset
from src.entities.enemies.enemy import Enemy


class Phantom(Enemy):
    def __init__(self, path_waypoints: list[tuple[float, float]]) -> None:
        animation = [
            load_asset("phantom1"),
            load_asset("phantom2"),
            load_asset("phantom3"),
            load_asset("phantom4"),
            load_asset("phantom5"),
            load_asset("phantom4"),
            load_asset("phantom3"),
            load_asset("phantom2"),
        ]

        super().__init__(
            animation=animation,
            movement_speed=82,
            max_health=45,
            path_waypoints=path_waypoints,
            coins_drop=30,
        )
