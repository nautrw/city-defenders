from enum import Enum, auto
from typing import TYPE_CHECKING

import pygame

import src.core.config as Config
from src.core.map import GameMap
from src.core.scenes_manager import Scene
from src.core.utils import load_asset, load_map, load_scaled_asset, split_tileset
from src.gui.button import CUSTOM_BUTTON_CLICKED, Button
from src.gui.gui_manager import GUIManager
from src.gui.icon import Icon
from src.gui.placement_system import RectAnchorMode
from src.gui.text import Text
from src.maps.data import MAPS_DATA
from src.scenes.main_game import MainGameScene

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
        self.elements = []

        padding = Config.ELEMENT_OUTER_PADDING * 9

        if self.state == MapSelectorSceneGUIState.NORMAL:
            map_name = self.scene.all_maps[self.scene.selected_map_index]  # ty:ignore[unresolved-attribute]
            map_icon_surf = load_scaled_asset(f"{map_name}_globe", (288, 288))

            map_icon = Icon(
                "map_icon",
                Config.SCREEN_WIDTH / 2,
                Config.SCREEN_HEIGHT / 2,
                map_icon_surf.width,
                map_icon_surf.height,
                map_icon_surf,
                anchor=RectAnchorMode.CENTER
            )

            map_name = Text(
                "map_name",
                self.scene.all_maps[self.scene.selected_map_index],  # ty:ignore[unresolved-attribute]
                Config.SCREEN_WIDTH / 2,
                map_icon.rect.top - padding,
                size=Config.FONT_SIZE_HUGE,
                anchor=RectAnchorMode.CENTER,
            )

            arrow_new_size = (Config.BUTTON_SIZE * 3, Config.BUTTON_SIZE * 3)

            # it's kind of confusing, i'm aware
            right_button_icon = load_scaled_asset("left_button", arrow_new_size)
            right_button_hovered_icon = load_scaled_asset(
                "left_arrow_button_hovered", arrow_new_size
            )
            right_button_pressed_icon = load_scaled_asset(
                "left_arrow_button_pressed", arrow_new_size
            )

            left_button_icon = pygame.transform.flip(right_button_icon, True, False)
            left_button_hovered_icon = pygame.transform.flip(
                right_button_hovered_icon, True, False
            )
            left_button_pressed_icon = pygame.transform.flip(
                right_button_pressed_icon, True, False
            )

            go_right_button = Button(
                "go_right_button",
                map_icon.rect.right + padding,
                map_icon.rect.centery,
                *arrow_new_size,
                anchor=RectAnchorMode.MIDLEFT,
                normal_icon=right_button_icon,
                hover_icon=right_button_hovered_icon,
                pressed_icon=right_button_pressed_icon,
                normal_bg=None,
                hover_bg=None,
                pressed_bg=None,
            )

            go_left_button = Button(
                "go_left_button",
                map_icon.rect.left - padding,
                map_icon.rect.centery,
                *arrow_new_size,
                anchor=RectAnchorMode.MIDRIGHT,
                normal_icon=left_button_icon,
                hover_icon=left_button_hovered_icon,
                pressed_icon=left_button_pressed_icon,
                normal_bg=None,
                hover_bg=None,
                pressed_bg=None,
            )

            play_button = Button(
                "play_button",
                map_icon.rect.centerx,
                map_icon.rect.bottom + padding,
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
                anchor=RectAnchorMode.MIDTOP,
            )

            self.elements.append(map_icon)
            self.elements.append(map_name)
            self.elements.append(go_right_button)
            self.elements.append(go_left_button)
            self.elements.append(play_button)

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == CUSTOM_BUTTON_CLICKED:
            if event.button.id == "go_right_button":
                self.scene.selected_map_index += 1  # ty:ignore[unresolved-attribute]
                self.scene.selected_map_index %= len(self.scene.all_maps)  # ty:ignore[unresolved-attribute]
            elif event.button.id == "go_left_button":
                self.scene.selected_map_index -= 1  # ty:ignore[unresolved-attribute]
                self.scene.selected_map_index %= len(self.scene.all_maps)  # ty:ignore[unresolved-attribute]
            elif event.button.id == "play_button":
                map_name = self.scene.all_maps[self.scene.selected_map_index]  # ty:ignore[unresolved-attribute]
                self.scene.enter_map(map_name)  # ty:ignore[unresolved-attribute]


class MapSelectorScene(Scene):
    def __init__(self, game: "GameApp"):
        super().__init__(game)

        self.all_maps = list(MAPS_DATA.keys())
        self.selected_map_index = 0

        self.gui_manager = MapSelectorSceneGUIManager(self)

    def enter_map(self, map_name: str):
        tileset_img = load_asset("tileset")
        tileset = split_tileset(tileset_img, Config.TILE_WIDTH, Config.TILE_HEIGHT)
        map_data = load_map(map_name)

        self.game.scene_manager.switch(
            MainGameScene(self.game, GameMap(tileset, map_data), MAPS_DATA[map_name])
        )

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(Config.BRIGHT_GREEN)

        self.gui_manager.render_elements(surface)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            self.gui_manager.handle_event(event)

    def update(self, delta_time: float) -> None:
        self.gui_manager.update_elements(delta_time, pygame.mouse.get_pos())
