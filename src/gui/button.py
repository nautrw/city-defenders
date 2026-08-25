from enum import Enum, auto

import pygame
from pygame.typing import ColorLike

import src.core.config as Config


class ButtonStates(Enum):
    NORMAL = auto()
    HOVERED = auto()
    PRESSED = auto()

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, normal_bg: ColorLike = Config.ColorsConfig.button_normal_bg, hover_bg: ColorLike = Config.ColorsConfig.button_hovered_bg, pressed_bg: ColorLike = Config.ColorsConfig.button_pressed_bg, text: str = '', image: pygame.Surface | None = None):
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

        self.text = text
        self.image = image

    def draw(self, surface: pygame.Surface):
        if self.state == ButtonStates.NORMAL:
            self.surface.fill(self.normal_bg)
        elif self.state == ButtonStates.HOVERED:
            self.surface.fill(self.hover_bg)
        elif self.state == ButtonStates.PRESSED:
            self.surface.fill(self.pressed_bg)

        surface.blit(self.surface, self.rect)

    def update(self, delta_time: float):
        mouse_position = pygame.mouse.get_pos()
        pressed_buttons = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse_position):
            self.state = ButtonStates.HOVERED

            if pressed_buttons[0]: # left click
                self.state = ButtonStates.PRESSED
        else:
            self.state = ButtonStates.NORMAL
