import pygame
from pygame.typing import ColorLike

import src.core.config as Config
from src.gui.element import Element


class ElementContainer(Element):
    def __init__(
        self,
        id: str,
        x: float,
        y: float,
        width: float,
        height: float,
        inner_padding: int = 2,
        bg_color: ColorLike = Config.BUTTON_NORMAL_BG,
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inner_padding = inner_padding
        self.bg_color = bg_color

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_frect(topleft=(self.x, self.y))

        self.elements = []

        super().__init__(id, self.surface, self.rect)

    def draw(self, surface: pygame.Surface) -> None:
        self.surface.fill(self.bg_color)

        for element in self.elements:
            element.draw(self.surface)

        surface.blit(self.surface, self.rect)

    def update(self, delta_time: float, mouse_position: tuple[float, float]) -> None:
        # relative_mouse_position = (self.x - mouse_position[0], self.y - mouse_position[1])
        relative_mouse_position = (
            mouse_position[0] - self.x,
            mouse_position[1] - self.y,
        )

        for element in self.elements:
            element.update(delta_time, relative_mouse_position)
