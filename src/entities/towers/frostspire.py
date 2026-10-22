from typing import ClassVar

from src.core.utils import load_asset
from src.entities.projectiles.ballistic_projectile import BallisticProjectileType
from src.entities.projectiles.ice_shard import IceShard
from src.entities.towers.tower import Tower


class FrostspireTower(Tower):
    display_name = "Frostspire"
    description = (
        "Slows down enemies by making them cold. Does not damage enemies by itself."
    )

    cost: ClassVar[tuple[int, ...]] = (240, 325, 430)
    damage: ClassVar[tuple[float, ...]] = (0, 0, 0)
    shooting_speed: ClassVar[tuple[float, ...]] = (2.0, 1.55, 1.2)
    area_radius: ClassVar[tuple[float, ...]] = (135, 165, 200)
    shards_cost: ClassVar[int] = 240

    projectile: ClassVar[BallisticProjectileType] = IceShard

    def __init__(self, x_position: int, y_position: int) -> None:
        images = [
            load_asset("frostspire_0"),
            load_asset("frostspire_1"),
            load_asset("frostspire_2"),
        ]

        super().__init__(
            x_position=x_position,
            y_position=y_position,
            tower_image=images,
        )
