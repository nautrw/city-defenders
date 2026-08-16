import pygame
import sys
from src.core.config import config as Config
from src.scenes.main_game import MainGameScene
from src.core.scenes_manager import SceneManager, Scene

class GameApp:
    def __init__(self) -> None:
        pygame.init()

        self.running = True

        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), Config.FLAGS)

        self.clock = pygame.time.Clock()
        self.delta_time = 0

        self.scene_manager = SceneManager()
        self.scene_manager.push(MainGameScene(self, map_data = [
            [  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8, 11,  8,  8, ],
            [  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8, 11,  8,  8, ],
            [  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8, 11,  8,  8, ],
            [  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8,  8, 11,  8,  8, ],
            [  8,  8,  8, 11, 11, 11, 11, 11, 11,  8,  8,  8, 11,  8,  8, ],
            [  8,  8,  8, 11,  8,  8,  8,  8, 11,  8,  8,  8, 11,  8,  8, ],
            [  8,  8,  8, 11,  8,  8,  8,  8, 11,  8,  8,  8, 11,  8,  8, ],
            [  8,  8,  8, 11,  8,  8,  8,  8, 11,  8,  8,  8, 11,  8,  8, ],
            [  8,  8,  8, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,  8,  8, ],
            [  8,  8,  8,  8,  8,  8,  8,  8, 11,  8,  8,  8,  8,  8,  8, ],
            [  8,  8,  8, 11, 11, 11,  8,  8, 11,  8,  8,  8,  8,  8,  8, ],
            [  8,  8,  8, 11,  8, 11,  8,  8, 11,  8,  8,  8,  8,  8,  8, ],
            [  8,  8,  8, 11, 11, 11, 11, 11, 11,  8,  8,  8,  8,  8,  8, ],
            [  8,  8,  8,  8,  8, 11,  8,  8,  8,  8,  8,  8,  8,  8,  8, ],
            [  8,  8,  8,  8,  8, 11,  8,  8,  8,  8,  8,  8,  8,  8,  8, ],
        ]))

    def run(self) -> None:
        try:
            while self.running:
                if pygame.event.get(pygame.QUIT):
                    # reminder that all exit logic is in the `finally` block
                    # near the bottom of the function
                    self.running = False
                
                if self.scene_manager.current_scene:
                    self.scene_manager.current_scene.handle_events(pygame.event.get())
                    self.scene_manager.current_scene.update(self.delta_time)
                    self.scene_manager.current_scene.render(self.screen)

                pygame.display.flip()
                self.delta_time = self.clock.tick(Config.FPS) / 1000.0
        finally:
            pygame.quit()
