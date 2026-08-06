import pytest
from src.core.config import config as Config

def test_attribute_errors():
    with pytest.raises(AttributeError):
        Config.this_will_never_be_a_key
        Config.ugnigenigmeigmeoigmeooka
        Config.oinmoimfo3nof3nfoi3nfo3j
        Config.this_neither_will_be_key
