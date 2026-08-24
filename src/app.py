from os import path

import pygame

from src.core.config import config as Config
from src.core.map import GameMap
from src.core.scenes_manager import SceneManager
from src.core.utils import clean_map_json, load_json_file, split_tileset
from src.scenes.main_game import MainGameScene


class GameApp:
    def __init__(self) -> None:
        pygame.init()

        self.running = True

        self.screen = pygame.display.set_mode(
            (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), Config.FLAGS
        )

        self.clock = pygame.time.Clock()
        self.delta_time = 0

        tileset_img = pygame.image.load("src/assets/tiles/tileset.png").convert_alpha()
        tileset = split_tileset(tileset_img, Config.TILE_WIDTH, Config.TILE_HEIGHT)
        map_data = clean_map_json(
            load_json_file(path.join("src", "assets", "maps", "Test.json"))
        )

        self.scene_manager = SceneManager()
        self.scene_manager.push(MainGameScene(self, GameMap(tileset, map_data)))

    def run(self) -> None:
        try:
            while self.running:
                events = pygame.event.get()

                for event in events:
                    if event.type == pygame.QUIT:
                        # reminder that all exit logic is in the `finally` block
                        # near the bottom of the function
                        self.running = False

                if self.scene_manager.current_scene:
                    self.scene_manager.current_scene.handle_events(events)
                    self.scene_manager.current_scene.update(self.delta_time)
                    self.scene_manager.current_scene.render(self.screen)

                pygame.display.flip()
                self.delta_time = self.clock.tick(Config.FPS) / 1000.0
        finally:
            pygame.quit()
