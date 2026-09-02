import pygame


class Camera:
    def __init__(
        self,
        viewport_width: float,
        viewport_height: float,
        world_width: float,
        world_height: float,
        world_scale_factor: int = 1,
    ) -> None:
        self.offset = pygame.Vector2()
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.world_width = world_width
        self.world_height = world_height
        self.world_scale_factor = world_scale_factor

    def viewport_to_world(self, viewport_x: float, viewport_y: float) -> tuple[float, float]:
        viewport_pos = pygame.Vector2(viewport_x, viewport_y)

        world_coord = (viewport_pos / self.world_scale_factor) + self.offset
        return (world_coord.x, world_coord.y)

    def move(self, delta_x: float, delta_y: float, clamp: bool = True) -> tuple[float, float]:
        movement = pygame.Vector2(delta_x, delta_y)
        new_offset = self.offset - movement

        if not clamp:
            self.offset += movement
        else:
            # if (
            #     0
            #     < new_offset.x
            #     < self.world_width - (self.viewport_width / self.world_scale_factor)
            # ):
            #     self.offset.x -= movement.x
            # if (
            #     0
            #     < new_offset.y
            #     < self.world_height - (self.viewport_height / self.world_scale_factor)
            # ):
            # self.offset.y -= movement.y

            self.offset.x = min(
                max(0, new_offset.x),
                (self.world_width - (self.viewport_width / self.world_scale_factor)),
            )

            self.offset.y = min(
                max(0, new_offset.y),
                self.world_height - (self.viewport_height / self.world_scale_factor),
            )

        return (int(self.offset.x), int(self.offset.y))
