from numpy import inner
from enum import Enum, auto

import pygame
from pygame.typing import ColorLike

import src.core.config as Config


class ButtonStates(Enum):
    NORMAL = auto()
    HOVERED = auto()
    PRESSED = auto()

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, inner_padding: int = 2, normal_bg: ColorLike = Config.ColorsConfig.button_normal_bg, hover_bg: ColorLike = Config.ColorsConfig.button_hovered_bg, pressed_bg: ColorLike = Config.ColorsConfig.button_pressed_bg, text: str = '', text_color: ColorLike = Config.ColorsConfig.text_normal, image: pygame.Surface | None = None):
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
            self.image_rect = self.image.get_rect(centerx=self.width // 2, top=inner_padding)

        self.text = text
        if self.text:
            self.font = pygame.font.Font(Config.FontConfig.font_name, Config.FontConfig.font_size_normal)
            self.text_surface = self.font.render(self.text, False, text_color)
            self.text_rect = self.text_surface.get_rect(centerx=self.width // 2, top=(self.image.get_rect().height + inner_padding if self.image else 0) + inner_padding)
            print(self.text_rect)

    def draw(self, surface: pygame.Surface):
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

    def update(self, delta_time: float):
        mouse_position = pygame.mouse.get_pos()
        pressed_buttons = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse_position):
            self.state = ButtonStates.HOVERED

            if pressed_buttons[0]: # left click
                self.state = ButtonStates.PRESSED
        else:
            self.state = ButtonStates.NORMAL
