import pygame
from src.core.base_ship import BaseShip
from src.core.base_turret import BaseTurret

class CorvetteShip(BaseShip):
    # pygame.Sprite defaults these two to None and by LSP will scream at me
    # if I don't put these
    rect: pygame.Rect | pygame.FRect
    image: pygame.Surface


    def __init__(self, turrets: list[BaseTurret]):
        super().__init__()

        self.display_name: str = "Corvette"
        self.description: str = "A basic spaceship. Nothing much to see here."

        self.image = pygame.image.load("src/assets/ships/corvette.png")
        self.rect = self.image.get_rect()

        self.equipped_turrets = turrets
        self.mounting_points = ((36, 57),) # 1 turret
