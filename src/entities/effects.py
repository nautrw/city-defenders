import pygame
from pygame.typing import ColorLike


class EnemyEffect:
    def __init__(
        self,
        duration: float,
        stackable: bool = False,
        speed_multiplier: float = 1,
        damage_over_time: float = 0,
        overlay_color: ColorLike | None = None,
    ) -> None:
        self.duration = duration
        self.duration_counter = 0

        self.stackable = stackable
        self.speed_multiplier = speed_multiplier

        self.damage_over_time_cooldown = 0.1
        self.damage_over_time_dt_counter = 0
        self.damage_over_time = damage_over_time

        self.overlay_color = overlay_color

    def update(self, delta_time: float):
        self.duration_counter += delta_time
        self.damage_over_time_dt_counter += delta_time

    def draw(self, surface: pygame.Surface):
        if self.overlay_color:
            surface.fill(self.overlay_color, special_flags=pygame.BLEND_RGBA_MIN)


class FrozenEffect(EnemyEffect):
    stackable = True
    overlay_color = (162, 235, 255)  # rgb(162,235,255)

    def __init__(self, duration: float = 3, damage_over_time: float = 0, speed_multiplier: float = 0.5) -> None:
        super().__init__(
            duration=duration,
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
            stackable=self.stackable,
            damage_over_time=damage_over_time,
            overlay_color=self.overlay_color,
        )
