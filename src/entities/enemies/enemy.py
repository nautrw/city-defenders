import pygame

from src.entities.health_bar import HealthBar

ENEMY_KILLED = pygame.event.custom_type()


class Enemy(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(
        self,
        animation: list[pygame.Surface],
        movement_speed: int,
        max_health: int,
        path_waypoints: list[tuple[float, float]],
        coins_drop: int,
        animation_duration: float = 0.25,
    ):
        super().__init__()

        self.animation = animation
        self.animation_index = 0
        self.animation_duration = animation_duration
        self.animation_dt_counter = 0
        
        self.image = animation[self.animation_index]
        self.rect = self.image.get_frect()

        self.path_waypoints = path_waypoints
        self.waypoint_index = 1
        self.position = pygame.Vector2(self.path_waypoints[0])
        self.velocity = pygame.Vector2()

        self.movement_speed = movement_speed
        self.max_health = max_health
        self.health = max_health

        self.coins_drop = coins_drop

        self.health_bar = HealthBar()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
        self.health_bar.draw(surface)

    def update(self, delta_time: float) -> None:
        movement_target = pygame.Vector2(self.path_waypoints[self.waypoint_index])
        movement = movement_target - pygame.Vector2(self.rect.center)
        distance_to_target = movement.length()

        if distance_to_target <= (self.movement_speed * delta_time):
            self.position = movement_target
            self.waypoint_index += 1
        else:
            movement.normalize_ip()
            self.velocity = movement * self.movement_speed
            self.position += self.velocity * delta_time

        self.rect.center = self.position

        self.health_bar.update(self.health, self.max_health, self.rect.midtop)

        self.animation_dt_counter += delta_time

        if self.animation_dt_counter >= self.animation_duration:
            self.animation_index += 1
            self.animation_index %= len(self.animation)
            self.image = self.animation[self.animation_index]
            self.animation_dt_counter = 0

        if self.health <= 0 or self.waypoint_index >= len(self.path_waypoints):
            event = pygame.Event(ENEMY_KILLED, {"entity": self})
            pygame.event.post(event)
            self.kill()
            return
