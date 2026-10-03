from enum import Enum, auto
from typing import TYPE_CHECKING

import pygame

import src.core.config as Config
from src.core.scenes_manager import Scene
from src.gui.button import CUSTOM_BUTTON_CLICKED, Button
from src.gui.container import ElementContainer
from src.gui.gui_manager import GUIManager
from src.gui.placement_system import RectAnchorMode
from src.gui.text import Text

if TYPE_CHECKING:
    from src.app import GameApp


class PauseMenuGUIState(Enum):
    NORMAL = auto()


class PauseMenuGUIManager(GUIManager):
    def __init__(self, scene: "PauseMenuScene") -> None:
        default_state = PauseMenuGUIState.NORMAL

        super().__init__(scene, default_state)

        self.scene: PauseMenuScene

        self.refresh()

    def refresh(self) -> None:
        container_height = 258
        container_width = 500
        button_width = container_width - (Config.ELEMENT_OUTER_PADDING * 2)
        button_height = 50

        main_container = ElementContainer(
            "main_container",
            Config.SCREEN_WIDTH / 2,
            Config.SCREEN_HEIGHT / 2,
            container_width,
            container_height,
            anchor=RectAnchorMode.CENTER,
        )

        pause_text = Text(
            "paused_text",
            "Paused",
            container_width / 2,
            Config.ELEMENT_OUTER_PADDING,
            size=Config.FONT_SIZE_VERYBIG,
            anchor=RectAnchorMode.MIDTOP,
        )

        back_button = Button(
            "back_button",
            container_width / 2,
            pause_text.rect.bottom + Config.ELEMENT_OUTER_PADDING,
            button_width,
            button_height,
            text=Text(
                "back_button_text",
                "Back",
                button_width / 2,
                button_height / 2,
                anchor=RectAnchorMode.CENTER,
            ),
            anchor=RectAnchorMode.MIDTOP,
        )

        restart_button = Button(
            "restart_button",
            container_width / 2,
            back_button.rect.bottom + Config.ELEMENT_OUTER_PADDING,
            button_width,
            button_height,
            text=Text(
                "restart_button_text",
                "Restart Map",
                button_width / 2,
                button_height / 2,
                anchor=RectAnchorMode.CENTER,
            ),
            anchor=RectAnchorMode.MIDTOP,
        )

        main_menu_button = Button(
            "main_menu_button",
            container_width / 2,
            restart_button.rect.bottom + Config.ELEMENT_OUTER_PADDING,
            button_width,
            button_height,
            text=Text(
                "main_menu_button_text",
                "Main Menu",
                button_width / 2,
                button_height / 2,
                anchor=RectAnchorMode.CENTER,
            ),
            anchor=RectAnchorMode.MIDTOP,
        )


        main_container.add_element(pause_text)
        main_container.add_element(back_button)
        main_container.add_element(restart_button)
        main_container.add_element(main_menu_button)
        self.elements.append(main_container)

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == CUSTOM_BUTTON_CLICKED:
            if event.button.id == "back_button":
                self.scene.unpause()
            elif event.button.id == "restart_button":
                self.scene.unpause()

                if self.scene.game.scene_manager.current_scene:
                    self.scene.game.scene_manager.current_scene.restart()  # ty:ignore[unresolved-attribute]
            elif event.button.id == "main_menu_button":
                # prevents circular import
                from src.scenes.main_menu import MainMenuScene

                self.scene.game.scene_manager.empty_stack()
                self.scene.game.scene_manager.push(MainMenuScene(self.scene.game))


class PauseMenuScene(Scene):
    def __init__(self, game: "GameApp"):
        super().__init__(game)

        self.gui_manager = PauseMenuGUIManager(self)

    def render(self, surface: pygame.Surface) -> None:
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill(Config.DARK_BG)
        surface.blit(overlay)

        self.gui_manager.render_elements(surface)

    def unpause(self):
        self.game.scene_manager.pop()
        pygame.mixer.music.unpause()
        self.game.scene_manager.current_scene.paused = False # ty:ignore[unresolved-attribute]

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            self.gui_manager.handle_event(event)

            if event.type == pygame.KEYDOWN:  # noqa: SIM102
                if event.key == pygame.K_ESCAPE:
                    self.unpause()

    def update(self, delta_time: float) -> None:
        self.gui_manager.update_elements(delta_time, pygame.mouse.get_pos())
