from src.core.data_saving import reset_data, load_data_from_file
from src.gui.container import ElementContainer
from enum import Enum, auto
import random
from typing import TYPE_CHECKING

import pygame
from loguru import logger

import src.core.config as Config
from src.core.scenes_manager import Scene
from src.core.utils import get_sound, load_asset, load_scaled_asset
from src.gui.button import CUSTOM_BUTTON_CLICKED, Button
from src.gui.gui_manager import GUIManager
from src.gui.placement_system import RectAnchorMode
from src.gui.text import Text
from src.maps.data import ALL_MAP_MUSIC
from src.scenes.map_selector import MapSelectorScene
from src.scenes.tower_shop import TowerShopScene

if TYPE_CHECKING:
    from src.app import GameApp


class MainMenuSceneGUIState(Enum):
    NORMAL = auto()
    CONFIRM_ERASE_DATA = auto()


class MainMenuSceneGUIManager(GUIManager):
    def __init__(self, scene: "MainMenuScene") -> None:
        self.scene = scene
        self.elements = []
        self.state = MainMenuSceneGUIState.NORMAL

        self.refresh()

    def refresh(self) -> None:
        self.elements = []

        if self.state == MainMenuSceneGUIState.NORMAL:
            quit_button = Button(
                "quit_button",
                Config.ELEMENT_OUTER_PADDING,
                Config.ELEMENT_OUTER_PADDING,
                Config.BUTTON_SIZE,
                Config.BUTTON_SIZE,
                normal_icon=load_scaled_asset("close_icon"),
            )

            title_text = Text(
                "title_text",
                "City Defenders TD",
                Config.SCREEN_WIDTH / 2,
                Config.SCREEN_HEIGHT * 0.25,
                Config.FONT_SIZE_XXXLARGE,
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
                    Config.FONT_SIZE_LARGE,
                    anchor=RectAnchorMode.CENTER,
                ),
                anchor=RectAnchorMode.CENTER,
            )

            tower_shop_button = Button(
                "tower_shop_button",
                Config.SCREEN_WIDTH / 2,
                play_button.rect.bottom + Config.ELEMENT_OUTER_PADDING,
                Config.BUTTON_SIZE * 4,
                Config.BUTTON_SIZE,
                text=Text(
                    "tower_shop_button_text",
                    "Tower Shop",
                    Config.BUTTON_SIZE * (4 / 2),
                    Config.BUTTON_SIZE / 2,
                    Config.FONT_SIZE_LARGE,
                    anchor=RectAnchorMode.CENTER,
                ),
                anchor=RectAnchorMode.MIDTOP,
            )

            erase_data_button = Button(
                "erase_data_button",
                Config.ELEMENT_OUTER_PADDING,
                Config.SCREEN_HEIGHT - Config.ELEMENT_OUTER_PADDING,
                Config.BUTTON_SIZE * 3,
                Config.BUTTON_SIZE,
                text=Text(
                    "erase_data_button_text",
                    "Erase Data",
                    Config.BUTTON_SIZE * (3/2),
                    Config.BUTTON_SIZE / 2,
                    anchor=RectAnchorMode.CENTER,
                    fg_color=Config.RED
                ),
                anchor=RectAnchorMode.BOTTOMLEFT
            )
            
            self.add_element(quit_button)
            self.add_element(title_text)
            self.add_element(play_button)
            self.add_element(erase_data_button)
            self.add_element(tower_shop_button)
        elif self.state == MainMenuSceneGUIState.CONFIRM_ERASE_DATA:
            container_width = 650
            container_height = 150
            button_width = (
                (container_width - (Config.ELEMENT_OUTER_PADDING * 2))
                # this padding is the middle between the 2 buttons
                - Config.ELEMENT_OUTER_PADDING
            ) / 2
            button_height = 50

            main_container = ElementContainer(
                "main_container",
                Config.SCREEN_WIDTH / 2,
                Config.SCREEN_HEIGHT / 2,
                container_width,
                container_height,
                anchor=RectAnchorMode.CENTER,
            )

            question_text = Text(
                "question_text",
                "Are you sure you want to erase your data?",
                container_width / 2,
                Config.ELEMENT_OUTER_PADDING,
                size=Config.FONT_SIZE_MEDIUM,
                anchor=RectAnchorMode.MIDTOP,
                wrap_length=container_width,
            )
            warning_text = Text(
                "warning_text",
                "You will lose ALL your progress.",
                container_width / 2,
                question_text.rect.bottom + Config.ELEMENT_OUTER_PADDING,
                size=Config.FONT_SIZE_MEDIUM,
                anchor=RectAnchorMode.MIDTOP,
                fg_color=Config.RED,
                wrap_length=container_width,
            )

            yes_button = Button(
                "erase_data_yes_button",
                Config.ELEMENT_OUTER_PADDING,
                warning_text.rect.bottom + Config.ELEMENT_OUTER_PADDING,
                button_width,
                button_height,
                text=Text(
                    "yes_button_text",
                    "Yes",
                    button_width / 2,
                    button_height / 2,
                    anchor=RectAnchorMode.CENTER,
                    fg_color=Config.RED,
                ),
            )
            no_button = Button(
                "erase_data_no_button",
                yes_button.rect.right + Config.ELEMENT_OUTER_PADDING,
                warning_text.rect.bottom + Config.ELEMENT_OUTER_PADDING,
                button_width,
                button_height,
                text=Text(
                    "no_button_text",
                    "No",
                    button_width / 2,
                    button_height / 2,
                    anchor=RectAnchorMode.CENTER,
                ),
            )

            main_container.add_element(question_text)
            main_container.add_element(warning_text)
            main_container.add_element(yes_button)
            main_container.add_element(no_button)
            self.add_element(main_container)

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == CUSTOM_BUTTON_CLICKED:
            logger.debug(f"gui button clicked: id={event.button.id}")

            if self.state == MainMenuSceneGUIState.NORMAL:
                if event.button.id == "play_button":
                    self.scene.game.scene_manager.switch(MapSelectorScene(self.scene.game))
                elif event.button.id == "tower_shop_button":
                    self.scene.game.scene_manager.switch(TowerShopScene(self.scene.game))
                elif event.button.id == "quit_button":
                    self.scene.game.save_quit()
                elif event.button.id == "erase_data_button":
                    self.state = MainMenuSceneGUIState.CONFIRM_ERASE_DATA
                    self.refresh()
            elif self.state == MainMenuSceneGUIState.CONFIRM_ERASE_DATA:
                if event.button.id == "erase_data_yes_button":
                    reset_data()
                    self.scene.game.player_save = load_data_from_file()
                    self.state = MainMenuSceneGUIState.NORMAL
                    self.refresh()
                elif event.button.id == "erase_data_no_button":
                    self.state = MainMenuSceneGUIState.NORMAL
                    self.refresh()


