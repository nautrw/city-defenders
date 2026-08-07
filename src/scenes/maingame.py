import pygame
from src.core.scenes_manager import Scene, SceneManager
from src.core.config import config as Config
from src.core.base_turret import BaseTurret
from src.entities.ships.corvette import CorvetteShip

class Turret(BaseTurret):
    # pygame.Sprite defaults these two to None and by LSP will scream at me
    # if I don't put these
    rect: pygame.Rect | pygame.FRect
    image: pygame.Surface

    def __init__(self):
        super().__init__(7, 33)

        self.image = pygame.image.load("src/assets/turrets/basic_turret.png")
        self.rect = self.image.get_rect()

class MainGameScene(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager)
        
        self.screen_width = Config.SCREEN_WIDTH
        self.screen_height = Config.SCREEN_HEIGHT
        self.ship = CorvetteShip([Turret()])

    def handle_events(self, events: list[pygame.Event]):
        pass
    
    def update(self, delta_time: int | float):
        pass

    def render(self, screen: pygame.Surface):
        self.ship.draw(screen)
