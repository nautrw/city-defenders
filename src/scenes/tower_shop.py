from typing import TYPE_CHECKING

import pygame
from loguru import logger

import src.core.config as Config
from src.core.scenes_manager import Scene
from src.core.utils import (
    load_button_state_triplet_assets,
    load_scaled_asset,
)
from src.gui.button import CUSTOM_BUTTON_CLICKED, Button
from src.gui.gui_manager import GUIManager
from src.gui.placement_system import RectAnchorMode

if TYPE_CHECKING:
    from src.app import GameApp


class MapSelectorSceneGUIManager(GUIManager):
    def __init__(self, scene: "TowerShopScene") -> None:

        super().__init__(scene)

        self.scene: TowerShopScene

        self.refresh()

    def refresh(self) -> None:
        self.elements = []

        close_icon = Button(
            "back_to_main_menu_button",
            Config.ELEMENT_OUTER_PADDING,
            Config.ELEMENT_OUTER_PADDING,
            Config.BUTTON_SIZE,
            Config.BUTTON_SIZE,
            anchor=RectAnchorMode.TOPLEFT,
            normal_icon=load_scaled_asset("close_icon"),
        )


        arrow_new_size = (Config.BUTTON_SIZE * 3, Config.BUTTON_SIZE * 3)

        # right_icons go to the right map and left_icons go to the left map
        right_icons = load_button_state_triplet_assets("left_arrow", arrow_new_size)
        left_icons = {
            "normal_icon": pygame.transform.flip(
                right_icons["normal_icon"], True, False
            ),
            "pressed_icon": pygame.transform.flip(
                right_icons["pressed_icon"], True, False
            ),
            "hover_icon": pygame.transform.flip(
                right_icons["hover_icon"], True, False
            ),
        }

        go_right_button = Button(
            "go_right_button",
            Config.SCREEN_WIDTH * .80,
            Config.SCREEN_HEIGHT / 2,
            *arrow_new_size,
            anchor=RectAnchorMode.MIDLEFT,
            **right_icons,
            normal_bg=None,
            hover_bg=None,
            pressed_bg=None,
        )

        go_left_button = Button(
            "go_left_button",
            Config.SCREEN_WIDTH * .20,
            Config.SCREEN_HEIGHT / 2,
            *arrow_new_size,
            anchor=RectAnchorMode.MIDRIGHT,
            normal_icon=left_icons["normal_icon"],
            hover_icon=left_icons["hover_icon"],
            pressed_icon=left_icons["pressed_icon"],
            normal_bg=None,
            hover_bg=None,
            pressed_bg=None,
        )

        self.elements.append(close_icon)
        self.elements.append(go_right_button)
        self.elements.append(go_left_button)

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == CUSTOM_BUTTON_CLICKED:
            logger.debug(f"gui button clicked: id={event.button.id}")

            self.refresh()


class TowerShopScene(Scene):
    def __init__(self, game: "GameApp"):
        super().__init__(game)

        self.selected_map_index = 0
        self.background = load_scaled_asset("tower_shop", (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))

        self.gui_manager = MapSelectorSceneGUIManager(self)

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.background, (0, 0))

        self.gui_manager.render_elements(surface)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            self.gui_manager.handle_event(event)

    def update(self, delta_time: float) -> None:
        self.gui_manager.update_elements(delta_time, pygame.mouse.get_pos())
