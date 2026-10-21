import pygame


class Particle(pygame.sprite.Sprite):
    def __init__(
        self,
        initial_x: float,
        initial_y: float,
        image: pygame.Surface,
        lifetime: float = 1,
        velocity_x: float = 0.0,
        velocity_y: float = -0.5,
    ) -> None:
        super().__init__()
        self.image = image
        assert self.image is not None
        self.rect = self.image.get_frect(center=(initial_x, initial_y))

        self.velocity = pygame.Vector2(velocity_x, velocity_y)

        self.age = 0.0
        self.lifetime = lifetime

    def update(self, delta_time: float, speed_multiplier: float) -> None:
        assert self.rect is not None
        
        self.age += delta_time * speed_multiplier

        self.rect.center += self.velocity * speed_multiplier

        if self.age >= self.lifetime:
            self.kill()
    
    def draw(self, surface: pygame.Surface):
        assert self.image is not None
        assert self.rect is not None
        
        surface.blit(self.image, self.rect)