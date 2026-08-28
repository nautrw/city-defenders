from abc import ABC, abstractmethod

import pygame


class Element(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        ...
    
    @abstractmethod
    def update(self, delta_time: float) -> None:
        ...
