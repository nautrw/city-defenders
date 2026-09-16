from cmath import e
from typing import Protocol

import pygame

from src.core.utils import angle_to_point
from src.entities.enemies.enemy import Enemy
from src.entities.projectiles.explosion import Explosion


# protocols are used to describe how a subclass should be
# this also serves for type hinting, like in Turret, where
# type hinting the projectile as BallisticProjectile will cause
# an error because it requires an image, but its subclasses
# dont take an image because they provide it
class BallisticProjectileType(Protocol):
    def __call__(
        self, damage: int, x_position: float, y_position: float, target: Enemy
    ):
        pass


class BallisticProjectile(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(
        self,
        damage: int,
        x_position: float,
        y_position: float,
        target: Enemy,
        image: pygame.Surface,
        explode_on_target_collision: bool = False,
    ):
        super().__init__()

        self.original_image = image
        self.image = self.original_image.copy()
        self.rect = image.get_frect(centerx=x_position, bottom=y_position)

        self.position = pygame.Vector2(x_position, y_position)
        self.velocity = pygame.Vector2()

        self.target = target

        self.damage = damage
        self.hit_target = False

        self.explode_on_target_collision = explode_on_target_collision

        self.angle = 0

    def update(
        self,
        delta_time: float,
        enemies_group: pygame.sprite.Group,
        explosions_group: pygame.sprite.Group,
    ) -> None:
        # makes the arrow dissapear if the target is killed by another turret
        if not self.target.alive():
            self.kill()
            return

        target_pos = pygame.Vector2(self.target.rect.center)
        movement = target_pos - self.position

        if movement.length_squared() != 0:
            movement.normalize_ip()

        move_speed = 200
        self.velocity = movement * move_speed
        self.position += self.velocity * delta_time
        self.rect.center = self.position

        self.angle = angle_to_point(
            self.position.x,
            self.position.y,
            self.target.position.x,
            self.target.position.y,
        )

        if not self.hit_target and self.target in pygame.sprite.spritecollide(
            self, enemies_group, False
        ):
            self.target.health -= self.damage

            if self.explode_on_target_collision:
                explosion = Explosion(
                    self.damage, self.target.rect.centerx, self.target.rect.centery
                )
                explosions_group.add(explosion)

            self.kill()
            return

    def draw(self, surface: pygame.Surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, self.rect)
