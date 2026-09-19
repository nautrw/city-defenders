import pygame

from src.core.utils import load_asset
from src.entities.projectiles.cannon_ball import CannonBall
from src.entities.turrets.turret import Turret


class CannonTurret(Turret):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    display_name = "Cannon"
    description = "Shoots cannon balls at turrets. Explosion does massive amounts of damage to multiple enemies."
    initial_cost = 100

    def __init__(self, x_position: int, y_position: int):
        image = load_asset("cannon")

        super().__init__(
            display_name=self.display_name,
            description=self.description,
            cost=[self.initial_cost, 500, 700],
            damage=[15, 25, 40],
            x_position=x_position,
            y_position=y_position,
            turret_image=image,
            projectile=CannonBall,
            shooting_speed=[3, 2, 1],
            area_radius=[75, 150, 200],
        )
