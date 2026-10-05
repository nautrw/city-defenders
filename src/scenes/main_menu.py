import random
from typing import TYPE_CHECKING

import pygame
from loguru import logger

import src.core.config as Config
from src.core.scenes_manager import Scene
from src.core.utils import get_sound, load_asset
from src.gui.button import CUSTOM_BUTTON_CLICKED, Button
from src.gui.gui_manager import GUIManager
from src.gui.placement_system import RectAnchorMode
from src.gui.text import Text
from src.maps.data import ALL_MAP_MUSIC
from src.scenes.map_selector import MapSelectorScene

if TYPE_CHECKING:
    from src.app import GameApp


class MainMenuSceneGUIManager(GUIManager):
    def __init__(self, scene: "MainMenuScene") -> None:

        super().__init__(scene)

        self.refresh()

    def refresh(self) -> None:
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
        if event.type == CUSTOM_BUTTON_CLICKED:
            logger.debug(f"gui button clicked: id={event.button.id}")

            if event.button.id == "play_button":
                self.scene.game.scene_manager.switch(MapSelectorScene(self.scene.game))


class MainMenuScene(Scene):
    def __init__(self, game: "GameApp"):
        super().__init__(game)

        self.music_playlist = ALL_MAP_MUSIC  # couldnt decide on one
        random.shuffle(self.music_playlist)

        self.music_index = 0
        self.music_channel = pygame.mixer.find_channel()
        self.play_next_music()

        self.gui_manager = MainMenuSceneGUIManager(self)

    def play_next_music(self):
        current_music = self.music_playlist[self.music_index]
        pygame.mixer.music.load(get_sound(current_music))
        pygame.mixer.music.play(fade_ms=Config.DEFAULT_SOUND_FADEIN_MS)

        to_queue = self.music_playlist[
            (self.music_index + 1) % len(self.music_playlist)
        ]
        pygame.mixer.music.queue(get_sound(to_queue))

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(Config.BRIGHT_GREEN)

        game_icon = load_asset("game_icon")
        game_icon_rect = game_icon.get_rect(
            center=(Config.SCREEN_WIDTH / 2, Config.SCREEN_HEIGHT * 0.25)
        )
        surface.blit(game_icon, game_icon_rect)

        self.gui_manager.render_elements(surface)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            self.gui_manager.handle_event(event)

            if event == pygame.mixer.music.get_endevent():
                self.play_next_music()

    def update(self, delta_time: float) -> None:
        self.gui_manager.update_elements(delta_time, pygame.mouse.get_pos())
