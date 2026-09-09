from typing import TYPE_CHECKING

import pygame

import src.core.config as Config
from src.core.scenes_manager import Scene
from src.core.utils import get_font

if TYPE_CHECKING:
    from src.app import GameApp


class GameWonScene(Scene):
    def __init__(self, game: "GameApp"):
        super().__init__(game)

    def handle_events(self, events: list[pygame.Event]) -> None:
        pass

    def update(self, delta_time: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(Config.FULL_HEALTH_COLOR)
        font = pygame.font.Font(get_font(Config.FONT_NORMAL), Config.FONT_SIZE_VERYBIG)
        text = font.render("Game Over", True, Config.TEXT_COLOR_NORMAL)
        text_rect = text.get_frect(
            center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2)
        )
        surface.blit(text, text_rect)
