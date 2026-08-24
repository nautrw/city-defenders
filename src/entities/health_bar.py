import pygame


class HealthBar(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((28, 5))
        self.rect = self.image.get_rect()

    def update(self, current_health: int, max_health: int, position: tuple[float, float]):
        self.rect.centerx = int(position[0])
        self.rect.centery = int(position[1] - 4)

        self.image.fill("black")

        if current_health >= max_health / 26:
            pygame.draw.rect(self.image, "green", pygame.Rect(1, 1, int(current_health / max_health * 26), 3))
    
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
