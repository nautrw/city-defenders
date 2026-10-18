from src.gui.gui_utils import build_stat_display
from src.gui.container import ElementContainer
from typing import TYPE_CHECKING

import pygame
from loguru import logger

import src.core.config as Config
from src.core.scenes_manager import Scene
from src.core.utils import get_sound, load_scaled_asset
from src.gui.button import CUSTOM_BUTTON_CLICKED, Button
from src.gui.gui_manager import GUIManager
from src.gui.placement_system import RectAnchorMode
from src.gui.text import Text

if TYPE_CHECKING:
    from src.app import GameApp


class GameDefeatSceneGUIManager(GUIManager):
    def __init__(self, scene: "GameLostScene"):
        self.scene: GameLostScene

        super().__init__(scene)

        self.refresh()

    def refresh(self) -> None:
        self.elements = []

        defeat_plaque_img = load_scaled_asset("defeat_plaque", (360, 432))
        defeat_plaque = ElementContainer(
            "defeat_plaque",
            Config.SCREEN_WIDTH / 2,
            Config.SCREEN_HEIGHT * .4,
            *defeat_plaque_img.size,
            bg_image=defeat_plaque_img,
            anchor=RectAnchorMode.CENTER
        )

        defeat_text = Text(
            "defeat_text",
            "Defeated...",
            defeat_plaque.rect.width / 2,
            defeat_plaque.rect.height * .24,
            size=Config.FONT_SIZE_XXXLARGE,
            anchor=RectAnchorMode.MIDTOP,
        )

        shards_reward = build_stat_display(
            "shards_reward",
            f"+{self.scene.shards_reward}",
            defeat_plaque.rect.width / 2,
            defeat_plaque.rect.height * .65, # wanted it to be 67 so bad :(
            icon_name="shard_icon",
            anchor=RectAnchorMode.MIDTOP,
            text_size=Config.FONT_SIZE_XLARGE
        )

        button_width = Config.BUTTON_SIZE * 3
        play_again_button = Button(
            "play_again_button",
            Config.SCREEN_WIDTH / 2,
            defeat_plaque.rect.bottom + Config.ELEMENT_OUTER_PADDING,
            button_width,
            Config.BUTTON_SIZE,
            text=Text(
                "play_again_button_text",
                "Play Again",
                button_width / 2,
                Config.BUTTON_SIZE / 2,
                size=Config.FONT_SIZE_LARGE,
                anchor=RectAnchorMode.CENTER,
            ),
            anchor=RectAnchorMode.MIDTOP,
        )

        self.add_element(defeat_plaque)
        defeat_plaque.add_element(defeat_text)
        defeat_plaque.add_element(shards_reward)
        self.add_element(play_again_button)


    def handle_event(self, event: pygame.Event) -> None:
        if event.type == CUSTOM_BUTTON_CLICKED:
            logger.debug(f"gui button clicked: id={event.button.id}")

            if event.button.id == "play_again_button":
                # prevent circular import
                from src.scenes.map_selector import MapSelectorScene

                # stack is [maingame, GameLostScene] before emptying
                self.scene.game.scene_manager.empty_stack()
                self.scene.game.scene_manager.push(MapSelectorScene(self.scene.game))


class GameLostScene(Scene):
    def __init__(self, game: "GameApp", shards_reward: int) -> None:
        self.shards_reward = shards_reward

        super().__init__(game)

        self.gui_manager = GameDefeatSceneGUIManager(self)

    def on_enter(self) -> None:
        pygame.mixer.music.load(get_sound("The Fallen"))
        pygame.mixer.music.play(loops=-1, fade_ms=Config.DEFAULT_SOUND_FADEIN_MS)

    def on_exit(self) -> None:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            self.gui_manager.handle_event(event)

    def update(self, delta_time: float) -> None:
        self.gui_manager.update_elements(delta_time, pygame.mouse.get_pos())

    def render(self, surface: pygame.Surface) -> None:
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill(Config.DARK_BG)
        surface.blit(overlay)

        self.gui_manager.render_elements(surface)
