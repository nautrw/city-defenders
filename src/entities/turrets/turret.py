from os import path

import pygame
from pygame.geometry import Circle

from src.entities.projectiles.ballistic_projectile import BallisticProjectile


class Turret(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self, x_position: int, y_position: int, turret_image: pygame.Surface, projectile: type[BallisticProjectile], shooting_speed: float, area_radius: float):
        super().__init__()

        self.position = pygame.Vector2(x_position, y_position)

        self.base = pygame.image.load(path.join("src", "assets", "entities", "turrets", "turret_base.png")).convert_alpha()
        self.original_turret_image = turret_image
        self.turret_image = turret_image.copy()

        self.base_rect = self.base.get_rect(center=self.position)
        self.turret_rect = self.turret_image.get_rect(center=self.position)

        self.projectile = projectile
        self.shooting_speed = shooting_speed

        self.area = Circle(self.base_rect.center, area_radius)

        self.turret_angle = 0

    def draw(self, surface: pygame.Surface):
        self.turret_image = pygame.transform.rotate(self.original_turret_image, self.turret_angle)

        surface.blit(self.base, self.base_rect)
        surface.blit(self.turret_image, self.turret_rect)
