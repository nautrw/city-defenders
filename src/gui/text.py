from enum import Enum, auto

import pygame
from pygame.typing import ColorLike

import src.core.config as Config
from src.core.utils import get_font
from src.gui.element import Element
from src.gui.placement_system import RectAnchorMode


class TextPlacementModes(Enum):
    TOP_LEFT = auto()
    CENTER_CENTER = auto()
    TOP_CENTER = auto()


class Text(Element):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(
        self,
        id: str,
        text: str,
        x: float,
        y: float,
        size: int = Config.FONT_SIZE_NORMAL,
        anchor: RectAnchorMode = RectAnchorMode.TOPLEFT,
        antialias: bool = True,
        fg_color: ColorLike = Config.TEXT_COLOR_NORMAL,
        font_name: str = Config.FONT_NORMAL,
        wrap_length: int = 500,
    ):
        self.font = pygame.font.Font(get_font(font_name), size)
        self.image = pygame.Surface((0, 0))  # placeholder
        self.rect = self.image.get_frect()

        self.x = x
        self.y = y
        self.anchor = anchor

        self.text = text
        self.antialias = antialias
        self.fg_color = fg_color
        self.wrap_length = wrap_length

        super().__init__(
            id,
            self.image,
            self.x,
            self.y,
            self.rect.width,
            self.rect.height,
            self.anchor,
        )

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

        self.rect = self.image.get_frect()
        self.move(self.x, self.y, self.anchor)
