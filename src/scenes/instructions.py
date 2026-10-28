from typing import TYPE_CHECKING

import pygame
from loguru import logger

import src.core.config as Config
from src.core.scenes_manager import Scene
from src.core.utils import load_scaled_asset
from src.gui.button import CUSTOM_BUTTON_CLICKED, Button
from src.gui.gui_manager import GUIManager
from src.gui.placement_system import RectAnchorMode
from src.gui.text import Text

if TYPE_CHECKING:
    from src.app import GameApp


class InstructionsSceneGUIManager(GUIManager):
    def refresh(self) -> None:
        title = Text(
            "title",
            "Instructions",
            Config.SCREEN_WIDTH / 2,
            Config.ELEMENT_OUTER_PADDING,
            Config.FONT_SIZE_XXLARGE,
            anchor=RectAnchorMode.MIDTOP,
        )
        self.add_element(title)

        back_button = Button(
            "back_button",
            Config.ELEMENT_OUTER_PADDING,
            Config.ELEMENT_OUTER_PADDING,
            Config.BUTTON_SIZE,
            Config.BUTTON_SIZE,
            normal_icon=load_scaled_asset("close_icon"),
        )
        self.add_element(back_button)

        instructions_text = Text(
            "instructions_text",
            """Beating a map will give you shards to unlock towers in the tower shop
YOUR DATA SAVES WHEN EXITING THE GAMES

While playing a map:
- Right click and drag to move the camera around the map
- Click on the hammer at the top right to build towers
- You may click on a tower to view its stats and upgrade it
- You may change the speed or pause at the bottom left
- Press `r` to show tower areas of effect""",
            Config.ELEMENT_OUTER_PADDING,
            back_button.rect.bottom + Config.ELEMENT_OUTER_PADDING,
        )
        self.add_element(instructions_text)

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == CUSTOM_BUTTON_CLICKED:
            logger.debug(f"gui button clicked: id={event.button.id}")

            if event.button.id == "back_button":
                from src.scenes.main_menu import MainMenuScene

                self.scene.game.scene_manager.switch(MainMenuScene(self.scene.game))


class InstructionsScene(Scene):
    def __init__(self, game: "GameApp"):
        super().__init__(game)

        self.gui_manager = InstructionsSceneGUIManager(self)

        self.background = load_scaled_asset(
            "main_menu", (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        )

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.background, (0, 0))
        self.gui_manager.render_elements(surface)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            self.gui_manager.handle_event(event)

    def update(self, delta_time: float) -> None:
        self.gui_manager.update_elements(delta_time, pygame.mouse.get_pos())
