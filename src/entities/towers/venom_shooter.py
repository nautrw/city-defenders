from typing import ClassVar

from src.core.utils import load_asset
from src.entities.projectiles.ballistic_projectile import BallisticProjectileType
from src.entities.projectiles.venom_spit import VenomSpit
from src.entities.towers.tower import Tower


class VenomShooterTower(Tower):
    display_name = "Venom Shooter"
    description = (
        "Shoots drops of venom at enemies, poisoning them and damaging them over time."
    )

    cost: ClassVar[tuple[int, ...]] = (290, 390, 510)
    damage: ClassVar[tuple[float, ...]] = (4, 6, 8)
    shooting_speed: ClassVar[tuple[float, ...]] = (1.9, 1.5, 1.2)
    area_radius: ClassVar[tuple[float, ...]] = (130, 160, 190)
    shards_cost: ClassVar[int] = 330

    projectile: ClassVar[BallisticProjectileType] = VenomSpit

    def __init__(self, x_position: int, y_position: int) -> None:
        images = [
            load_asset("venomshooter_0"),
            load_asset("venomshooter_1"),
            load_asset("venomshooter_2"),
        ]

        super().__init__(
            x_position=x_position,
            y_position=y_position,
            tower_image=images,
        )
