from typing import ClassVar

import pygame
from pygame.geometry import Circle
from pygame.typing import ColorLike

import src.core.config as Config
from src.core.utils import angle_to_point, load_asset
from src.entities.enemies.enemy import Enemy
from src.entities.projectiles.ballistic_projectile import (
    BallisticProjectile,
    BallisticProjectileType,
)


class Tower(pygame.sprite.Sprite):
    display_name: ClassVar[str]
    description: ClassVar[str]

    cost: ClassVar[tuple[int, ...]]
    damage: ClassVar[tuple[float, ...]]
    shooting_speed: ClassVar[tuple[float, ...]]
    area_radius: ClassVar[tuple[float, ...]]

    projectile: ClassVar[BallisticProjectileType]

    shards_cost: ClassVar[int]

    def __init__(
        self,
        x_position: float,
        y_position: float,
        tower_image: list[pygame.Surface],
    ) -> None:
        super().__init__()

        self.position = pygame.Vector2(x_position, y_position)

        self.upgrade_index = 0

        self.original_base_image = load_asset("tower_base")
        self.base = self.original_base_image.copy()
        self.original_tower_images = tower_image
        self.tower_image = tower_image[self.upgrade_index]

        # tower needs to have a separate rect because of rotation, so i use
        # the base as the rect
        self.rect = self.base.get_frect(center=self.position)
        self.tower_rect = self.tower_image.get_frect(center=self.position)

        assert self.rect is not None

        # can shoot immediately after placing
        self.shoot_cooldown_delta_time = self.shooting_speed[self.upgrade_index]

        self.area = Circle(self.rect.center, self.area_radius[self.upgrade_index])

        self.tower_angle = 0

        self.tower_tip = pygame.Vector2(0, -self.tower_image.get_height() / 2)

    def _shoot_at(self, enemy: Enemy) -> BallisticProjectile:
        projectile_offset = self.tower_tip.rotate(-self.tower_angle)
        projectile_position = self.position + projectile_offset

        projectile = self.projectile(
            damage=self.damage[self.upgrade_index],
            x_position=projectile_position[0],
            y_position=projectile_position[1],
            target=enemy,
        )
        return projectile

    def move_center(self, new_x: float, new_y: float) -> None:
        assert self.rect is not None

        self.position = (new_x, new_y)
        self.rect.center = self.position
        self.tower_rect.center = self.position
        self.area.center = self.position

    def draw(
        self,
        surface: pygame.Surface,
        draw_radiuses: bool,
        overlay_color: ColorLike | None = None,
    ) -> None:
        assert self.rect is not None
        self.base = self.original_base_image.copy()

        if draw_radiuses:
            circle_surf = pygame.Surface(self.area.as_frect().size, pygame.SRCALPHA)
            radius = self.area.radius
            pygame.draw.circle(
                circle_surf,
                Config.TOWER_RADIUS_COLOR,
                (radius, radius),
                radius,
            )
            surface.blit(circle_surf, self.area.as_frect())

        self.tower_image = pygame.transform.rotozoom(
            self.original_tower_images[self.upgrade_index], self.tower_angle, 1
        )
        self.tower_rect = self.tower_image.get_frect(center=self.rect.center)

        if overlay_color:
            self.base.fill(overlay_color, special_flags=pygame.BLEND_RGBA_MIN)
            self.tower_image.fill(overlay_color, special_flags=pygame.BLEND_RGBA_MIN)

        surface.blit(self.base, self.rect)
        surface.blit(self.tower_image, self.tower_rect)

    def upgrade(self) -> None:
        assert self.rect is not None

        self.upgrade_index += 1
        self.area = Circle(self.rect.center, self.area_radius[self.upgrade_index])

    def update(
        self,
        delta_time: float,
        enemies_group: pygame.sprite.Group,
        projectiles_group: pygame.sprite.Group,
        game_speed_multiplier: int,
    ) -> None:
        assert self.rect is not None

        for enemy in enemies_group:
            if self.area.colliderect(enemy.rect):
                self.tower_angle = angle_to_point(
                    self.rect.centerx,
                    self.rect.centery,
                    enemy.rect.centerx,
                    enemy.rect.centery,
                )

                if (
                    self.shoot_cooldown_delta_time
                    >= self.shooting_speed[self.upgrade_index]
                ):
                    projectile = self._shoot_at(enemy)
                    projectiles_group.add(projectile)
                    self.shoot_cooldown_delta_time = 0

        self.shoot_cooldown_delta_time += delta_time * game_speed_multiplier
