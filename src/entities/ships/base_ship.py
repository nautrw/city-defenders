import pygame
from src.entities.turrets.base_turret import BaseTurret

class BaseShip(pygame.sprite.Sprite):
    # pygame.Sprite defaults these two to None and by LSP will scream at me
    # if I don't put these
    rect: pygame.Rect | pygame.FRect
    image: pygame.Surface

    def __init__(self) -> None:
        super().__init__()

        self.display_name: str
        self.description: str

        self.image: pygame.Surface

        self.equipped_turrets: list[BaseTurret] # subclasses can be added too

        # set of x,y coordinates corresponding to points on the sprite image
        # where the guns are attached to (see the draw method);
        # also determines how many turrets a spaceship supports
        self.mounting_points: tuple[tuple[int | float, int | float], ...]

    def update(self, delta_time: int | float) -> None:
        ...
    
    def draw(self, screen: pygame.Surface) -> None:
        for gun_obj in self.equipped_turrets:
            for placement in self.mounting_points:
                gun_image = gun_obj.image
                gun_rect = gun_image.get_rect()
                acx, acy = gun_obj.attachment_center
                px, py = placement
                gun_rect.topleft = (px - acx, py - acy)
                self.image.blit(gun_image, gun_rect)

                screen.blit(self.image, self.rect)
