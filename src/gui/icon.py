import pygame

from src.gui.element import Element


class Icon(Element):
    def __init__(self, id: str, x: float, y: float, image: pygame.Surface):
        self.id = id
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

        super().__init__(self.id, self.image, self.rect)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    def update(self, delta_time: float, mouse_position: tuple[float, float]) -> None:
        pass
