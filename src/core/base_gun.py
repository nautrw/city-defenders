import pygame

class BaseGun(pygame.sprite.Sprite):
    # pygame.Sprite defaults these two to None and by LSP will scream at me
    # if I don't put these
    rect: pygame.Rect | pygame.FRect
    image: pygame.Surface
    
    def __init__(self, attachment_center_x: int | float, attachment_center_y: int | float):
        super().__init__()

    def update(self, delta_time: int | float):
        ...

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
