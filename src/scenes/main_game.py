import pygame
from src.core.scenes_manager import Scene, SceneManager
from src.app import GameApp

class MainGameScene(Scene):
    def __init__(self, game: GameApp):
        super().__init__(game)

    def handle_events(self, events: list[pygame.Event]) -> None:
        pass

    def update(self, delta_time: int | float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        pass
