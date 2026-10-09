from pygame.typing import ColorLike

import src.core.config as Config
from src.core.utils import load_scaled_asset
from src.gui.button import Button
from src.gui.container import ElementContainer
from src.gui.icon import Icon
from src.gui.placement_system import RectAnchorMode
from src.gui.text import Text


def build_stat_display(
    parent_id: str,
    default_text: str,
    x: float,
    y: float,
    icon_name: str | None = None,
    text_size: int = Config.FONT_SIZE_MEDIUM,
    anchor: RectAnchorMode = RectAnchorMode.TOPLEFT,
    card_width: int = 192,
    card_height: int = 80,
) -> ElementContainer:
    container = ElementContainer(
        parent_id, x, y, card_width, card_height, anchor=anchor
    )

    if icon_name:
        icon = Icon(
            f"{parent_id}_icon",
            Config.ELEMENT_OUTER_PADDING,
            card_height // 2,
            load_scaled_asset(
                icon_name,
                (Config.GUI_MEDIUM_ICON_SIZE, Config.GUI_MEDIUM_ICON_SIZE),
            ),
            anchor=RectAnchorMode.MIDLEFT,
        )

        container.add_element(icon)
        text_x = icon.rect.right + Config.ELEMENT_OUTER_PADDING
    else:
        text_x = Config.ELEMENT_OUTER_PADDING

    text = Text(
        f"{parent_id}_text",
        default_text,
        text_x,
        card_height // 2,
        size=text_size,
        anchor=RectAnchorMode.MIDLEFT,
    )

    container.add_element(text)

    return container


def build_currency_button(
    parent_id: str,
    x: float,
    y: float,
    icon_name: str,
    default_text: str,
    width: int = 208,
    height: int = 104,
    icon_size: int = Config.GUI_MEDIUM_ICON_SIZE,
    anchor: RectAnchorMode = RectAnchorMode.CENTER,
    normal_bg: ColorLike | None = Config.BUTTON_NORMAL_BG,
    hover_bg: ColorLike | None = Config.BUTTON_HOVERED_BG,
    pressed_bg: ColorLike | None = Config.BUTTON_PRESSED_BG,
    enabled: bool = True,
) -> Button:
    button_icon = Icon(
        f"{parent_id}_icon",
        Config.ELEMENT_OUTER_PADDING,
        height / 2,
        load_scaled_asset(icon_name, (icon_size, icon_size)),
        anchor=RectAnchorMode.MIDLEFT,
    )

    button = Button(
        parent_id,
        x,
        y,
        width,
        height,
        anchor=anchor,
        text=Text(
            f"{parent_id}_text",
            default_text,
            button_icon.rect.right + Config.ELEMENT_OUTER_PADDING,
            height / 2,
            size=Config.FONT_SIZE_XXLARGE,
            anchor=RectAnchorMode.MIDLEFT,
            fg_color=Config.TEXT_COLOR_NORMAL if enabled else Config.RED,
        ),
        normal_icon=button_icon,
        normal_bg=normal_bg,
        hover_bg=hover_bg,
        pressed_bg=pressed_bg,
        enabled=enabled,
    )

    return button
