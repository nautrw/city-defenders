import pygame

from src.core.utils import Coordinate

class BallisticProjectile(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self, x_position: int, y_position: int, target: Coordinate, image: pygame.Surface, movement_speed: int):
        super().__init__()

        self.image = image
        self.rect = image.get_rect(centerx=x_position, bottom=y_position)

        self.position = pygame.Vector2(x_position, y_position)
        self.velocity = pygame.Vector2()
        self.movement_speed = movement_speed
        self.target = target

    def update(self, dt: float) -> None:
        movement = self.target - pygame.Vector2(self.rect.center)

        self.velocity = movement * self.movement_speed
        self.position += self.velocity * dt
        self.rect.center = self.position
