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
    initial_cost = 250

    def __init__(self, x_position: int, y_position: int) -> None:
        image = [
            load_asset("venomshooter_0"),
            load_asset("venomshooter_1"),
            load_asset("venomshooter_2"),
        ]

        super().__init__(
            display_name=self.display_name,
            description=self.description,
            cost=[self.initial_cost, 300, 450],
            damage=[0.1, 0.2, 0.3],
            x_position=x_position,
            y_position=y_position,
            tower_image=image,
            projectile=VenomSpit,
            shooting_speed=[5, 3, 2],
            area_radius=[75, 150, 200],
        )
