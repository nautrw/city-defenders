import pygame
from .base_gun import BaseGun

class BaseShip(pygame.sprite.Sprite):
    # pygame.Sprite defaults these two to None and by LSP will scream at me
    # if I don't put these
    rect: pygame.Rect | pygame.FRect
    image: pygame.Surface

    def __init__(self):
        super().__init__()

        self.display_name: str
        self.description: str

        self.image: pygame.Surface

        # ((gun1, (x, y), (gun2, (x, y), (gun3, (x, y)))
        self.guns: tuple[tuple[BaseGun, tuple[int | float, int | float]], ...]

    def update(self, delta_time: int | float):
        ...
    
    def draw(self, screen: pygame.Surface):
        for gun_obj, placement in self.guns:
            gun_image = gun_obj.image
            gun_rect = gun_image.get_rect()
            gun_rect.center = placement
            self.image.blit(gun_image, gun_rect)

        screen.blit(self.image, self.rect)
