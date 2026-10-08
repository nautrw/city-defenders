from src.gui.icon import Icon
from enum import Enum, auto

import pygame
from pygame.typing import ColorLike

import src.core.config as Config
from src.gui.element import Element
from src.gui.placement_system import RectAnchorMode
from src.gui.text import Text

CUSTOM_BUTTON_CLICKED = pygame.event.custom_type()


class ButtonStates(Enum):
    NORMAL = auto()
    HOVERED = auto()
    PRESSED = auto()


class Button(Element):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(
        self,
        id: str,
        x: float,
        y: float,
        width: float,
        height: float,
        anchor: RectAnchorMode = RectAnchorMode.TOPLEFT,
        inner_padding: int = 2,
        normal_bg: ColorLike | None = Config.BUTTON_NORMAL_BG,
        hover_bg: ColorLike | None = Config.BUTTON_HOVERED_BG,
        pressed_bg: ColorLike | None = Config.BUTTON_PRESSED_BG,
        normal_icon: pygame.Surface | Icon |None = None,
        hover_icon: pygame.Surface | Icon | None = None,
        pressed_icon: pygame.Surface | Icon | None = None,
        text: Text | None = None,
        once_per_click: bool = True,
        enabled: bool = True,
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.anchor = anchor
        self.enabled = enabled

        self.state: ButtonStates = ButtonStates.NORMAL

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        super().__init__(
            id, self.image, self.x, self.y, self.width, self.height, self.anchor
        )

        self.normal_bg = normal_bg
        self.hover_bg = hover_bg
        self.pressed_bg = pressed_bg

        self.normal_icon = normal_icon
        self.hover_icon = hover_icon or normal_icon
        self.pressed_icon = pressed_icon or normal_icon

        self.text = text

        if self.text:
            self.text.render_text()

        if self.normal_icon:
            if isinstance(self.normal_icon, pygame.Surface):
                self.icon_rect = self.normal_icon.get_frect(
                    center=(self.width / 2, self.height / 2)
                )

                if self.text:
                    self.icon_rect = self.normal_icon.get_frect(
                        centerx=self.width / 2, top=inner_padding
                    )
            elif isinstance(self.normal_icon, Icon):
                self.icon_rect = self.normal_icon.rect

        self.pressed_last_frame = pygame.mouse.get_pressed()[0]
        self.once_per_click = once_per_click
    
    def _draw_icon(self, icon: pygame.Surface | Icon, surface: pygame.Surface) -> None:
        if isinstance(icon, pygame.Surface):
            surface.blit(icon, self.icon_rect)
        elif isinstance(icon, Icon):
            icon.draw(surface)

    def draw(self, surface: pygame.Surface) -> None:
        if self.enabled:
            if self.state == ButtonStates.NORMAL:
                if self.normal_bg:
                    self.image.fill(self.normal_bg)

                if self.normal_icon:
                    self._draw_icon(self.normal_icon, self.image)
            elif self.state == ButtonStates.HOVERED:
                if self.hover_bg:
                    self.image.fill(self.hover_bg)

                if self.hover_icon:
                    self._draw_icon(self.hover_icon, self.image)
            elif self.state == ButtonStates.PRESSED:
                if self.pressed_bg:
                    self.image.fill(self.pressed_bg)

                if self.pressed_icon:
                    self._draw_icon(self.pressed_icon, self.image)
        else:
            if self.pressed_bg:
                self.image.fill(self.pressed_bg)

            if self.pressed_icon:
                self._draw_icon(self.pressed_icon, self.image)

        if self.text:
            self.text.draw(self.image)

        surface.blit(self.image, self.rect)

    def update(self, delta_time: float, mouse_position: tuple[float, float]) -> None:
        pressed = pygame.mouse.get_pressed()[0]
        hovered = self.rect.collidepoint(mouse_position)

        if hovered:
            if pressed:
                self.state = ButtonStates.PRESSED

                if (
                    self.once_per_click and not self.pressed_last_frame
                ) or not self.once_per_click:
                    pygame.event.post(
                        pygame.event.Event(CUSTOM_BUTTON_CLICKED, {"button": self})
                    )
            else:
                self.state = ButtonStates.HOVERED
        else:
            self.state = ButtonStates.NORMAL

        self.pressed_last_frame = pressed

    def toggle(self, condition: bool) -> None:
        self.enabled = condition
