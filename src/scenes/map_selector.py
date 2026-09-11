from src.scenes.main_game import MainGameScene
from src.gui.text import Text
from enum import Enum, auto
from src.core.map import GameMap
from typing import TYPE_CHECKING

import pygame

import src.core.config as Config
from src.core.scenes_manager import Scene
from src.gui.button import Button, CUSTOM_BUTTON_CLICKED
from src.core.utils import load_asset, load_scaled_asset, split_tileset, load_map
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
        self.elements = []
         
        padding = Config.ELEMENT_OUTER_PADDING * 3
        
        if self.state == MapSelectorSceneGUIState.NORMAL:
            map_name = Text(
                "map_name",
                self.scene.all_maps[self.scene.selected_map_index],  # ty:ignore[unresolved-attribute]
                Config.SCREEN_WIDTH / 2,
                Config.SCREEN_HEIGHT / 2,
                size=Config.FONT_SIZE_HUGE,
                anchor=RectAnchorMode.CENTER,
            )

            new_size = (Config.BUTTON_SIZE, Config.BUTTON_SIZE)

            # it's kind of confusing, i'm aware
            right_button_icon = load_scaled_asset("left_button", new_size)
            right_button_hovered_icon = load_scaled_asset(
                "left_arrow_button_hovered", new_size
            )
            right_button_pressed_icon = load_scaled_asset(
                "left_arrow_button_pressed", new_size
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
                map_name.rect.right + padding,
                Config.SCREEN_HEIGHT / 2,
                *new_size,
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
                map_name.rect.left + padding,
                map_name.rect.midleft.y ,
                *new_size,
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
                Config.SCREEN_WIDTH / 2,
                map_name.rect.bottom + padding,
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
                self.scene.enter_map(map_name) # ty:ignore[unresolved-attribute]


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
