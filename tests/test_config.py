# For frozen dataclass testing:
# ty:ignore[invalid-assignment]

from xml.dom.minidom import Attr
from dataclasses import FrozenInstanceError
import pytest
from src.core.config import config as Config
from src.core.config import DisplayConfig


def test_attribute_errors():
    with pytest.raises(AttributeError):
        Config.this_will_never_be_a_key

    with pytest.raises(AttributeError):
        Config.ugnigenigmeigmeoigmeooka

    with pytest.raises(AttributeError):
        Config.oinmoimfo3nof3nfoi3nfo3j

    with pytest.raises(AttributeError):
        Config.this_neither_will_be_key

def test_display_config_frozen():
    display = DisplayConfig()

    with pytest.raises(FrozenInstanceError):
        display.FPS = 1993029902

    with pytest.raises(FrozenInstanceError):
        display.SCREEN_HEIGHT = 49939220

    with pytest.raises(FrozenInstanceError):
        display.SCREEN_WIDTH = 5992929
