from src.gui.container import ElementContainer
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
from src.entities.entity_data import TOWERS
from src.gui.button import CUSTOM_BUTTON_CLICKED, Button
from src.gui.gui_manager import GUIManager
from src.gui.gui_utils import build_stat_display
from src.gui.icon import Icon
from src.gui.placement_system import RectAnchorMode

if TYPE_CHECKING:
    from src.app import GameApp


class TowerShopGUIManager(GUIManager):
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

        shards_display_container = build_stat_display(
            "shards_display",
            f"{self.scene.game.player_save.shards}",
            Config.SCREEN_WIDTH / 2,
            Config.ELEMENT_OUTER_PADDING,
            icon_name="shard_icon",
            text_size=Config.FONT_SIZE_XLARGE,
            anchor=RectAnchorMode.MIDTOP,
        )

        self.elements.append(shards_display_container)

        container_width = Config.SCREEN_WIDTH / 1.75
        container_height = 960 * .75
        menu_container = ElementContainer(
            "tower_menu_container",
            Config.SCREEN_WIDTH / 2,
            Config.SCREEN_HEIGHT * .15,
            container_width,
            container_height,
            bg_color=Config.DARKER_BG,
            anchor=RectAnchorMode.MIDTOP
        )

        current_tower = self.scene.towers[self.scene.tower_index]
        
        tower_icon = Icon(
            "tower_icon",
            Config.ELEMENT_OUTER_PADDING * 2,
            Config.ELEMENT_OUTER_PADDING * 2,
            load_scaled_asset(f"{current_tower}_0", (250, 250)),
        )

        menu_container.add_element(tower_icon)
        self.elements.append(menu_container)

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
            Config.SCREEN_WIDTH * 0.80,
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
            Config.SCREEN_WIDTH * 0.20,
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

            if event.button.id == "back_to_main_menu_button":
                # prevent circular import
                from src.scenes.main_menu import MainMenuScene

                self.scene.game.scene_manager.switch(MainMenuScene(self.scene.game))
            elif event.button.id == "go_left_button":
                self.scene.tower_index -= 1
                self.scene.tower_index %= len(self.scene.towers)
            elif event.button.id == "go_right_button":
                self.scene.tower_index += 1
                self.scene.tower_index %= len(self.scene.towers)

            self.refresh()


class TowerShopScene(Scene):
    def __init__(self, game: "GameApp"):
        super().__init__(game)

        self.selected_map_index = 0
        self.background = load_scaled_asset(
            "tower_shop", (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        )

        self.towers = list(TOWERS.keys())
        self.tower_index = 0

        self.gui_manager = TowerShopGUIManager(self)

    def on_enter(self) -> None:
        pygame.mixer.music.load(get_sound("Classical Medieval Song"))
        pygame.mixer.music.play(loops=-1, fade_ms=Config.DEFAULT_SOUND_FADEIN_MS)

    def on_leave(self) -> None:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.background, (0, 0))

        self.gui_manager.render_elements(surface)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            self.gui_manager.handle_event(event)

    def update(self, delta_time: float) -> None:
        self.gui_manager.update_elements(delta_time, pygame.mouse.get_pos())

    def on_exit(self) -> None:
        pygame.mixer.music.stop()
