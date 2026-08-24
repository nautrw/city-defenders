from os import path

import pygame

from src.entities.enemies.enemy import Enemy


class Slime(Enemy):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self, x: float, y: float):
        image = pygame.image.load(
            path.join("src", "assets", "entities", "slime.png")
        ).convert_alpha()

        super().__init__(image=image, movement_speed=5, max_health=10)

        self.rect.center = (x, y)
