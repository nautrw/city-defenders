from typing import Protocol

import pygame

from src.core.utils import angle_to_point


# protocols are used to describe how a subclass should be
# this also serves for type hinting, like in Turret, where
# type hinting the projectile as BallisticProjectile will cause
# an error because it requires an image, but its subclasses
# dont take an image because they provide it
class BallisticProjectileType(Protocol):
    def __call__(
        self, x_position: float, y_position: float, target_x: float, target_y: float
    ):
        pass


class BallisticProjectile(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(
        self,
        x_position: float,
        y_position: float,
        target_x: float,
        target_y: float,
        image: pygame.Surface,
        movement_speed: int,
        damage: int,
    ):
        super().__init__()

        self.original_image = image
        self.image = self.original_image.copy()
        self.rect = image.get_frect(centerx=x_position, bottom=y_position)

        self.position = pygame.Vector2(x_position, y_position)
        self.velocity = pygame.Vector2()
        self.movement_speed = movement_speed
        self.target = pygame.Vector2(target_x, target_y)

        self.damage = damage

        self.angle = 0

    def update(self, delta_time: float, enemies_group: pygame.sprite.Group) -> None:
        movement = self.target - pygame.Vector2(self.rect.center)

        if movement.length_squared() != 0:
            movement.normalize_ip()

        self.velocity = movement * self.movement_speed
        self.position += self.velocity * delta_time
        self.rect.center = self.position

        self.angle = angle_to_point(
            self.position.x, self.position.y, self.target.x, self.target.y
        )

        if collisions := pygame.sprite.spritecollide(self, enemies_group, False):
            for collision in collisions:
                collision.health -= self.damage

            self.kill()

    def draw(self, surface: pygame.Surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, self.rect)
