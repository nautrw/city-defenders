from enum import Enum, auto

import pygame
from pygame.typing import ColorLike

import src.core.config as Config
from src.gui.element import Element

CUSTOM_BUTTON_CLICKED = pygame.event.custom_type()


class ButtonStates(Enum):
    NORMAL = auto()
    HOVERED = auto()
    PRESSED = auto()


class Button(Element):
    def __init__(
        self,
        id: str,
        x: int,
        y: int,
        width: int,
        height: int,
        inner_padding: int = 2,
        normal_bg: ColorLike = Config.BUTTON_NORMAL_BG,
        hover_bg: ColorLike = Config.BUTTON_HOVERED_BG,
        pressed_bg: ColorLike = Config.BUTTON_PRESSED_BG,
        text: str = "",
        text_color: ColorLike = Config.TEXT_NORMAL,
        image: pygame.Surface | None = None,
        once_per_click: bool = True,
    ) -> None:
        super().__init__(id)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.state: ButtonStates = ButtonStates.NORMAL

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))

        self.normal_bg = normal_bg
        self.hover_bg = hover_bg
        self.pressed_bg = pressed_bg

        self.image = image
        if self.image:
            self.image_rect = self.image.get_rect(
                centerx=self.width // 2, top=inner_padding
            )

        self.text = text
        if self.text:
            self.font = pygame.font.Font(Config.FONT_NAME, Config.FONT_SIZE_NORMAL)
            self.text_surface = self.font.render(self.text, False, text_color)
            self.text_rect = self.text_surface.get_rect(
                centerx=self.width // 2,
                top=(self.image.get_rect().height + inner_padding if self.image else 0)
                + inner_padding,
            )

        self.pressed_last_frame = False
        self.once_per_click = once_per_click

    def draw(self, surface: pygame.Surface) -> None:
        if self.state == ButtonStates.NORMAL:
            self.surface.fill(self.normal_bg)
        elif self.state == ButtonStates.HOVERED:
            self.surface.fill(self.hover_bg)
        elif self.state == ButtonStates.PRESSED:
            self.surface.fill(self.pressed_bg)

        if self.image:
            self.surface.blit(self.image, self.image_rect)

        if self.text:
            self.surface.blit(self.text_surface, self.text_rect)

        surface.blit(self.surface, self.rect)

    def update(self, delta_time: float) -> None:
        mouse_position = pygame.mouse.get_pos()
        pressed_buttons = pygame.mouse.get_pressed()
        pressed = pressed_buttons[0]  # left click

        if self.rect.collidepoint(mouse_position):
            self.state = ButtonStates.PRESSED if pressed else ButtonStates.HOVERED

            if pressed and (not self.once_per_click or not self.pressed_last_frame):
                event = pygame.Event(CUSTOM_BUTTON_CLICKED, {"button": self})
                pygame.event.post(event)

                self.pressed_last_frame = True
        else:
            self.state = ButtonStates.NORMAL

        self.pressed_last_frame = pressed
