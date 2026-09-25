import pygame

from src.entities.effects import EnemyEffect
from src.entities.health_bar import HealthBar

ENEMY_KILLED = pygame.event.custom_type()
DEFENSE_BREACHED = pygame.event.custom_type()


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
    ) -> None:
        super().__init__()

        self.animation = animation
        self.animation_index = 0
        self.animation_duration = animation_duration
        self.animation_dt_counter = 0
        
        self.image = self.animation[self.animation_index]
        self.rect = self.image.get_frect()

        self.path_waypoints = path_waypoints
        self.waypoint_index = 1
        self.position = pygame.Vector2(self.path_waypoints[0])
        self.velocity = pygame.Vector2()

        self.movement_speed = movement_speed
        self.max_health = max_health
        self.health = max_health

        self.effects: list[EnemyEffect] = []

        self.coins_drop = coins_drop

        self.health_bar = HealthBar()

    def draw(self, surface: pygame.Surface) -> None:
        image_drawn = self.image.copy()

        for effect in self.effects:
            effect.draw(image_drawn)

        surface.blit(image_drawn, self.rect)
        self.health_bar.draw(surface)

    def add_effect(self, effect: EnemyEffect) -> None:
        if effect.stackable or not effect in self.effects:
            self.effects.append(effect)

    def update_effects(self, delta_time: float) -> None:
        for effect in self.effects:
            effect.update(delta_time)

            if effect.duration_counter >= effect.duration:
                self.effects.remove(effect)

            if effect.damage_over_time_dt_counter >= effect.damage_over_time_cooldown:
                self.health -= effect.damage_over_time
                effect.damage_over_time_dt_counter = 0

    def get_speed_multiplied(self) -> pygame.Vector2:
        cumulative_speed_multiplier = 1

        for effect in self.effects:
            cumulative_speed_multiplier *= effect.speed_multiplier

        return self.velocity * cumulative_speed_multiplier

    def update(self, delta_time: float, game_speed_multiplier: int) -> None:
        movement_target = pygame.Vector2(self.path_waypoints[self.waypoint_index])
        movement = movement_target - pygame.Vector2(self.rect.center)
        distance_to_target = movement.length()

        multiplied_dt = delta_time * game_speed_multiplier

        self.update_effects(multiplied_dt)

        if distance_to_target <= (self.movement_speed * multiplied_dt):
            self.position = movement_target
            self.waypoint_index += 1
        else:
            movement.normalize_ip()
            self.velocity = movement * self.movement_speed
            self.position += self.get_speed_multiplied() * multiplied_dt

        self.rect.center = self.position

        self.health_bar.update(self.health, self.max_health, self.rect.midtop)

        self.animation_dt_counter += multiplied_dt

        if self.animation_dt_counter >= self.animation_duration:
            self.animation_index += 1
            self.animation_index %= len(self.animation)
            self.image = self.animation[self.animation_index]
            self.animation_dt_counter = 0

        if self.health <= 0:
            event = pygame.Event(ENEMY_KILLED, {"entity": self})
            pygame.event.post(event)
            self.kill()
            return
        elif self.waypoint_index >= len(self.path_waypoints):
            event = pygame.Event(DEFENSE_BREACHED, {"entity": self})
            pygame.event.post(event)
            self.kill()
            return
