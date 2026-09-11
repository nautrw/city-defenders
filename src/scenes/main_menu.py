from src.core.utils import load_asset
from enum import Enum, auto
from typing import TYPE_CHECKING

import pygame

import src.core.config as Config
from src.core.scenes_manager import Scene
from src.gui.button import CUSTOM_BUTTON_CLICKED, Button
from src.gui.gui_manager import GUIManager
from src.gui.placement_system import RectAnchorMode
from src.gui.text import Text
from src.scenes.map_selector import MapSelectorScene

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

            play_button = Button(
                "play_button",
                Config.SCREEN_WIDTH / 2,
                Config.SCREEN_HEIGHT * 0.5,
                Config.BUTTON_SIZE * 2,
                Config.BUTTON_SIZE,
                text=Text(
                    "play_button_play_text",
                    "Play",
                    Config.BUTTON_SIZE,
                    Config.BUTTON_SIZE / 2,
                    Config.FONT_SIZE_HEADER,
                    anchor=RectAnchorMode.CENTER,
                ),
                anchor=RectAnchorMode.CENTER,
            )

            self.elements.append(title_text)
            self.elements.append(play_button)

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == CUSTOM_BUTTON_CLICKED:  # noqa: SIM102
            if event.button.id == "play_button":
                self.scene.game.scene_manager.switch(MapSelectorScene(self.scene.game))


class MainMenuScene(Scene):
    def __init__(self, game: "GameApp"):
        super().__init__(game)

        self.gui_manager = MainMenuSceneGUIManager(self)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(Config.BRIGHT_GREEN)

        game_icon = load_asset("game_icon")
        game_icon_rect = game_icon.get_rect(center=(Config.SCREEN_WIDTH / 2, Config.SCREEN_HEIGHT * .25))
        surface.blit(game_icon, game_icon_rect)

        self.gui_manager.render_elements(surface)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            self.gui_manager.handle_event(event)

    def update(self, delta_time: float) -> None:
        self.gui_manager.update_elements(delta_time, pygame.mouse.get_pos())
