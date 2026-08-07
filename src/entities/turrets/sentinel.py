import pygame
from src.core.base_turret import BaseTurret

class SentinelTurret(BaseTurret):
    # pygame.Sprite defaults these two to None and by LSP will scream at me
    # if I don't put these
    rect: pygame.Rect | pygame.FRect
    image: pygame.Surface

    def __init__(self):
        super().__init__(attachment_center=(7, 33))

        self.image = pygame.image.load("src/assets/turrets/basic_turret.png") 
        self.rect = self.image.get_rect()
