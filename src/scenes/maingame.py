import pygame
from src.core.scenes_manager import Scene, SceneManager
from src.core.config import config as Config
from src.entities.ships.corvette import CorvetteShip
from src.entities.turrets.sentinel import SentinelTurret

class MainGameScene(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager)
        
        self.screen_width = Config.SCREEN_WIDTH
        self.screen_height = Config.SCREEN_HEIGHT
        self.ship = CorvetteShip([SentinelTurret()])

    def handle_events(self, events: list[pygame.Event]):
        pass
    
    def update(self, delta_time: int | float):
        pass

    def render(self, screen: pygame.Surface):
        self.ship.draw(screen)
