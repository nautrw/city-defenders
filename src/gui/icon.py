import pygame

from src.gui.element import Element
from src.gui.placement_system import RectAnchorMode


class Icon(Element):
    def __init__(
        self,
        id: str,
        x: float,
        y: float,
        image: pygame.Surface,
        anchor: RectAnchorMode = RectAnchorMode.TOPLEFT,
    ) -> None:
        self.id = id
        self.surface = image.copy()
        self.width = image.width
        self.height = image.height
        self.anchor = anchor

        self.x = x
        self.y = y

        super().__init__(
            self.id, self.surface, self.x, self.y, self.width, self.height, self.anchor
        )

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    def update(self, delta_time: float, mouse_position: tuple[float, float]) -> None:
        pass
