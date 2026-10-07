from typing import ClassVar
import pygame

from src.core.utils import load_asset
from src.entities.projectiles.venom_spit import VenomSpit
from src.entities.towers.tower import Tower


class VenomShooterTower(Tower):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    display_name = "Venom Shooter"
    description = (
        "Shoots drops of venom at enemies, poisoning them and damaging them over time."
    )
    cost: ClassVar[tuple[int, ...]] = (155, 215, 295)
    damage: ClassVar[tuple[float, ...]] = (1.5, 2.5, 4)
    shooting_speed: ClassVar[tuple[float, ...]] = (2.4, 1.9, 1.5)
    area_radius: ClassVar[tuple[float, ...]] = (115, 145, 175)

    def __init__(self, x_position: int, y_position: int) -> None:
        images = [
            load_asset("venomshooter_0"),
            load_asset("venomshooter_1"),
            load_asset("venomshooter_2"),
        ]

        super().__init__(
            display_name=self.display_name,
            description=self.description,
            cost=self.cost,
            damage=self.damage,
            x_position=x_position,
            y_position=y_position,
            tower_image=images,
            projectile=VenomSpit,
            shooting_speed=self.shooting_speed,
            area_radius=self.area_radius,
        )
