import random
from src.core.utils import load_asset, load_scaled_asset
from src.entities.particle import Particle
import src.core.config as Config
import pygame
from pygame.typing import ColorLike


class EnemyEffect:
    def __init__(
        self,
        duration: float,
        particle_img: pygame.Surface,
        stackable: bool = False,
        speed_multiplier: float = 1,
        damage_over_time: float = 0,
        overlay_color: ColorLike | None = None,
        particle_spawn_interval: float = Config.PARTICLE_SPAWN_INTERVAL
    ) -> None:
        self.duration = duration
        self.duration_counter = 0

        self.stackable = stackable
        self.speed_multiplier = speed_multiplier

        self.damage_over_time_cooldown = 0.1
        self.damage_over_time_dt_counter = 0
        self.damage_over_time = damage_over_time

        self.overlay_color = overlay_color

        self.particle_img = particle_img
        self.particle_spawn_interval = particle_spawn_interval
        self.particle_dt_counter = 0.0

    def update(self, delta_time: float, x_range: tuple[float, float], y_pos: float, particle_group: pygame.sprite.Group):
        self.duration_counter += delta_time
        self.damage_over_time_dt_counter += delta_time

        self.particle_dt_counter += delta_time
        if self.particle_dt_counter >= self.particle_spawn_interval:
            self.particle_dt_counter = 0
            particle = Particle(random.uniform(*x_range), y_pos, self.particle_img) 
            particle_group.add(particle)

    def draw(self, surface: pygame.Surface):
        if self.overlay_color:
            # rgba mult works the best
            surface.fill(self.overlay_color, special_flags=pygame.BLEND_RGBA_MULT)


class FrozenEffect(EnemyEffect):
    stackable = True
    overlay_color = (162, 235, 255)  # rgb(162,235,255)

    def __init__(
        self,
        duration: float = 3,
        damage_over_time: int = 0,
        speed_multiplier: float = 0.5,
    ) -> None:
        super().__init__(
            duration=duration,
            particle_img=load_scaled_asset("frozen_effect", (8, 8)),
            stackable=self.stackable,
            speed_multiplier=speed_multiplier,
            overlay_color=self.overlay_color,
        )


class PoisonedEffect(EnemyEffect):
    duration = 3
    stackable = True
    overlay_color = "#494182"

    def __init__(self, duration: float = 3, damage_over_time: float = 0.1) -> None:
        super().__init__(
            duration=duration,
            particle_img=load_scaled_asset("poisoned_effect", (8, 8)),
            stackable=self.stackable,
            damage_over_time=damage_over_time,
            overlay_color=self.overlay_color,
        )


class BurningEffect(EnemyEffect):
    duration = 5
    speed_multiplier = 3
    stackable = True
    overlay_color = "#FF6717"

    def __init__(self, duration: float = duration, damage_over_time: float = 1) -> None:
        super().__init__(
            duration=duration,
            particle_img=load_scaled_asset("burning_effect", (8, 8)),
            stackable=self.stackable,
            damage_over_time=damage_over_time,
            overlay_color=self.overlay_color,
            speed_multiplier=self.speed_multiplier,
        )
