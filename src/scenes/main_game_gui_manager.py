from enum import Enum, auto
from typing import TYPE_CHECKING

import pygame

import src.core.config as Config
from src.core.utils import load_asset, load_scaled_asset
from src.entities.entity_data import TURRETS
from src.entities.turrets.crossbow import CrossbowTurret
from src.entities.turrets.turret import Turret
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
    PLACING_TURRET = auto()
    TOWER_SELECTED = auto()


class MainGameSceneGUIManager(GUIManager):
    def __init__(self, scene: "MainGameScene") -> None:
        default_state = UIStates.COLLAPSED

        super().__init__(scene, default_state)

        self.selected_tower_to_buy: type[Turret] | None = None

        self.refresh()

    def update_wave_text(self):
        self.get_element_by_id("wave_text").update_text(  # ty:ignore[unresolved-attribute]
            f"Wave {self.scene.wave + 1}/{len(self.scene.waves)}"  # ty:ignore[unresolved-attribute]
        )

    def update_wave_time_left_text(self):
        self.get_element_by_id("time_left_text").update_text(  # ty:ignore[unresolved-attribute]
            f"{int(self.scene.waves_interval - self.scene.wave_interval_dt_count)}s left"  # ty:ignore[unresolved-attribute]
        )

    def update_coins_text(self):
        self.get_element_by_id("coins_text").update_text(  # ty:ignore[unresolved-attribute]
            str(self.scene.coins)  # ty:ignore[unresolved-attribute]
        )

    def update_health_text(self):
        self.get_element_by_id("health_text").update_text(  # ty:ignore[unresolved-attribute]
            f"{self.scene.health}/{self.scene.max_health}",  # ty:ignore[unresolved-attribute]
        )

    def refresh(self) -> None:
        self.elements = []

        # COINS DISPLAY ALWAYS SHOWN
        coin_icon_size = 48

        card_width = 192
        card_height = 80

        heart_icon = Icon(
            "heart_icon",
            Config.ELEMENT_OUTER_PADDING,
            card_height // 2,
            coin_icon_size,
            coin_icon_size,
            load_scaled_asset("health_icon", (coin_icon_size, coin_icon_size)),
            anchor=RectAnchorMode.MIDLEFT,
        )

        health_text = Text(
            "health_text",
            f"{self.scene.health}/{self.scene.max_health}",  # ty:ignore[unresolved-attribute]
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
            coin_icon_size,
            coin_icon_size,
            load_scaled_asset("coin", (coin_icon_size, coin_icon_size)),
            RectAnchorMode.MIDLEFT,
        )

        coins_text = Text(
            "coins_text",
            str(self.scene.coins),  # ty:ignore[unresolved-attribute]
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
            f"Wave {self.scene.wave + 1}/{len(self.scene.waves)}",  # ty:ignore[unresolved-attribute]
            Config.ELEMENT_OUTER_PADDING * 2,
            Config.ELEMENT_OUTER_PADDING,
        )

        time_left_text = Text(
            "time_left_text",
            f"{int(self.scene.waves_interval - self.scene.wave_interval_dt_count)}s left",  # ty:ignore[unresolved-attribute]
            Config.ELEMENT_OUTER_PADDING * 2,
            wave_text.rect.bottom - 5,
        )

        wave_display_container.add_element(wave_text)
        wave_display_container.add_element(time_left_text)

        self.elements.append(wave_display_container)

        if self.state == UIStates.COLLAPSED:
            build_icon = load_scaled_asset("build_icon")
            build_button = Button(
                "tower_picker_menu_button",
                (Config.SCREEN_WIDTH - Config.ELEMENT_OUTER_PADDING),
                Config.ELEMENT_OUTER_PADDING,
                Config.BUTTON_SIZE,
                Config.BUTTON_SIZE,
                icon=build_icon,
                anchor=RectAnchorMode.TOPRIGHT,
            )
            self.elements.append(build_button)
        elif self.state == UIStates.TOWER_PICKER_MENU:
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
                icon=close_icon,
            )

            columns = max(
                1,
                int(
                    (container_width + Config.ELEMENT_OUTER_PADDING)
                    / (Config.BUTTON_SIZE + Config.ELEMENT_OUTER_PADDING)
                ),
            )

            for i, tower in enumerate(TURRETS):
                column = i % columns
                row = i // columns

                button_x = Config.ELEMENT_OUTER_PADDING + column * (
                    Config.BUTTON_SIZE + Config.ELEMENT_OUTER_PADDING
                )
                button_y = Config.ELEMENT_OUTER_PADDING + row * (
                    Config.BUTTON_SIZE + Config.ELEMENT_OUTER_PADDING
                )

                icon = load_asset(tower)
                element = Button(
                    f"build_{tower}_turret_button",
                    button_x,  # placeholders
                    button_y,
                    Config.BUTTON_SIZE,
                    Config.BUTTON_SIZE,
                    icon=icon,
                )

                tower_picker_container.add_element(element)

            self.elements.append(tower_picker_close_button)
            self.elements.append(tower_picker_container)
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
                icon=close_icon,
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
                str(self.selected_tower_to_buy.cost),  # ty:ignore[unresolved-attribute]
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
                normal_bg=Config.BUY_BUTTON_NORMAL_BG,
                hover_bg=Config.BUY_BUTTON_HOVERED_BG,
                pressed_bg=Config.BUY_BUTTON_PRESSED_BG,
                enabled=(self.scene.coins >= self.selected_tower_to_buy.cost),  # ty:ignore[unresolved-attribute]
            )

            container.add_element(tower_name)
            container.add_element(tower_description)
            container.add_element(cost_text)
            container.add_element(coin_icon)
            container.add_element(tower_cost)
            container.add_element(build_button)

            self.elements.append(container)
            self.elements.append(close_container_button)
        elif self.state == UIStates.PLACING_TURRET:
            close_icon = load_scaled_asset("close_icon")
            tower_discard_button = Button(
                "tower_discard_button",
                (Config.SCREEN_WIDTH - Config.ELEMENT_OUTER_PADDING),
                Config.ELEMENT_OUTER_PADDING,
                Config.BUTTON_SIZE,
                Config.BUTTON_SIZE,
                icon=close_icon,
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
                Config.SCREEN_HEIGHT * 0.75,
                208,
                104,
                anchor=RectAnchorMode.CENTER,
                text=Text(
                    "sell_text",
                    "Sell",
                    208 // 2,
                    104 // 2,
                    size=Config.FONT_SIZE_VERYBIG,
                    anchor=RectAnchorMode.CENTER,
                ),
                normal_bg=Config.BUY_BUTTON_NORMAL_BG,
                hover_bg=Config.BUY_BUTTON_HOVERED_BG,
                pressed_bg=Config.BUY_BUTTON_PRESSED_BG,
            )

            close_icon = load_scaled_asset("close_icon")
            close_selected_tower_menu_button = Button(
                "close_selected_tower_menu_button",
                (Config.SCREEN_WIDTH - container_width - Config.ELEMENT_OUTER_PADDING),
                Config.ELEMENT_OUTER_PADDING,
                Config.BUTTON_SIZE,
                Config.BUTTON_SIZE,
                icon=close_icon,
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
                and event.button.id.endswith("_turret_button")
                and event.button.id.split("_")[1] in TURRETS
            ):
                id = event.button.id.split("_")[1]
                self.selected_tower_to_buy = TURRETS[id]
                self.switch_state(UIStates.TOWER_PICKER_TOWER_SELECTED)
            elif event.button.id == "close_tower_picker_tower_selected_menu_button":
                self.selected_tower_to_buy = None
                self.switch_state(UIStates.TOWER_PICKER_MENU)
            elif event.button.id == "sell_selected_tower_button":
                self.scene.sell_selected_tower()  # ty:ignore[unresolved-attribute]
                self.switch_state(UIStates.COLLAPSED)
            elif event.button.id == "close_selected_tower_menu_button":
                self.switch_state(UIStates.COLLAPSED)
                self.scene.selected_tower = None  # ty:ignore[unresolved-attribute]
            elif event.button.id == "tower_discard_button":
                self.switch_state(UIStates.TOWER_PICKER_MENU)
                self.scene.turret_to_place = None  # ty:ignore[unresolved-attribute]
                self.scene.can_place_turret = False  # ty:ignore[unresolved-attribute]
            elif event.button.id == "buy_selected_tower_button":  # noqa: SIM102
                # here comes ty:ignore hell...
                if self.selected_tower_to_buy:  # noqa: SIM102
                    if self.scene.coins >= self.selected_tower_to_buy.cost:  # ty:ignore[unresolved-attribute]
                        self.scene.turret_to_place = self.selected_tower_to_buy(  # ty:ignore[unresolved-attribute]
                            *self.scene.camera.viewport_to_world(  # ty:ignore[unresolved-attribute]
                                *pygame.mouse.get_pos()
                            )
                        )

                        self.switch_state(UIStates.PLACING_TURRET)
