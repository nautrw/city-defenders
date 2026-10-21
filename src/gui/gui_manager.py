import functools
import operator
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

import pygame

from src.core.scenes_manager import Scene
from src.gui.container import ElementContainer
from src.gui.element import Element

ElementT = TypeVar("ElementT", bound=Element | ElementContainer)
SceneT = TypeVar("SceneT", bound=Scene)


class ElementSearchTypeMismatchError(TypeError):
    pass


class ElementNotFoundError(ValueError):
    pass


# Generic[SceneT] is another example of typing magic I don't fully
# understand but it solves my problems; you pass in a scene type and then it
# uses that scene type as the type of the scene
class GUIManager(ABC, Generic[SceneT]):
    def __init__(self, scene: SceneT) -> None:
        self.scene = scene
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

    def get_element_by_id(self, id: str, element_type: type[ElementT]) -> ElementT:
        match = None

        for element in self.elements:
            if isinstance(element, ElementContainer):
                for container_element in element.elements:
                    if container_element.id == id:
                        match = container_element
            else:
                if element.id == id:
                    match = element

            if match:
                if not isinstance(match, element_type):
                    raise ElementSearchTypeMismatchError(
                        f"element {id} found of type "
                        f"{type(element)}, {element_type} "
                        "expected"
                    )

                return match

        raise ElementNotFoundError(f"element with id {id} not found")

    def element_exists(self, id: str) -> bool:
        elements = [
            [e.id for e in element.elements]
            if isinstance(element, ElementContainer)
            else element.id
            for element in self.elements
        ]

        # reduce() flattens the list,
        # https://docs.astral.sh/ruff/rules/quadratic-list-summation/
        return id in functools.reduce(operator.iadd, elements, [])

    def add_element(self, element: Element) -> None:
        if not self.element_exists(element.id):
            self.elements.append(element)
        else:
            raise ValueError(f"element with id {element.id} already exists in manager")

    def delete_element_by_id(self, id: str, element_type: type[ElementT]) -> ElementT:
        for element in self.elements:
            if isinstance(element, ElementContainer):
                for container_element in element.elements:
                    if container_element.id == id:
                        if isinstance(container_element, element_type):
                            element.elements.remove(container_element)
                        else:
                            raise ElementNotFoundError(
                                f"element {id} found of type "
                                f"{type(element)}, {element_type} "
                                "expected"
                            )
            else:
                if element.id == id:
                    if isinstance(container_element, element_type):
                        self.elements.remove(element)
                    else:
                        raise ElementSearchTypeMismatchError(
                            f"element {id} found of type "
                            f"{type(element)}, {element_type} "
                            "expected"
                        )

        raise ElementNotFoundError(f"element with id {id} not found")
