import pygame
from abc import ABC, abstractmethod

class SceneManager:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        
        self.current_scene = Scene(self)

    def switch_scene(self, scene: Scene) -> None:
        self.current_scene.on_exit()
        self.current_scene = scene
        self.current_scene.on_enter()

class Scene(ABC):
    def __init__(self, manager: SceneManager) -> None:
        self.manager = manager

    # Abstractmethods make it so that its required for any other classes that
    # inherit from this to implement the functions themselves
    @abstractmethod
    def handle_events(self, events: list[pygame.Event]) -> None:
        ...

    @abstractmethod
    def update(self, delta_time: int | float) -> None:
        ...

    def render(self, screen: pygame.Surface) -> None:
        pass

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass
