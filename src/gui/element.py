from abc import ABC, abstractmethod

import pygame


class Element(ABC):
    def __init__(self, id: str, image: pygame.Surface, rect: pygame.Rect | pygame.FRect) -> None:
        self.id = id
        self.image = image
        self.rect = rect

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None: ...

    @abstractmethod
    def update(self, delta_time: float, mouse_position: tuple[float, float]) -> None: ...
