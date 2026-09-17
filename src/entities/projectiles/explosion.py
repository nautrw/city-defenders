import pygame

from src.core.utils import load_asset


class Explosion(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(
        self,
        damage: int,
        x_position: float,
        y_position: float,
        duration: float = 0.25,
    ):
        super().__init__()

        self.image = load_asset("explosion")
        self.rect = self.image.get_frect(center=(x_position, y_position))

        self.damage = damage

        self.duration = duration
        self.duration_counter_dt = 0
        self.opacity = 255

        self.hit_enemies = False

    def update(self, delta_time: float, enemies_group: pygame.sprite.Group, game_speed_multiplier: int) -> None:
        if not self.hit_enemies:
            collisions = pygame.sprite.spritecollide(self, enemies_group, False)

            for enemy in collisions:
                enemy.health -= self.damage

            self.hit_enemies = True

        self.duration_counter_dt += delta_time * game_speed_multiplier
        self.opacity = int((self.duration / self.duration_counter_dt) * 255)

    def draw(self, surface: pygame.Surface):
        self.image.set_alpha(self.opacity)
        surface.blit(self.image, self.rect)
