import pygame
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Solves the circular import error as a result of src.app being uninitialized
# TYPE_CHECKING is false at runtime so the lsp can still see it but it's not
# actually imported
if TYPE_CHECKING:
    from src.app import GameApp

class SceneManager:
    def __init__(self) -> None:
        self._scenes_stack: list[Scene] = []

    @property
    def current_scene(self) -> Scene | None:
        if not self._scenes_stack:
            return None
        
        return self._scenes_stack[-1]

    @property
    def stack_length(self) -> int:
        return len(self._scenes_stack)

    def pop(self) -> None:
        """Removes the top scene from the stack."""

        if self._scenes_stack:
            old_scene = self._scenes_stack.pop()
            old_scene.on_exit()

        # protects against calling on_enter on NoneType if the stack is empty
        # after popping
        if self._scenes_stack: 
            self._scenes_stack[-1].on_enter()

    def switch(self, new_scene: Scene) -> None:
        """
        Switches the top scene from the stack without affecting the one below.
        """
        if self._scenes_stack:
            old_scene = self._scenes_stack.pop()
            old_scene.on_exit()

        self._scenes_stack.append(new_scene)
        new_scene.on_enter()

    def push(self, new_scene: Scene) -> None:
        """Pushes a new scene to the stack without affecting the one below.."""
        self._scenes_stack.append(new_scene)
        new_scene.on_enter()

class Scene(ABC):
    def __init__(self, game: GameApp) -> None:
        self.game = game

    # Abstractmethods make it so that its required for any other classes that
    # inherit from this to implement the functions themselves
    @abstractmethod
    def handle_events(self, events: list[pygame.Event]) -> None:
        ...

    @abstractmethod
    def update(self, delta_time: int | float) -> None:
        ...

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        ...

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass
