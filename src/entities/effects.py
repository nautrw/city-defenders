import pygame
from pygame.typing import ColorLike


class EnemyEffect:
    def __init__(
        self,
        duration: float,
        stackable: bool = False,
        speed_multiplier: float = 1,
        damage_over_time: int = 0,
        overlay_color: ColorLike | None = None,
    ) -> None:
        self.duration = duration
        self.duration_counter = 0

        self.stackable = stackable
        self.speed_multiplier = speed_multiplier

        self.damage_over_time_cooldown = 0.5
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
    duration = 3
    speed_multiplier = 0.5
    stackable = True
    overlay_color = (162, 235, 255)  # rgb(162,235,255)

    def __init__(self) -> None:
        super().__init__(
            duration=self.duration,
            stackable=self.stackable,
            speed_multiplier=self.speed_multiplier,
            overlay_color=self.overlay_color,
        )


class PoisonedEffect(EnemyEffect):
    duration = 3
    stackable = True
    damage_over_time = 2
    overlay_color = "#494182"

    def __init__(self) -> None:
        super().__init__(
            duration=self.duration,
            stackable=self.stackable,
            damage_over_time=self.damage_over_time,
            overlay_color=self.overlay_color,
        )
