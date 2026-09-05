import pygame
from pygame.typing import ColorLike

import src.core.config as Config
from src.gui.element import Element
from src.gui.placement_system import RectAnchorMode


class ElementContainer(Element):
    def __init__(
        self,
        id: str,
        x: float,
        y: float,
        width: float,
        height: float,
        anchor: RectAnchorMode = RectAnchorMode.TOPLEFT,
        inner_padding: int = 2,
        bg_color: ColorLike = Config.BUTTON_NORMAL_BG,
        bg_image: pygame.Surface | None = None,
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.anchor = anchor

        self.inner_padding = inner_padding
        self.bg_color = bg_color

        self.bg_image = bg_image or None

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        self.elements = []

        super().__init__(
            id, self.surface, self.x, self.y, self.width, self.height, self.anchor
        )

    def draw(self, surface: pygame.Surface) -> None:
        if self.bg_image:
            self.surface.blit(self.bg_image, self.rect)
        else:
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

    def add_element(self, element: Element):
        self.elements.append(element)
