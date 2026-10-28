from typing import TYPE_CHECKING

import pygame
from loguru import logger

import src.core.config as Config
from src.core.scenes_manager import Scene
from src.core.utils import load_scaled_asset
from src.gui.button import CUSTOM_BUTTON_CLICKED, Button
from src.gui.container import ElementContainer
from src.gui.gui_manager import GUIManager
from src.gui.placement_system import RectAnchorMode
from src.gui.text import Text

if TYPE_CHECKING:
    from src.app import GameApp


CREDITS: list[dict[str, str]] = [
    {
        "title": "Oleaguid Font",
        "author": "arynoc",
        "modification": "Removed short quiet segments at the beginning and end.",
    },
    {
        "title": "Heroic Demise (Updated Version)",
        "author": "Matthew Pablo",
        "modification": "Removed short quiet segments at the beginning and end.",
    },
    {
        "title": "Soliloquy",
        "author": "Matthew Pablo",
        "modification": "Compressed; removed short quiet segments at the beginning and end.",
    },
    {
        "title": "The Fall of Arcana (New Era Version)",
        "author": "Matthew Pablo",
        "modification": "Removed short quiet segments at the beginning and end.",
    },
    {
        "title": "Classical/Medieval Song",
        "author": "professorlamp",
        "modification": "Removed short quiet segments at the beginning and end.",
    },
    {
        "title": "Can't Stop Winning",
        "author": "Jonathan Shaw",
        "modification": "Removed short quiet segments at the beginning and end.",
    },
    {
        "title": "The Fallen",
        "author": "Jonathan Shaw",
        "modification": "Removed short quiet segments at the beginning and end.",
    },
    {
        "title": "The Bard's Tale",
        "author": "RandomMind",
        "modification": "Removed short quiet segments at the beginning and end.",
    },
    {
        "title": "The Bard's Tale",
        "author": "RandomMind",
        "modification": "Removed short quiet segments at the beginning and end.",
    },
]


class CreditsSceneGUIManager(GUIManager):
    def refresh(self) -> None:
        credit_box_side_len = 230
        cards_per_row = (Config.SCREEN_WIDTH - Config.ELEMENT_OUTER_PADDING) // (
            credit_box_side_len + Config.ELEMENT_OUTER_PADDING
        )

        credits_title = Text(
            "title",
            "Credits",
            Config.SCREEN_WIDTH / 2,
            Config.ELEMENT_OUTER_PADDING,
            Config.FONT_SIZE_XXLARGE,
            anchor=RectAnchorMode.MIDTOP,
        )
        self.add_element(credits_title)

        back_button = Button(
            "back_button",
            Config.ELEMENT_OUTER_PADDING,
            Config.ELEMENT_OUTER_PADDING,
            Config.BUTTON_SIZE,
            Config.BUTTON_SIZE,
            normal_icon=load_scaled_asset("close_icon"),
        )
        self.add_element(back_button)

        for i, card in enumerate(CREDITS):
            title, author, mod = card.values()

            x = Config.ELEMENT_OUTER_PADDING + (
                (i % cards_per_row)
                * (credit_box_side_len + Config.ELEMENT_OUTER_PADDING)
            )
            y = (
                max(credits_title.rect.bottom, back_button.rect.bottom)
                + Config.ELEMENT_OUTER_PADDING
                + (
                    (i // cards_per_row)
                    * (credit_box_side_len + Config.ELEMENT_OUTER_PADDING)
                )
            )

            container = ElementContainer(
                f"c{i}",
                x,
                y,
                credit_box_side_len,
                credit_box_side_len,
            )

            text = Text(
                f"{title}_credit_card_text",
                f"{title} - {author} ({mod})",
                Config.ELEMENT_OUTER_PADDING,
                Config.ELEMENT_OUTER_PADDING,
                size=Config.FONT_SIZE_SMALL,
                wrap_length=credit_box_side_len - Config.ELEMENT_OUTER_PADDING,
            )
            container.add_element(text)

            self.add_element(container)

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == CUSTOM_BUTTON_CLICKED:
            logger.debug(f"gui button clicked: id={event.button.id}")

            if event.button.id == "back_button":
                from src.scenes.main_menu import MainMenuScene

                self.scene.game.scene_manager.switch(MainMenuScene(self.scene.game))


class CreditsScene(Scene):
    def __init__(self, game: "GameApp"):
        super().__init__(game)

        self.gui_manager = CreditsSceneGUIManager(self)

        self.background = load_scaled_asset(
            "main_menu", (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        )

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.background, (0, 0))
        self.gui_manager.render_elements(surface)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            self.gui_manager.handle_event(event)

    def update(self, delta_time: float) -> None:
        self.gui_manager.update_elements(delta_time, pygame.mouse.get_pos())
