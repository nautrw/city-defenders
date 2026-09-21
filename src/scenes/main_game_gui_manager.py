from enum import Enum, auto
from typing import TYPE_CHECKING

import pygame

import src.core.config as Config
from src.core.utils import (
    load_asset,
    load_button_state_triplet_assets,
    load_scaled_asset,
)
from src.entities.entity_data import TOWERS
from src.entities.towers.tower import Tower
from src.gui.button import CUSTOM_BUTTON_CLICKED, Button
from src.gui.container import ElementContainer
from src.gui.gui_manager import GUIManager
from src.gui.icon import Icon
from src.gui.placement_system import RectAnchorMode
from src.gui.text import Text

if TYPE_CHECKING:
    from src.scenes.main_game import MainGameScene


class UIStates(Enum):
    COLLAPSED = auto()
    TOWER_PICKER_MENU = auto()
    TOWER_PICKER_TOWER_SELECTED = auto()
    PLACING_TOWER = auto()
    TOWER_SELECTED = auto()


class MainGameSceneGUIManager(GUIManager):
    def __init__(self, scene: "MainGameScene") -> None:
        default_state = UIStates.COLLAPSED

        super().__init__(scene, default_state)

        self.selected_tower_to_buy: type[Tower] | None = None

        self.scene: MainGameScene

        self.refresh()

    def update_wave_text(self) -> None:
        self.get_element_by_id("wave_text", Text).update_text(
            f"Wave {self.scene.wave + 1}/{len(self.scene.waves)}"
        )

    def update_coins_text(self) -> None:
        self.get_element_by_id("coins_text", Text).update_text(str(self.scene.coins))

    def update_health_text(self) -> None:
        self.get_element_by_id("health_text", Text).update_text(
            f"{self.scene.health}/{self.scene.max_health}",
        )

    def update_next_wave_button(self) -> None:
        self.get_element_by_id("next_wave_button", Button).enabled = not (
            self.scene.wave + 1
        ) >= len(self.scene.waves)

    def update_game_speed_buttons(self) -> None:
        self.get_element_by_id("game_speed_half_button", Button).enabled = (
            self.scene.game_speed_multiplier != 0.5
        )
        self.get_element_by_id("game_speed_normal_button", Button).enabled = (
            self.scene.game_speed_multiplier != 1
        )
        self.get_element_by_id("game_speed_double_button", Button).enabled = (
            self.scene.game_speed_multiplier != 2
        )

    def _build_stats_displays(self) -> None:
        card_width = 192
        card_height = 80

        heart_icon = Icon(
            "heart_icon",
            Config.ELEMENT_OUTER_PADDING,
            card_height // 2,
            Config.GUI_MEDIUM_ICON_SIZE,
            Config.GUI_MEDIUM_ICON_SIZE,
            load_scaled_asset("health_icon", (Config.GUI_MEDIUM_ICON_SIZE, Config.GUI_MEDIUM_ICON_SIZE)),
            anchor=RectAnchorMode.MIDLEFT,
        )

        health_text = Text(
            "health_text",
            f"{self.scene.health}/{self.scene.max_health}",
            heart_icon.rect.right + Config.ELEMENT_OUTER_PADDING,
            card_height // 2,
            Config.FONT_SIZE_BIGGER,
            anchor=RectAnchorMode.MIDLEFT,
        )

        health_display_container = ElementContainer(
            "health_display_container",
            Config.ELEMENT_OUTER_PADDING,
            Config.ELEMENT_OUTER_PADDING,
            card_width,
            card_height,
        )

        health_display_container.add_element(heart_icon)
        health_display_container.add_element(health_text)
        self.elements.append(health_display_container)

        coin_icon = Icon(
            "coin_icon",
            Config.ELEMENT_OUTER_PADDING,
            card_height // 2,
            Config.GUI_MEDIUM_ICON_SIZE,
            Config.GUI_MEDIUM_ICON_SIZE,
            load_scaled_asset("coin", (Config.GUI_MEDIUM_ICON_SIZE, Config.GUI_MEDIUM_ICON_SIZE)),
            RectAnchorMode.MIDLEFT,
        )

        coins_text = Text(
            "coins_text",
            str(self.scene.coins),
            coin_icon.rect.right + Config.ELEMENT_OUTER_PADDING,
            card_height // 2,
            Config.FONT_SIZE_BIGGER,
            anchor=RectAnchorMode.MIDLEFT,
        )

        coin_display_container = ElementContainer(
            "coin_display_container",
            Config.ELEMENT_OUTER_PADDING,
            health_display_container.rect.bottom + Config.ELEMENT_OUTER_PADDING,
            card_width,
            card_height,
        )

        coin_display_container.add_element(coin_icon)
        coin_display_container.add_element(coins_text)

        self.elements.append(coin_display_container)

        wave_display_container = ElementContainer(
            "wave_display_container",
            Config.ELEMENT_OUTER_PADDING,
            coin_display_container.rect.bottom + Config.ELEMENT_OUTER_PADDING,
            card_width,
            card_height,
        )

        wave_text = Text(
            "wave_text",
            f"Wave {self.scene.wave + 1}/{len(self.scene.waves)}"
            if self.scene.wave != -1
            else "Press Start",
            Config.ELEMENT_OUTER_PADDING,
            wave_display_container.rect.height / 2,
            anchor=RectAnchorMode.MIDLEFT,
        )

        wave_display_container.add_element(wave_text)

        self.elements.append(wave_display_container)


    def _build_game_speed_controller(self) -> None:
        game_speed_button_width = 72
        game_speed_button_height = 32

        game_speed_buttons_container = ElementContainer(
            "game_speed_buttons_container",
            Config.ELEMENT_OUTER_PADDING,
            Config.SCREEN_HEIGHT - Config.ELEMENT_OUTER_PADDING,
            (game_speed_button_width * 3) + (Config.ELEMENT_OUTER_PADDING * 4),
            game_speed_button_height + (Config.ELEMENT_OUTER_PADDING * 2),
            anchor=RectAnchorMode.BOTTOMLEFT,
        )

        game_speed_half_button = Button(
            "game_speed_half_button",
            Config.ELEMENT_OUTER_PADDING,
            game_speed_buttons_container.rect.height - Config.ELEMENT_OUTER_PADDING,
            game_speed_button_width,
            game_speed_button_height,
            text=Text(
                "game_speed_half_text",
                "1/2x",
                game_speed_button_width / 2,
                game_speed_button_height / 2,
                anchor=RectAnchorMode.CENTER,
            ),
            anchor=RectAnchorMode.BOTTOMLEFT,
            enabled=self.scene.game_speed_multiplier != 0.5,
        )

        game_speed_normal_button = Button(
            "game_speed_normal_button",
            game_speed_half_button.rect.right + Config.ELEMENT_OUTER_PADDING,
            game_speed_buttons_container.rect.height - Config.ELEMENT_OUTER_PADDING,
            game_speed_button_width,
            game_speed_button_height,
            text=Text(
                "game_speed_normal_text",
                "1x",
                game_speed_button_width / 2,
                game_speed_button_height / 2,
                anchor=RectAnchorMode.CENTER,
            ),
            anchor=RectAnchorMode.BOTTOMLEFT,
            enabled=self.scene.game_speed_multiplier != 1,
        )

        game_speed_double_button = Button(
            "game_speed_double_button",
            game_speed_normal_button.rect.right + Config.ELEMENT_OUTER_PADDING,
            game_speed_buttons_container.rect.height - Config.ELEMENT_OUTER_PADDING,
            game_speed_button_width,
            game_speed_button_height,
            text=Text(
                "game_speed_double_text",
                "2x",
                game_speed_button_width / 2,
                game_speed_button_height / 2,
                anchor=RectAnchorMode.CENTER,
            ),
            anchor=RectAnchorMode.BOTTOMLEFT,
            enabled=self.scene.game_speed_multiplier != 2,
        )

        game_speed_buttons_container.add_element(game_speed_half_button)
        game_speed_buttons_container.add_element(game_speed_normal_button)
        game_speed_buttons_container.add_element(game_speed_double_button)

        self.elements.append(game_speed_buttons_container)


    def _build_collapsed_ui(self) -> None:
        build_icon = load_scaled_asset("build_icon")
        build_button = Button(
            "tower_picker_menu_button",
            (Config.SCREEN_WIDTH - Config.ELEMENT_OUTER_PADDING),
            Config.ELEMENT_OUTER_PADDING,
            Config.BUTTON_SIZE,
            Config.BUTTON_SIZE,
            normal_icon=build_icon,
            anchor=RectAnchorMode.TOPRIGHT,
        )

        next_wave_button = Button(
            "next_wave_button",
            (Config.SCREEN_WIDTH - Config.ELEMENT_OUTER_PADDING),
            (Config.SCREEN_HEIGHT - Config.ELEMENT_OUTER_PADDING),
            Config.BUTTON_SIZE * 2,
            Config.BUTTON_SIZE * 2,
            **load_button_state_triplet_assets(
                "next_wave", (Config.GUI_ICON_SIZE * 2, Config.GUI_ICON_SIZE * 2)
            ),
            anchor=RectAnchorMode.BOTTOMRIGHT,
            enabled=not (self.scene.wave + 1) >= len(self.scene.waves),
        )

        self.elements.append(build_button)
        self.elements.append(next_wave_button)
 
    def _build_tower_picker_menu(self) -> None:
        container_width = 500

        tower_picker_container = ElementContainer(
            "tower_picker_menu",
            (Config.SCREEN_WIDTH - container_width),
            0,
            container_width,
            Config.SCREEN_HEIGHT,
        )

        close_icon = load_scaled_asset("close_icon")

        tower_picker_close_button = Button(
            "tower_picker_close_button",
            ((Config.SCREEN_WIDTH - container_width) - Config.BUTTON_SIZE)
            - Config.ELEMENT_OUTER_PADDING,
            Config.ELEMENT_OUTER_PADDING,
            Config.BUTTON_SIZE,
            Config.BUTTON_SIZE,
            normal_icon=close_icon,
        )

        columns = max(
            1,
            int(
                (container_width + Config.ELEMENT_OUTER_PADDING)
                / (Config.BUTTON_SIZE + Config.ELEMENT_OUTER_PADDING)
            ),
        )

        for i, tower in enumerate(TOWERS):
            column = i % columns
            row = i // columns

            button_x = Config.ELEMENT_OUTER_PADDING + column * (
                Config.BUTTON_SIZE + Config.ELEMENT_OUTER_PADDING
            )
            button_y = Config.ELEMENT_OUTER_PADDING + row * (
                Config.BUTTON_SIZE + Config.ELEMENT_OUTER_PADDING
            )

            icon = load_asset(f"{tower}_0")
            element = Button(
                f"build_{tower}_tower_button",
                button_x,  # placeholders
                button_y,
                Config.BUTTON_SIZE,
                Config.BUTTON_SIZE,
                normal_icon=icon,
            )

            tower_picker_container.add_element(element)

        self.elements.append(tower_picker_close_button)
        self.elements.append(tower_picker_container)


    def refresh(self) -> None:
        self.elements = []

        self._build_stats_displays()
        self._build_game_speed_controller()

        if self.state == UIStates.COLLAPSED:
            self._build_collapsed_ui()
        elif self.state == UIStates.TOWER_PICKER_MENU:
            self._build_tower_picker_menu()
        elif self.state == UIStates.TOWER_PICKER_TOWER_SELECTED:
            container_width = 500

            container = ElementContainer(
                "tower_picker_tower_selected_menu",
                (Config.SCREEN_WIDTH - container_width),
                0,
                container_width,
                Config.SCREEN_HEIGHT,
            )

            close_icon = load_scaled_asset("close_icon")
            close_container_button = Button(
                "close_tower_picker_tower_selected_menu_button",
                ((Config.SCREEN_WIDTH - container_width) - Config.BUTTON_SIZE)
                - Config.ELEMENT_OUTER_PADDING,
                Config.ELEMENT_OUTER_PADDING,
                Config.BUTTON_SIZE,
                Config.BUTTON_SIZE,
                normal_icon=close_icon,
            )

            tower_name = Text(
                "selected_tower_display_name",
                self.selected_tower_to_buy.display_name,  # ty:ignore[unresolved-attribute]
                container_width // 2,
                Config.ELEMENT_OUTER_PADDING,
                anchor=RectAnchorMode.MIDTOP,
                size=Config.FONT_SIZE_HEADER,
            )

            tower_description = Text(
                "selected_tower_description",
                self.selected_tower_to_buy.description,  # ty:ignore[unresolved-attribute]
                Config.ELEMENT_OUTER_PADDING,
                Config.ELEMENT_OUTER_PADDING + tower_name.rect.height,
                wrap_length=container_width,
            )

            cost_text = Text(
                "cost_text",
                "Cost: ",
                Config.ELEMENT_OUTER_PADDING,
                tower_description.rect.bottom + Config.ELEMENT_OUTER_PADDING,
            )
            coin_img = load_scaled_asset("coin", (36, 36))
            coin_icon = Icon(
                "coin_icon",
                cost_text.rect.right,
                cost_text.rect.top,
                Config.FONT_SIZE_NORMAL,
                Config.FONT_SIZE_NORMAL,
                coin_img,
            )
            tower_cost = Text(
                "tower_cost",
                str(self.selected_tower_to_buy.initial_cost),  # ty:ignore[unresolved-attribute]
                coin_icon.rect.right + Config.ELEMENT_OUTER_PADDING,
                coin_icon.rect.top,
            )

            build_button = Button(
                "buy_selected_tower_button",
                container_width // 2,
                Config.SCREEN_HEIGHT * 0.75,
                208,
                104,
                anchor=RectAnchorMode.CENTER,
                text=Text(
                    "buy_text",
                    "Buy",
                    208 // 2,
                    104 // 2,
                    size=Config.FONT_SIZE_VERYBIG,
                    anchor=RectAnchorMode.CENTER,
                ),
                normal_bg=Config.GREEN_BUTTON_NORMAL_BG,
                hover_bg=Config.GREEN_BUTTON_HOVERED_BG,
                pressed_bg=Config.GREEN_BUTTON_PRESSED_BG,
                enabled=(self.scene.coins >= self.selected_tower_to_buy.initial_cost),  # ty:ignore[unresolved-attribute]
            )

            container.add_element(tower_name)
            container.add_element(tower_description)
            container.add_element(cost_text)
            container.add_element(coin_icon)
            container.add_element(tower_cost)
            container.add_element(build_button)

            self.elements.append(container)
            self.elements.append(close_container_button)
        elif self.state == UIStates.PLACING_TOWER:
            close_icon = load_scaled_asset("close_icon")
            tower_discard_button = Button(
                "tower_discard_button",
                (Config.SCREEN_WIDTH - Config.ELEMENT_OUTER_PADDING),
                Config.ELEMENT_OUTER_PADDING,
                Config.BUTTON_SIZE,
                Config.BUTTON_SIZE,
                normal_icon=close_icon,
                anchor=RectAnchorMode.TOPRIGHT,
            )

            self.elements.append(tower_discard_button)
        elif self.state == UIStates.TOWER_SELECTED:
            container_width = 500

            selected_tower_menu = ElementContainer(
                "selected_tower_menu",
                Config.SCREEN_WIDTH - container_width,
                0,
                container_width,
                Config.SCREEN_HEIGHT,
            )

            tower_name = Text(
                "selected_tower_display_name",
                self.scene.selected_tower.display_name,  # ty:ignore[unresolved-attribute]
                container_width // 2,
                Config.ELEMENT_OUTER_PADDING,
                anchor=RectAnchorMode.MIDTOP,
                size=Config.FONT_SIZE_HEADER,
            )

            tower_description = Text(
                "selected_tower_description",
                self.scene.selected_tower.description,  # ty:ignore[unresolved-attribute]
                Config.ELEMENT_OUTER_PADDING,
                Config.ELEMENT_OUTER_PADDING + tower_name.rect.height,
                wrap_length=container_width,
            )

            sell_button = Button(
                "sell_selected_tower_button",
                container_width // 2,
                Config.SCREEN_HEIGHT - Config.ELEMENT_OUTER_PADDING,
                208,
                104,
                anchor=RectAnchorMode.MIDBOTTOM,
                text=Text(
                    "sell_text",
                    "Sell",
                    208 // 2,
                    104 // 2,
                    size=Config.FONT_SIZE_VERYBIG,
                    anchor=RectAnchorMode.CENTER,
                ),
                normal_bg=Config.RED_BUTTON_NORMAL_BG,
                hover_bg=Config.RED_BUTTON_HOVERED_BG,
                pressed_bg=Config.RED_BUTTON_PRESSED_BG,
            )

            if (
                self.scene.selected_tower.upgrade_index  # ty:ignore[unresolved-attribute]
                < len(
                    self.scene.selected_tower.cost  # ty:ignore[unresolved-attribute]
                )
                - 1
                and self.scene.selected_tower
            ):
                selected_tower: Tower = self.scene.selected_tower

                attack_icon_surf = load_scaled_asset(
                    "attack_icon", (Config.GUI_MEDIUM_ICON_SIZE, Config.GUI_MEDIUM_ICON_SIZE)
                )
                attack_icon = Icon(
                    "attack_icon",
                    Config.ELEMENT_OUTER_PADDING,
                    tower_description.rect.bottom + Config.ELEMENT_OUTER_PADDING,
                    *attack_icon_surf.size,
                    image=attack_icon_surf,
                )

                attack_text = Text(
                    "selected_tower_attack_stat_upgrade_text",
                    f"{selected_tower.damage[selected_tower.upgrade_index]} -> {selected_tower.damage[selected_tower.upgrade_index + 1]}",
                    attack_icon.rect.right + Config.ELEMENT_OUTER_PADDING,
                    attack_icon.rect.centery,
                    anchor=RectAnchorMode.MIDLEFT,
                )

                attack_speed_icon_surf = load_scaled_asset(
                    "clock_icon", (Config.GUI_MEDIUM_ICON_SIZE, Config.GUI_MEDIUM_ICON_SIZE)
                )
                attack_speed_icon = Icon(
                    "attack_speed_icon",
                    Config.ELEMENT_OUTER_PADDING,
                    attack_icon.rect.bottom + Config.ELEMENT_OUTER_PADDING,
                    *attack_speed_icon_surf.size,
                    image=attack_speed_icon_surf,
                )
                attack_speed_text = Text(
                    "selected_tower_attack_speed_stat_text",
                    f"{selected_tower.shooting_speed[selected_tower.upgrade_index]} -> {selected_tower.shooting_speed[selected_tower.upgrade_index + 1]}",
                    attack_speed_icon.rect.right + Config.ELEMENT_OUTER_PADDING,
                    attack_speed_icon.rect.centery,
                    anchor=RectAnchorMode.MIDLEFT,
                )

                range_icon_surf = load_scaled_asset(
                    "range_icon", (Config.GUI_MEDIUM_ICON_SIZE, Config.GUI_MEDIUM_ICON_SIZE)
                )
                range_icon = Icon(
                    "range_icon",
                    Config.ELEMENT_OUTER_PADDING,
                    attack_speed_icon.rect.bottom + Config.ELEMENT_OUTER_PADDING,
                    *range_icon_surf.size,
                    image=range_icon_surf,
                )
                range_text = Text(
                    "selected_tower_range_stat_text",
                    f"{selected_tower.area_radius[selected_tower.upgrade_index]} -> {selected_tower.area_radius[selected_tower.upgrade_index + 1]}",
                    range_icon.rect.right + Config.ELEMENT_OUTER_PADDING,
                    range_icon.rect.centery,
                    anchor=RectAnchorMode.MIDLEFT,
                )

                upgrade_button = Button(
                    "upgrade_selected_tower_button",
                    container_width // 2,
                    sell_button.rect.top - Config.ELEMENT_OUTER_PADDING,
                    208,
                    104,
                    anchor=RectAnchorMode.MIDBOTTOM,
                    text=Text(
                        "upgrade_button_text",
                        "Upgrade",
                        208 // 2,
                        104 // 2,
                        size=Config.FONT_SIZE_BIGGER,
                        anchor=RectAnchorMode.CENTER,
                    ),
                    normal_bg=Config.GREEN_BUTTON_NORMAL_BG,
                    hover_bg=Config.GREEN_BUTTON_HOVERED_BG,
                    pressed_bg=Config.GREEN_BUTTON_PRESSED_BG,
                    enabled=self.scene.coins >= selected_tower.cost[selected_tower.upgrade_index]
                )

                selected_tower_menu.add_element(attack_icon)
                selected_tower_menu.add_element(attack_text)
                selected_tower_menu.add_element(attack_speed_icon)
                selected_tower_menu.add_element(attack_speed_text)
                selected_tower_menu.add_element(range_icon)
                selected_tower_menu.add_element(range_text)
                selected_tower_menu.add_element(upgrade_button)

            close_icon = load_scaled_asset("close_icon")
            close_selected_tower_menu_button = Button(
                "close_selected_tower_menu_button",
                (Config.SCREEN_WIDTH - container_width - Config.ELEMENT_OUTER_PADDING),
                Config.ELEMENT_OUTER_PADDING,
                Config.BUTTON_SIZE,
                Config.BUTTON_SIZE,
                normal_icon=close_icon,
                anchor=RectAnchorMode.TOPRIGHT,
            )

            selected_tower_menu.add_element(tower_name)
            selected_tower_menu.add_element(tower_description)
            selected_tower_menu.add_element(sell_button)

            self.elements.append(selected_tower_menu)
            self.elements.append(close_selected_tower_menu_button)

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == CUSTOM_BUTTON_CLICKED:
            if event.button.id == "tower_picker_menu_button":
                self.switch_state(UIStates.TOWER_PICKER_MENU)
            elif event.button.id == "tower_picker_close_button":
                self.switch_state(UIStates.COLLAPSED)
            elif (
                event.button.id.startswith("build_")
                and event.button.id.endswith("_tower_button")
                and event.button.id.split("_")[1] in TOWERS
            ):
                id = event.button.id.split("_")[1]
                self.selected_tower_to_buy = TOWERS[id]
                self.switch_state(UIStates.TOWER_PICKER_TOWER_SELECTED)
            elif event.button.id == "close_tower_picker_tower_selected_menu_button":
                self.selected_tower_to_buy = None
                self.switch_state(UIStates.TOWER_PICKER_MENU)
            elif event.button.id == "sell_selected_tower_button":
                self.scene.sell_selected_tower()
                self.switch_state(UIStates.COLLAPSED)
            elif event.button.id == "close_selected_tower_menu_button":
                self.switch_state(UIStates.COLLAPSED)
                self.scene.selected_tower = None
            elif event.button.id == "tower_discard_button":
                self.switch_state(UIStates.TOWER_PICKER_MENU)
                self.scene.tower_to_place = None
                self.scene.can_place_tower = False
            elif event.button.id == "buy_selected_tower_button":
                # here comes ty:ignore hell...
                if (
                    self.selected_tower_to_buy
                    and self.scene.coins >= self.selected_tower_to_buy.initial_cost  # ty:ignore[unresolved-attribute]
                ):
                    self.scene.tower_to_place = self.selected_tower_to_buy(  # ty:ignore[missing-argument]
                        *self.scene.camera.viewport_to_world(  # ty:ignore[invalid-argument-type]
                            *pygame.mouse.get_pos()
                        )
                    )

                    self.switch_state(UIStates.PLACING_TOWER)
            elif event.button.id == "next_wave_button":
                if not (self.scene.wave + 1) >= len(self.scene.waves):
                    self.scene.next_wave()
                    self.update_next_wave_button()
            elif event.button.id == "game_speed_half_button":
                self.scene.game_speed_multiplier = 0.5
                self.update_game_speed_buttons()
            elif event.button.id == "game_speed_normal_button":
                self.scene.game_speed_multiplier = 1
                self.update_game_speed_buttons()
            elif event.button.id == "game_speed_double_button":
                self.scene.game_speed_multiplier = 2
                self.update_game_speed_buttons()
            elif event.button.id == "upgrade_selected_tower_button" and self.scene.selected_tower:
                upgrade_cost = self.scene.selected_tower.cost[self.scene.selected_tower.upgrade_index]
                
                if self.scene.coins >= upgrade_cost:
                    self.scene.coins -= self.scene.selected_tower.cost[self.scene.selected_tower.upgrade_index]
                    self.scene.selected_tower.upgrade()
                    self.refresh()
