from src.gui.container import ElementContainer
import src.core.config as Config
from src.gui.icon import Icon
from src.gui.text import Text
from src.gui.placement_system import RectAnchorMode
from src.core.utils import load_scaled_asset


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
        parent_id,
        x, y,
        card_width,
        card_height,
        anchor=anchor
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
