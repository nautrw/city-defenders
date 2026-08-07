import pygame
from src.core.scenes_manager import Scene, SceneManager
from src.core.config import config as Config
from src.core.base_gun import BaseGun
from src.core.base_ship import BaseShip

class Gun(BaseGun):
    # pygame.Sprite defaults these two to None and by LSP will scream at me
    # if I don't put these
    rect: pygame.Rect | pygame.FRect
    image: pygame.Surface

    def __init__(self):
        super().__init__(9.5, 53.5)

        self.image = pygame.image.load("src/assets/guns/basic-gun.png")
        self.rect = self.image.get_rect()

class Ship(BaseShip):
    # pygame.Sprite defaults these two to None and by LSP will scream at me
    # if I don't put these
    rect: pygame.Rect | pygame.FRect
    image: pygame.Surface

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("src/assets/ships/corvette.png")
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)

        self.equipped_guns = [Gun()]
        self.gun_placements = ((46.5, 97.5),)
        


class MainGameScene(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager)
        
        self.screen_width = Config.SCREEN_WIDTH
        self.screen_height = Config.SCREEN_HEIGHT
        self.ship = Ship()

    def handle_events(self, events: list[pygame.Event]):
        pass
    
    def update(self, delta_time: int | float):
        pass

    def render(self, screen: pygame.Surface):
        self.ship.draw(screen)
