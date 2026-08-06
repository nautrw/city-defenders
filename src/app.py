import pygame
import sys

FPS = 60

class GameApp:
    def __init__(self):
        pygame.init()

        self.running = True

        self.screen = pygame.display.set_mode((500, 500))
        self.screen_width = 500
        self.screen_height = 500

        self.clock = pygame.time.Clock()
        self.delta_time = 0

    def run(self):
        try:
            while self.running:
                if pygame.event.get(pygame.QUIT):
                    # reminder that all exit logic is in the `finally` block
                    # near the bottom of the function
                    self.running = False

                pygame.display.flip()
                self.delta_time = self.clock.tick(FPS) / 1000.0
        finally:
            pygame.quit()

if __name__ == "__main__":
    app = GameApp()
    app.run()
