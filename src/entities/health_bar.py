import pygame

import src.core.config as Config


class HealthBar(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(
        self,
        width: float = 28.0,
        height: float = 5.0,
        border_width: float = 1.0,
        position_offset: float = -4.0,
    ):
        super().__init__()

        self.width = width
        self.height = height
        self.border_width = border_width
        self.border_offset = self.border_width * 2
        self.position_offset = position_offset

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_frect()

        self.health_percent = 1.0

    def update(
        self, current_health: int, max_health: int, position: tuple[float, float]
    ):
        self.rect.centerx = int(position[0])
        self.rect.centery = int(position[1] + self.position_offset)

        self.health_percent = current_health / max_health

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

        # multiplied by 2 to account for all sides of the bar having the border
        border_offset = self.border_width * 2
        width_inside_border = self.width - border_offset
        height_inside_border = self.height - border_offset
        self.image.fill("black")

        health_width = int(self.health_percent * width_inside_border)

        # color linear interpolation allows for the gradient shifting as
        # the health decreases
        color = pygame.Color.lerp(
            pygame.Color(Config.LOW_HEALTH_COLOR),
            pygame.Color(Config.MAX_HEALTH_COLOR),
            self.health_percent,
        )

        pygame.draw.rect(
            self.image,
            color,
            pygame.Rect(
                self.border_width, self.border_width, health_width, height_inside_border
            ),
        )
