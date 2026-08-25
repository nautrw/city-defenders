from turtle import circle
from src.entities.projectiles.arrow import Arrow
from numpy import angle
from os import path

import pygame
from pygame.geometry import Circle

from src.core.utils import angle_to_point
from src.entities.enemies.enemy import Enemy
from src.entities.projectiles.ballistic_projectile import BallisticProjectile
import src.core.config as Config


class Turret(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    # type[BallisticProjectile] allows passing any CLASS that is a subclass of BallisticProjectile
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

    def _shoot_at(self, enemy: Enemy):
        enemy_position = pygame.Vector2(enemy.rect.center)
        projectile = Arrow(self.base_rect.x, self.base_rect.y, enemy_position)
        return projectile

    def draw(self, surface: pygame.Surface, draw_radiuses: bool):
        if draw_radiuses:
            circle_surf = pygame.Surface(self.area.as_rect().size, pygame.SRCALPHA)
            radius = self.area.radius
            pygame.draw.circle(circle_surf, Config.ColorsConfig.turret_radius_color, (radius, radius), radius)
            surface.blit(circle_surf, self.area.as_rect())

        self.turret_image = pygame.transform.rotate(self.original_turret_image, self.turret_angle)
        self.turret_rect = self.turret_image.get_rect(center=self.base_rect.center)

        surface.blit(self.base, self.base_rect)
        surface.blit(self.turret_image, self.turret_rect)

    def update(self, delta_time: float, enemies_group: pygame.sprite.Group, projectiles_group: pygame.sprite.Group):
        for enemy in enemies_group:
            if self.area.colliderect(enemy.rect):
                self.turret_angle = angle_to_point(self.base_rect.center, enemy.rect.center)
                projectile = self._shoot_at(enemy)
                projectiles_group.add(projectile)
