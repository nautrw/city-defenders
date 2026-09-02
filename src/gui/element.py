from abc import ABC, abstractmethod

import pygame

from src.gui.placement_system import RectAnchorMode


class Element(ABC):
    def __init__(
        self,
        id: str,
        image: pygame.Surface,
        x: float,
        y: float,
        width: float,
        height: float,
        anchor: RectAnchorMode = RectAnchorMode.TOPLEFT,
    ) -> None:
        self.id = id
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.anchor = anchor

        self.rect = pygame.FRect(self.x, self.y, width=self.width, height=self.height)
        self.move(self.x, self.y)  # just to set the anchor

    def move(
        self,
        new_x: float,
        new_y: float,
        anchor: RectAnchorMode = RectAnchorMode.TOPLEFT,
    ):
        if anchor == RectAnchorMode.TOPLEFT:
            self.rect.topleft = (new_x, new_y)
        elif anchor == RectAnchorMode.MIDTOP:
            self.rect.midtop = (new_x, new_y)
        elif anchor == RectAnchorMode.TOPRIGHT:
            self.rect.topright = (new_x, new_y)
        elif anchor == RectAnchorMode.MIDLEFT:
            self.rect.midleft = (new_x, new_y)
        elif anchor == RectAnchorMode.CENTER:
            self.rect.center = (new_x, new_y)
        elif anchor == RectAnchorMode.MIDRIGHT:
            self.rect.midright = (new_x, new_y)
        elif anchor == RectAnchorMode.BOTTOMLEFT:
            self.rect.bottomleft = (new_x, new_y)
        elif anchor == RectAnchorMode.MIDBOTTOM:
            self.rect.midbottom = (new_x, new_y)
        elif anchor == RectAnchorMode.BOTTOMRIGHT:
            self.rect.bottomright = (new_x, new_y)

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None: ...

    @abstractmethod
    def update(
        self, delta_time: float, mouse_position: tuple[float, float]
    ) -> None: ...
