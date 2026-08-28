from abc import ABC, abstractmethod

import pygame


class Element(ABC):
    def __init__(self, id: str) -> None:
        self.id = id

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        ...
    
    @abstractmethod
    def update(self, delta_time: float, mouse_position: tuple[int, int]) -> None:
        ...
