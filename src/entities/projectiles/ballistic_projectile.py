import pygame

from src.core.utils import Coordinate, angle_to_point


class BallisticProjectile(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self, position: Coordinate, target: Coordinate, image: pygame.Surface, movement_speed: int, damage: int):
        super().__init__()

        self.original_image = image
        self.image = self.original_image.copy()
        self.rect = image.get_rect(centerx=position[0], bottom=position[1])

        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2()
        self.movement_speed = movement_speed
        self.target = target

        self.damage = damage
        
        self.angle = 0

    def update(self, dt: float, enemies_group: pygame.sprite.Group) -> None:
        movement = self.target - pygame.Vector2(self.rect.center)

        self.velocity = movement * self.movement_speed
        self.position += self.velocity * dt
        self.rect.center = self.position
        
        self.angle = angle_to_point(self.position, self.target)

        if collisions := pygame.sprite.spritecollide(self, enemies_group, False):
            for collision in collisions:
                collision.health -= self.damage

            self.kill()

    def draw(self, surface: pygame.Surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, self.rect)
