import pygame
from pygame.typing import ColorLike


class EnemyEffect:
    def __init__(
        self,
        duration: float,
        stackable: bool = False,
        speed_multiplier: float = 1,
        overlay_color: ColorLike | None = None,
    ):
        self.duration = duration
        self.duration_counter = 0

        self.stackable = stackable
        self.speed_multiplier = speed_multiplier

        self.overlay_color = overlay_color

    def update(self, delta_time: float):
        self.duration_counter += delta_time

    def draw(self, surface: pygame.Surface):
        if self.overlay_color:
            surface.fill(self.overlay_color, special_flags=pygame.BLEND_RGBA_MAX)


class FrozenEffect(EnemyEffect):
    duration = 5
    speed_multiplier = 0.5
    stackable = True
    overlay_color = (162, 235, 255)  # rgb(162,235,255)

    def __init__(self):
        super().__init__(
            duration=self.duration,
            stackable=self.stackable,
            speed_multiplier=self.speed_multiplier,
            overlay_color=self.overlay_color,
        )