class MainMenuScene(Scene):
    def __init__(self, game: "GameApp"):
        super().__init__(game)

        self.music_playlist = ALL_MAP_MUSIC  # couldn't decide on one
        random.shuffle(self.music_playlist)

        self.music_index = 0
        self.music_channel = pygame.mixer.find_channel()

        self.gui_manager = MainMenuSceneGUIManager(self)

        self.background = load_scaled_asset(
            "main_menu", (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        )

    def on_enter(self) -> None:
        self.play_next_music()

    def on_exit(self) -> None:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def play_next_music(self):
        current_music = self.music_playlist[self.music_index]
        pygame.mixer.music.load(get_sound(current_music))
        pygame.mixer.music.play(fade_ms=Config.DEFAULT_SOUND_FADEIN_MS)

        to_queue = self.music_playlist[
            (self.music_index + 1) % len(self.music_playlist)
        ]
        pygame.mixer.music.queue(get_sound(to_queue))

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.background, (0, 0))

        game_icon = load_asset("game_icon")
        game_icon_rect = game_icon.get_rect(
            center=(Config.SCREEN_WIDTH / 2, Config.SCREEN_HEIGHT * 0.25)
        )
        surface.blit(game_icon, game_icon_rect)

        self.gui_manager.render_elements(surface)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            self.gui_manager.handle_event(event)

            if event.type == pygame.mixer.music.get_endevent():
                self.play_next_music()

    def update(self, delta_time: float) -> None:
        self.gui_manager.update_elements(delta_time, pygame.mouse.get_pos())
