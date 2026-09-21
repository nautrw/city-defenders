import pygame

from src.core.utils import load_asset
from src.entities.projectiles.ice_shard import IceShard
from src.entities.towers.tower import Tower


class FrostspireTower(Tower):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    display_name = "Frostspire"
    description = (
        "Slows down enemies by making them cold. Does not damage enemies by itself."
    )
    initial_cost = 250

    def __init__(self, x_position: int, y_position: int) -> None:
        image = [load_asset("frostspire_0")]

        super().__init__(
            display_name=self.display_name,
            description=self.description,
            cost=[self.initial_cost, 300, 450],
            damage=[0, 0, 0],
            x_position=x_position,
            y_position=y_position,
            tower_image=image,
            projectile=IceShard,
            shooting_speed=[5, 3, 2],
            area_radius=[75, 150, 200],
        )
