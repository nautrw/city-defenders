import pygame

from src.core.utils import load_asset
from src.entities.projectiles.ice_shard import IceShard
from src.entities.turrets.turret import Turret


class Frostspire(Turret):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    display_name = "Frostspire"
    description = "Slows down enemies by making them cold."
    cost = 250

    def __init__(self, x_position: int, y_position: int):
        image = load_asset("frostspire")

        super().__init__(
            display_name=self.display_name,
            description=self.description,
            cost=self.cost,
            damage=0,
            x_position=x_position,
            y_position=y_position,
            turret_image=image,
            projectile=IceShard,
            shooting_speed=5,
            area_radius=75,
        )
