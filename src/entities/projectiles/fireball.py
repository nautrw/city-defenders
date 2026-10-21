import pygame

from src.core.utils import load_asset
from src.entities.effects import BurningEffect
from src.entities.enemies.enemy import Enemy
from src.entities.projectiles.ballistic_projectile import BallisticProjectile
from src.entities.projectiles.explosion import Explosion


class Fireball(BallisticProjectile):
    def __init__(
        self, damage: float, x_position: float, y_position: float, target: Enemy
    ) -> None:
        image = load_asset("fireball")

        super().__init__(
            x_position=x_position,
            y_position=y_position,
            target=target,
            image=image,
            damage=damage,
            explode_on_target_collision=True,
            effect_on_collide=BurningEffect,
        )

    def _handle_collision(
        self, enemies_group: pygame.sprite.Group, explosions_group: pygame.sprite.Group
    ) -> None:
        if not self.hit_target and self.target in pygame.sprite.spritecollide(
            self, enemies_group, False
        ):
            self.target.health -= self.damage

            if self.explode_on_target_collision:
                assert self.target.rect is not None
                explosion = Explosion(
                    self.damage,
                    self.target.rect.centerx,
                    self.target.rect.centery,
                    burn=True,
                )
                explosions_group.add(explosion)

            if self.effect_on_collide:
                # self.effect_on_collide is meant to be a subclass, and those
                # dont take duration so its ignored here
                effect = self.effect_on_collide(damage_over_time=self.damage)  # ty:ignore[missing-argument]
                self.target.add_effect(effect)

            self.kill()
            return
