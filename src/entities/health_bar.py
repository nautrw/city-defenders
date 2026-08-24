import pygame


class HealthBar(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self, width: int = 28, height: int = 5, border_width: int = 1):
        super().__init__()

        self.width = width
        self.height = height
        self.border_width = border_width
        self.border_offset = self.border_width * 2

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()

    def update(self, current_health: int, max_health: int, position: tuple[float, float]):
        # multiplied by 2 to account for all sides of the bar having the border
        border_offset = self.border_width * 2
        width_inside_border = self.width - border_offset
        height_inside_border = self.height - border_offset

        self.rect.centerx = int(position[0])
        self.rect.centery = int(position[1] - 4)

        self.image.fill("black")

        if current_health >= max_health / width_inside_border:
            health_percent = current_health / max_health
            health_width = int(health_percent * width_inside_border)

            # color linear interpolation allows for the gradient shifting as
            # the health decreases
            color = pygame.Color.lerp(pygame.Color(255, 0, 0), pygame.Color(0, 255, 0), health_percent)

            pygame.draw.rect(self.image, color, pygame.Rect(self.border_width, self.border_width, health_width, height_inside_border))
    
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
