import random
from enum import Enum, auto
from typing import TYPE_CHECKING

import pygame
from loguru import logger

import src.core.config as Config
from src.core.camera import Camera
from src.core.map import GameMap
from src.core.scenes_manager import Scene
from src.core.utils import get_sound, load_map, split_tileset, load_asset
from src.maps.data import MAPS_DATA
from src.entities.enemies.enemy import DEFENSE_BREACHED, ENEMY_KILLED
from src.entities.entity_data import ENEMIES
from src.entities.towers.tower import Tower, TowerType
from src.scenes.game_lost import GameLostScene
from src.scenes.game_won import GameWonScene
from src.scenes.main_game_gui_manager import MainGameSceneGUIManager, UIStates
from src.scenes.pause_menu import PauseMenuScene

# Solves the circular import error as a result of src.app being uninitialized
# TYPE_CHECKING is false at runtime so the lsp can still see it but it's not
# actually imported
if TYPE_CHECKING:
    from src.app import GameApp


class WaveState(Enum):
    SPAWNING = auto()
    CLEARING = auto()


class MainGameScene(Scene):
    # def __init__(self, game: "GameApp", map: GameMap, map_data: dict) -> None:
    def __init__(self, game: "GameApp", map_name: str) -> None:
        super().__init__(game)

        if not map_name or (map_name not in MAPS_DATA):
            raise ValueError(f"invalid map name: {map_name}")

        self.map_name = map_name
        self.map_data = MAPS_DATA[map_name]

        tileset_img = load_asset("tileset")
        tileset = split_tileset(tileset_img, Config.TILE_WIDTH, Config.TILE_HEIGHT)
        map_data = load_map(map_name)
        
        self.map = GameMap(tileset, map_data)
        self.game_surface = pygame.Surface(self.map.image.size)
        self.game_surface_rect = self.game_surface.get_frect()
        self.scaled_game_surface_size = (
            self.game_surface_rect.width * Config.MAP_SCALE_FACTOR,
            self.game_surface_rect.height * Config.MAP_SCALE_FACTOR,
        )

        self.camera = Camera(
            *self.game.screen.size,
            *self.game_surface_rect.size,
            Config.MAP_SCALE_FACTOR,
        )

        self.enemies_group = pygame.sprite.Group()
        self.towers_group = pygame.sprite.Group()
        self.projectiles_group = pygame.sprite.Group()
        self.explosions_group = pygame.sprite.Group()

        self.paused = False
        self.draw_tower_radiuses = False

        self.original_coins = self.map_data.initial_coins
        self.coins = self.original_coins
        self.shards_reward = self.map_data.shards_reward

        self.tower_to_place: TowerType | None = None
        self.can_place_tower = False
        self.selected_tower: TowerType | None = None

        self.waves = self.map_data.waves
        # -1 so that when the player starts the first wave it'll go to index 0
        self.wave = -1
        self.wave_state = WaveState.CLEARING

        self.wave_enemy_spawn_index = 0
        self.enemy_spawn_interval = 1
        self.enemy_spawn_interval_dt_count = 0

        self.max_health = self.map_data.health
        self.health = self.max_health

        self.enemies_killed = 0

        self.game_speed_multiplier = 1.0

        self.music_playlist = self.map_data.music
        random.shuffle(self.music_playlist)

        self.music_index = 0
        self.music_channel = pygame.mixer.find_channel()
        self.play_next_music()

        self.gui_manager = MainGameSceneGUIManager(self)

    def on_exit(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def play_next_music(self):
        current_music = self.music_playlist[self.music_index]
        pygame.mixer.music.load(get_sound(current_music))
        pygame.mixer.music.play(fade_ms=Config.DEFAULT_SOUND_FADEIN_MS)

        to_queue = self.music_playlist[
            (self.music_index + 1) % len(self.music_playlist)
        ]
        pygame.mixer.music.queue(get_sound(to_queue))

        logger.info(f"playing music: current={current_music}, queued={to_queue}")

    def place_selected_tower(self) -> None:
        self.towers_group.add(self.tower_to_place)
        self.gui_manager.switch_state(UIStates.TOWER_PICKER_MENU)

        cost = self.tower_to_place.cost[self.tower_to_place.upgrade_index]  # ty:ignore[unresolved-attribute]

        self.coins -= cost

        logger.info(
            f"tower placed: type={type(self.tower_to_place)}, "
            f"cost={cost}, new coins={self.coins}"
        )

        # reset everything
        self.can_place_tower = False
        self.tower_to_place = None
        self.gui_manager.switch_state(UIStates.COLLAPSED)
        self.gui_manager.refresh()

    def sell_selected_tower(self) -> None:
        if self.selected_tower:
            tower_cost = self.selected_tower.cost[self.selected_tower.upgrade_index]
            refund = round(tower_cost * 0.75)
            self.coins += refund

            # TODO: FINISH THIS LOG
            logger.info(
                f"tower sold: type={type(self.selected_tower)}, "
                f"upgrade index={self.selected_tower.upgrade_index}, "
                f"current cost={tower_cost}, "
                f"new coins={self.coins}"
            )

            self.selected_tower.kill()
            self.selected_tower = None

    def next_wave(self) -> None:
        self.wave += 1
        self.wave_enemy_spawn_index = 0
        self.enemy_spawn_interval_dt_count = 0

        self.wave_state = WaveState.SPAWNING

        self.gui_manager.update_wave_text()

        logger.info(f"new wave: wave={self.wave}, enemies={self.waves[self.wave]}")

    def update(self, delta_time: float) -> None:
        if not self.paused:
            if self.wave_state == WaveState.SPAWNING:
                self.enemy_spawn_interval_dt_count += delta_time

                if (
                    self.wave != -1
                    and self.enemy_spawn_interval_dt_count >= self.enemy_spawn_interval
                    and self.wave_enemy_spawn_index < len(self.waves[self.wave])
                ):
                    enemy_id = self.waves[self.wave][self.wave_enemy_spawn_index]
                    enemy = ENEMIES[enemy_id](self.map.path)
                    self.enemies_group.add(enemy)
                    self.wave_enemy_spawn_index += 1
                    self.enemy_spawn_interval_dt_count = 0

                if self.wave_enemy_spawn_index >= len(self.waves[self.wave]):
                    self.wave_state = WaveState.CLEARING

            # gui wave count is 1 higher, eg. when it says wave 5 it's actually
            # index 4, so len(self.waves) must be decreased by 1
            if (
                self.wave > -1
                and self.wave_state == WaveState.CLEARING
                and len(self.enemies_group) <= 0
                and self.wave >= len(self.waves) - 1
            ):
                logger.info(
                    "game won: "
                    f"map={self.map_name}"
                    f"shards reward={self.shards_reward}, "
                    f"final coins={self.coins}, "
                    f"final health={self.health}/{self.max_health}, "
                    f"towers placed={len(self.towers_group)}"
                )
                self.game.scene_manager.push(
                    GameWonScene(self.game, self.shards_reward), do_exit=True
                )
                self.game.player_save.shards += self.shards_reward
                self.game.player_save.beat_map(self.map_name)

            if self.health <= 0:
                reward = self.shards_reward // 2
                logger.info(
                    "game lost: "
                    f"map={self.map_name}"
                    f"shards reward={reward}, "
                    f"final coins={self.coins}, "
                    f"final health={self.health}/{self.max_health}, "
                    f"wave={self.wave + 1}/{len(self.waves)}, "
                    f"enemies killed={self.enemies_killed}, "
                    f"enemies remaining in wave={len(self.enemies_group)}, "
                    f"towers placed={len(self.towers_group)}"
                )
                self.game.scene_manager.push(
                    GameLostScene(self.game, reward), do_exit=True
                )
                self.game.player_save.shards += reward

            self.enemies_group.update(delta_time, self.game_speed_multiplier)
            self.towers_group.update(
                delta_time,
                self.enemies_group,
                self.projectiles_group,
                self.game_speed_multiplier,
            )
            self.explosions_group.update(
                delta_time, self.enemies_group, self.game_speed_multiplier
            )
            self.projectiles_group.update(
                delta_time,
                self.enemies_group,
                self.explosions_group,
                self.game_speed_multiplier,
            )

            self.gui_manager.update_elements(delta_time, pygame.mouse.get_pos())

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_world_coord = self.camera.viewport_to_world(mouse_x, mouse_y)

            ## camera movement
            if not any(
                element.rect.collidepoint(mouse_x, mouse_y)
                for element in self.gui_manager.elements
            ):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        if self.tower_to_place and self.can_place_tower:
                            self.place_selected_tower()
                        else:
                            for tower in self.towers_group:
                                if tower.rect.collidepoint(mouse_world_coord):
                                    self.selected_tower = tower
                                    self.gui_manager.switch_state(
                                        UIStates.TOWER_SELECTED
                                    )
                elif event.type == pygame.MOUSEMOTION:
                    if event.buttons[2]:  # right click
                        # event.rel is the amount of mouse movement
                        mouse_movement = (
                            pygame.Vector2(event.rel) / Config.MAP_SCALE_FACTOR
                        )

                        self.camera.move(int(mouse_movement.x), int(mouse_movement.y))

                    # tower must be moved alongside the map
                    if self.tower_to_place:
                        new_coord = pygame.Vector2(mouse_world_coord)
                        self.tower_to_place.move_center(*new_coord)
                        self.can_place_tower = not pygame.sprite.spritecollide(
                            self.tower_to_place, self.map.blocked_tiles, False
                        ) and not pygame.sprite.spritecollide(
                            self.tower_to_place, self.towers_group, False
                        )

            if event.type == ENEMY_KILLED:
                self.enemies_killed += 1

                logger.debug(
                    f"ENEMY_KILLED event received: type={type(event.entity)}, "
                    f"coins={event.entity.coins_drop}, count={self.enemies_killed}"
                )

                self.coins += event.entity.coins_drop
                self.gui_manager.update_coins_text()
                self.gui_manager.update_coin_dependent_ui()

            if event.type == DEFENSE_BREACHED:
                logger.debug(
                    f"DEFENSE_BREACHED event received: type={type(event.entity)}, "
                    f"health={event.entity.health}, base health={self.health}"
                )

                self.health -= event.entity.health
                self.gui_manager.update_health_text()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                    self.game.scene_manager.push(PauseMenuScene(self.game))
                    pygame.mixer.music.pause()
                elif event.key == pygame.K_r:
                    self.draw_tower_radiuses = not self.draw_tower_radiuses

            if event.type == pygame.mixer.music.get_endevent():
                self.play_next_music()

            self.gui_manager.handle_event(event)

    def render(self, surface: pygame.Surface) -> None:
        self.map.draw(self.game_surface)

        # pygame.sprite.Group.draw() only blits the sprite image,
        # but the enemies have a health bar that is drawn in their .draw()
        # method, so I call it normally (the draw function does little more)
        # than that
        for enemy in self.enemies_group:
            enemy.draw(self.game_surface)

        for tower in self.towers_group:
            tower.draw(self.game_surface, self.draw_tower_radiuses)

        for projectile in self.projectiles_group:
            projectile.draw(self.game_surface)

        for explosion in self.explosions_group:
            explosion.draw(self.game_surface)

        if self.tower_to_place:
            overlay_color = (
                (0, 255, 0, 255) if self.can_place_tower else (255, 0, 0, 255)
            )
            self.tower_to_place.draw(
                self.game_surface, True, overlay_color=overlay_color
            )

        scaled_game_surface = pygame.transform.scale(
            self.game_surface, self.scaled_game_surface_size
        )

        camera_view = pygame.Rect(
            self.camera.offset.x * Config.MAP_SCALE_FACTOR,
            self.camera.offset.y * Config.MAP_SCALE_FACTOR,
            self.game.screen.width,
            self.game.screen.height,
        )
        surface.blit(scaled_game_surface, (0, 0), camera_view)

        self.gui_manager.render_elements(surface)

    def restart(self) -> None:
        self.enemies_group.empty()
        self.towers_group.empty()
        self.projectiles_group.empty()
        self.explosions_group.empty()

        self.tower_to_place = None
        self.can_place_tower = False
        self.selected_tower = None

        self.wave = -1
        self.wave_state = WaveState.CLEARING

        self.wave_enemy_spawn_index = 0
        self.enemy_spawn_interval = 1
        self.enemy_spawn_interval_dt_count = 0

        self.health = self.max_health

        self.coins = self.original_coins

        self.gui_manager.refresh()

        logger.info("game restarted")
