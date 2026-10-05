from typing import TYPE_CHECKING

import pygame

import src.core.config as Config
from src.core.scenes_manager import Scene
from src.gui.button import CUSTOM_BUTTON_CLICKED, Button
from src.gui.gui_manager import GUIManager
from src.gui.placement_system import RectAnchorMode
from src.gui.text import Text

if TYPE_CHECKING:
    from src.app import GameApp


class GameVictorySceneGUIManager(GUIManager):
    def __init__(self, scene: "GameWonScene"):
        self.scene: GameWonScene

        super().__init__(scene)

        self.refresh()

    def refresh(self) -> None:
        self.elements = []

        victory_text = Text(
            "victory_text",
            "Victory!",
            Config.SCREEN_WIDTH / 2,
            Config.SCREEN_HEIGHT * 0.25,
            size=Config.FONT_SIZE_HUGE,
            anchor=RectAnchorMode.CENTER,
        )

        button_width = Config.BUTTON_SIZE * 3
        play_again_button = Button(
            "play_again_button",
            Config.SCREEN_WIDTH / 2,
            Config.SCREEN_HEIGHT * 0.5,
            button_width,
            Config.BUTTON_SIZE,
            text=Text(
                "play_again_button_text",
                "Play Again",
                button_width / 2,
                Config.BUTTON_SIZE / 2,
                size=Config.FONT_SIZE_HEADER,
                anchor=RectAnchorMode.CENTER,
            ),
            anchor=RectAnchorMode.CENTER,
        )

        self.elements.append(victory_text)
        self.elements.append(play_again_button)

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == CUSTOM_BUTTON_CLICKED:  # noqa: SIM102
            if event.button.id == "play_again_button":
                # prevent circular import
                from src.scenes.map_selector import MapSelectorScene

                self.scene.game.scene_manager.switch(MapSelectorScene(self.scene.game))


class GameWonScene(Scene):
    def __init__(self, game: "GameApp") -> None:
        super().__init__(game)

        self.gui_manager = GameVictorySceneGUIManager(self)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            self.gui_manager.handle_event(event)

    def update(self, delta_time: float) -> None:
        self.gui_manager.update_elements(delta_time, pygame.mouse.get_pos())

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(Config.BRIGHT_GREEN)
        self.gui_manager.render_elements(surface)
