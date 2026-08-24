import pygame


class Enemy(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self, image: pygame.Surface, movement_speed: int, max_health: int):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()

        self.movement_speed = movement_speed
        self.max_health = max_health
        self.health = max_health

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
