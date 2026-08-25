import pygame

from src.entities.health_bar import HealthBar


class Enemy(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self, image: pygame.Surface, movement_speed: int, max_health: int, path_waypoints: list[tuple[float, float]]):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()

        self.path_waypoints = path_waypoints
        self.waypoint_index = 1
        self.position = pygame.Vector2(self.path_waypoints[0])
        self.velocity = pygame.Vector2()

        self.movement_speed = movement_speed
        self.max_health = max_health
        self.health = max_health

        self.health_bar = HealthBar()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
        self.health_bar.draw(surface)
    
    def update(self, dt: float) -> None:
        if self.waypoint_index >= len(self.path_waypoints):
            self.kill()
            return

        movement_target = pygame.Vector2(self.path_waypoints[self.waypoint_index])
        movement = movement_target - pygame.Vector2(self.rect.center)
        distance_to_target = movement.length()

        if distance_to_target <= (self.movement_speed * dt):
            self.position = movement_target
            self.waypoint_index += 1
        else:
            movement.normalize_ip()
            self.velocity = movement * self.movement_speed
            self.position += self.velocity * dt

        self.rect.center = self.position
        
        self.health_bar.update(self.health, self.max_health, self.rect.midtop)
