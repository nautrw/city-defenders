from enum import Enum, auto
from typing import TYPE_CHECKING

import pygame

import src.core.config as Config
from src.core.scenes_manager import Scene
from src.core.utils import get_font
from src.gui.gui_manager import GUIManager
from src.gui.placement_system import RectAnchorMode
from src.gui.text import Text
from src.scenes.main_game_gui_manager import UIStates

if TYPE_CHECKING:
    from src.app import GameApp


class MainMenuGUIState(Enum):
    NORMAL = auto()


class MainMenuSceneGUIManager(GUIManager):
    def __init__(self, scene: "MainMenuScene") -> None:
        default_state = MainMenuGUIState.NORMAL

        super().__init__(scene, default_state)

        self.refresh()

    def refresh(self):
        if self.state == MainMenuGUIState.NORMAL:
            title_text = Text(
                "title_text",
                "City Defenders TD",
                Config.SCREEN_WIDTH / 2,
                Config.SCREEN_HEIGHT * 0.25,
                Config.FONT_SIZE_HUGE,
                anchor=RectAnchorMode.CENTER,
                wrap_length=0,
            )

            self.elements.append(title_text)

    def handle_event(self, event: pygame.Event) -> None:
        pass


class MainMenuScene(Scene):
    def __init__(self, game: "GameApp"):
        super().__init__(game)

        self.gui_manager = MainMenuSceneGUIManager(self)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(Config.BRIGHT_GREEN)

        self.gui_manager.render_elements(surface)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            self.gui_manager.handle_event(event)

    def update(self, delta_time: float) -> None:
        pass
