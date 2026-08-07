import pygame

class BaseTurret(pygame.sprite.Sprite):
    # pygame.Sprite defaults these two to None and by LSP will scream at me
    # if I don't put these
    rect: pygame.Rect | pygame.FRect
    image: pygame.Surface
    
    def __init__(self, attachment_center: tuple[int | float, int | float]):
        super().__init__()
        self.attachment_center = attachment_center

    def update(self, delta_time: int | float):
        ...

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
