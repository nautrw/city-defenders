from src.gui.text import Text
from enum import Enum, auto
from typing import TYPE_CHECKING

import pygame

import src.core.config as Config
from src.core.scenes_manager import Scene
from src.gui.button import Button
from src.core.utils import load_asset
from src.gui.gui_manager import GUIManager
from src.gui.placement_system import RectAnchorMode
from src.maps.data import MAPS_DATA

if TYPE_CHECKING:
    from src.app import GameApp


class MapSelectorSceneGUIState(Enum):
    NORMAL = auto()


class MapSelectorSceneGUIManager(GUIManager):
    def __init__(self, scene: "MapSelectorScene") -> None:
        default_state = MapSelectorSceneGUIState.NORMAL

        super().__init__(scene, default_state)
        self.refresh()

    def refresh(self):
        if self.state == MapSelectorSceneGUIState.NORMAL:
            map_name = Text(
                "map_name",
                self.scene.all_maps[self.scene.selected_map_index], # ty:ignore[unresolved-attribute]
                Config.SCREEN_WIDTH / 2,
                Config.SCREEN_HEIGHT / 2,
                size=Config.FONT_SIZE_HUGE,
                anchor=RectAnchorMode.CENTER
            )

            new_size = (Config.BUTTON_SIZE, Config.BUTTON_SIZE)

            # it's kind of confusing, i'm aware
            right_button_icon = load_asset("left_button")
            right_button_scaled = pygame.transform.scale(right_button_icon, new_size)

            left_button_icon = pygame.transform.flip(right_button_scaled, True, False)

            go_right_button = Button(
                "go_right_button",
                map_name.rect.right + Config.ELEMENT_OUTER_PADDING,
                Config.SCREEN_HEIGHT / 2,
                *right_button_scaled.size,
                anchor=RectAnchorMode.MIDLEFT,
                icon=right_button_scaled
            )

            go_left_button = Button(
                "go_left_button", 
                map_name.rect.left + Config.ELEMENT_OUTER_PADDING,
                Config.SCREEN_HEIGHT / 2,
                *left_button_icon.size,
                anchor=RectAnchorMode.MIDRIGHT,
                icon=left_button_icon
            )

            self.elements.append(map_name)
            self.elements.append(go_right_button)
            self.elements.append(go_left_button)

    def handle_event(self, event: pygame.Event) -> None:
        pass


class MapSelectorScene(Scene):
    def __init__(self, game: "GameApp"):
        super().__init__(game)

        self.all_maps = list(MAPS_DATA.keys())
        self.selected_map_index = 0

        self.gui_manager = MapSelectorSceneGUIManager(self)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(Config.DARK_BG)

        self.gui_manager.render_elements(surface)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            self.gui_manager.handle_event(event)

    def update(self, delta_time: float) -> None:
        pass
