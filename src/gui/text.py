from enum import Enum, auto

import pygame
from pygame.typing import ColorLike

import src.core.config as Config
from src.core.utils import get_font
from src.gui.element import Element


class TextPlacementModes(Enum):
    TOP_LEFT = auto()
    CENTER_CENTER = auto()
    TOP_CENTER = auto()


class Text(Element):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(
        self,
        text: str,
        x: float,
        y: float,
        size: int = Config.FONT_SIZE_NORMAL,
        placement_mode: TextPlacementModes = TextPlacementModes.TOP_LEFT,
        antialias: bool = True,
        fg_color: ColorLike = Config.TEXT_NORMAL,
        font_name: str = Config.FONT_NORMAL,
        wrap_length: int = 500,
    ):
        self.font = pygame.font.Font(get_font(font_name), size)

        self.x = x
        self.y = y
        self.placement_mode = placement_mode

        self.text = text
        self.antialias = antialias
        self.fg_color = fg_color
        self.wrap_length = wrap_length

        self.render_text()

    def update(self, delta_time: float, mouse_position: tuple[float, float]) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    def update_text(self, new_text: str) -> None:
        self.text = new_text
        self.render_text()

    def render_text(self) -> None:
        self.image = self.font.render(
            self.text, self.antialias, self.fg_color, wraplength=self.wrap_length
        )

        if self.placement_mode == TextPlacementModes.TOP_LEFT:
            self.rect = self.image.get_frect(topleft=(self.x, self.y))
        elif self.placement_mode == TextPlacementModes.CENTER_CENTER:
            self.rect = self.image.get_frect(center=(self.x, self.y))
        elif self.placement_mode == TextPlacementModes.TOP_CENTER:
            self.rect = self.image.get_frect(centerx=self.x, top=self.y)
