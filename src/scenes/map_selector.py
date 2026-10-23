from typing import TYPE_CHECKING

import pygame
from loguru import logger

import src.core.config as Config
from src.core.scenes_manager import Scene
from src.core.utils import (
    get_sound,
    load_button_state_triplet_assets,
    load_scaled_asset,
)
from src.gui.button import CUSTOM_BUTTON_CLICKED, Button
from src.gui.gui_manager import GUIManager
from src.gui.icon import Icon
from src.gui.placement_system import RectAnchorMode
from src.gui.text import Text
from src.maps.data import MAP_PROGRESSION, MAPS_DATA
from src.scenes.main_game import MainGameScene

if TYPE_CHECKING:
    from src.app import GameApp


class MapSelectorSceneGUIManager(GUIManager):
    def refresh(self) -> None:
        self.elements = []

        map_name = self.scene.all_maps[self.scene.selected_map_index]
        map_icon_surf = load_scaled_asset(f"{map_name}_globe", (288, 288))
        map_data = MAPS_DATA[map_name]
        waves_num = len(map_data.waves)

        padding = Config.ELEMENT_OUTER_PADDING * 9

        close_icon = Button(
            "back_to_main_menu_button",
            Config.ELEMENT_OUTER_PADDING,
            Config.ELEMENT_OUTER_PADDING,
            Config.BUTTON_SIZE,
            Config.BUTTON_SIZE,
            anchor=RectAnchorMode.TOPLEFT,
            normal_icon=load_scaled_asset("close_icon"),
        )

        map_icon = Icon(
            "map_icon",
            Config.SCREEN_WIDTH / 2,
            Config.SCREEN_HEIGHT / 2,
            map_icon_surf,
            anchor=RectAnchorMode.CENTER,
        )

        waves_number = Text(
            "waves_number",
            f"{waves_num} Waves",
            Config.SCREEN_WIDTH / 2,
            map_icon.rect.top - (padding / 3),
            size=Config.FONT_SIZE_LARGE,
            anchor=RectAnchorMode.MIDBOTTOM,
        )

        map_name_text = Text(
            "map_name",
            map_data.display_name,
            Config.SCREEN_WIDTH / 2,
            waves_number.rect.top - (padding / 2),
            size=Config.FONT_SIZE_XXXLARGE,
            anchor=RectAnchorMode.MIDBOTTOM,
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
            "hover_icon": pygame.transform.flip(right_icons["hover_icon"], True, False),
        }

        go_right_button = Button(
            "go_right_button",
            map_icon.rect.right + padding,
            map_icon.rect.centery,
            *arrow_new_size,
            anchor=RectAnchorMode.MIDLEFT,
            **right_icons,
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
            normal_icon=left_icons["normal_icon"],
            hover_icon=left_icons["hover_icon"],
            pressed_icon=left_icons["pressed_icon"],
            normal_bg=None,
            hover_bg=None,
            pressed_bg=None,
        )

        last_map = MAP_PROGRESSION[(self.scene.selected_map_index - 1) % len(MAPS_DATA)]
        can_play_map = (last_map in self.scene.game.player_save.beaten_maps) or (
            self.scene.selected_map_index == 0
        )

        play_button = Button(
            "play_button",
            map_icon.rect.centerx,
            map_icon.rect.bottom + padding,
            Config.BUTTON_SIZE * 2 if can_play_map else Config.BUTTON_SIZE * 4,
            Config.BUTTON_SIZE,
            text=Text(
                "play_button_play_text",
                "Play",
                Config.BUTTON_SIZE,
                Config.BUTTON_SIZE / 2,
                Config.FONT_SIZE_XLARGE,
                anchor=RectAnchorMode.CENTER,
            )
            if can_play_map
            else Text(
                "play_button_play_text",
                "Not Unlocked",
                Config.BUTTON_SIZE * 2,
                Config.BUTTON_SIZE / 2,
                Config.FONT_SIZE_LARGE,
                anchor=RectAnchorMode.CENTER,
            ),
            anchor=RectAnchorMode.MIDTOP,
            enabled=can_play_map,
            normal_bg=Config.GREEN_BUTTON_NORMAL_BG,
            hover_bg=Config.GREEN_BUTTON_HOVERED_BG,
            pressed_bg=Config.GREEN_BUTTON_PRESSED_BG,
        )

        self.add_element(close_icon)
        self.add_element(map_name_text)
        self.add_element(waves_number)
        self.add_element(map_icon)
        self.add_element(go_right_button)
        self.add_element(go_left_button)
        self.add_element(play_button)

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == CUSTOM_BUTTON_CLICKED:
            logger.debug(f"gui button clicked: id={event.button.id}")

            if event.button.id == "go_right_button":
                self.scene.selected_map_index += 1
                self.scene.selected_map_index %= len(self.scene.all_maps)
            elif event.button.id == "go_left_button":
                self.scene.selected_map_index -= 1
                self.scene.selected_map_index %= len(self.scene.all_maps)
            elif event.button.id == "play_button":
                map_name = self.scene.all_maps[self.scene.selected_map_index]
                self.scene.enter_map(map_name)
            elif event.button.id == "back_to_main_menu_button":
                # prevent circular import
                from src.scenes.main_menu import MainMenuScene

                self.scene.game.scene_manager.switch(MainMenuScene(self.scene.game))

            self.refresh()


class MapSelectorScene(Scene):
    def __init__(self, game: "GameApp"):
        super().__init__(game)

        self.all_maps = MAP_PROGRESSION
        self.selected_map_index = 0

        self.gui_manager = MapSelectorSceneGUIManager(self)

        self.background = load_scaled_asset(
            "map_selector", (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        )

    def on_enter(self) -> None:
        pygame.mixer.music.load(get_sound("The Bards Tale"))
        pygame.mixer.music.play(loops=-1, fade_ms=Config.DEFAULT_SOUND_FADEIN_MS)

    def on_exit(self) -> None:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def enter_map(self, map_name: str):
        logger.info(f"map selected: {map_name}")

        self.game.scene_manager.switch(MainGameScene(self.game, map_name))

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.background, (0, 0))

        self.gui_manager.render_elements(surface)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            self.gui_manager.handle_event(event)

    def update(self, delta_time: float) -> None:
        self.gui_manager.update_elements(delta_time, pygame.mouse.get_pos())
