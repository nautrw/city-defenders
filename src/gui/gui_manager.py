from abc import ABC, abstractmethod
from enum import Enum

import pygame

from src.core.scenes_manager import Scene
from src.gui.element import Element


class GUIManager(ABC):
    def __init__(self, scene: Scene, default_state: Enum) -> None:
        self.scene: Scene = scene
        self.state: Enum = default_state
        self.elements: list[Element] = []

    @abstractmethod
    def refresh(self) -> None: ...

    @abstractmethod
    def handle_event(self, event: pygame.Event) -> None: ...

    def render_elements(self, surface: pygame.Surface) -> None:
        for element in self.elements:
            element.draw(surface)

    def update_elements(
        self, delta_time: float, mouse_position: tuple[int, int]
    ) -> None:
        for element in self.elements:
            element.update(delta_time, mouse_position)

    def switch_state(self, state: Enum) -> None:
        self.state = state
        self.refresh()
