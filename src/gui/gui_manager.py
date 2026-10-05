from abc import ABC, abstractmethod
from typing import TypeVar

import pygame

from src.core.scenes_manager import Scene
from src.gui.container import ElementContainer
from src.gui.element import Element

T = TypeVar("T", bound=Element | ElementContainer)


class GUIManager(ABC):
    def __init__(self, scene: Scene) -> None:
        self.scene: Scene = scene
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

    def get_element_by_id(self, id: str, type: type[T]) -> T:
        for element in self.elements:
            if isinstance(element, ElementContainer):
                for container_element in element.elements:
                    if container_element.id == id:
                        return container_element
            else:
                if element.id == id:
                    return element  # ty:ignore[invalid-return-type]

        raise ValueError(f"element with id {id} not found")
