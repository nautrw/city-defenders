from enum import Enum, auto

import pygame
from pygame.typing import ColorLike

import src.core.config as Config
from src.gui.element import Element


class TextPlacementModes(Enum):
    TOPLEFT = auto()
    CENTER = auto()


class Text(Element):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(
        self,
        text: str,
        x: float,
        y: float,
        size: int = 24,
        placement_mode: TextPlacementModes = TextPlacementModes.TOPLEFT,
        antialias: bool = False,
        fg_color: ColorLike = Config.TEXT_NORMAL,
    ):
        self.font = pygame.font.Font("freesansbold.ttf", size)

        self.x = x
        self.y = y
        self.placement_mode = placement_mode

        self.text = text
        self.antialias = antialias
        self.fg_color = fg_color

        self.render_text()

    def update(self, delta_time: float, mouse_position: tuple[float, float]) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    def update_text(self, new_text: str) -> None:
        self.text = new_text
        self.render_text()

    def render_text(self) -> None:
        self.image = self.font.render(self.text, self.antialias, self.fg_color)

        if self.placement_mode == TextPlacementModes.TOPLEFT:
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        elif self.placement_mode == TextPlacementModes.CENTER:
            self.rect = self.image.get_rect(center=(self.x, self.y))
