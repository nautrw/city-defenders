import pygame


class Enemy(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    def __init__(self, image: pygame.Surface, movement_speed: int, max_health: int, path_waypoints: list[tuple[float, float]]):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()

        self.path_waypoints = path_waypoints
        self.waypoint_index = 1
        self.movement_target = self.path_waypoints[self.waypoint_index]
        self.position = pygame.Vector2(self.path_waypoints[0])
        self.velocity = pygame.Vector2()

        self.movement_speed = movement_speed
        self.max_health = max_health
        self.health = max_health

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
    
    def update(self, dt: float) -> None:
        if self.waypoint_index < len(self.path_waypoints):
            heading = self.movement_target - pygame.Vector2(self.rect.center)
            distance_to_target = heading.length()
            heading.normalize_ip()

            if distance_to_target <= 2:
                self.waypoint_index += 1
                self.movement_target = self.path_waypoints[self.waypoint_index]

            self.velocity = heading * self.movement_speed * dt

        self.position += self.velocity
        self.rect.center = self.position
