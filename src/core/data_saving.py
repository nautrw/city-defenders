import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path

from loguru import logger
from platformdirs import PlatformDirs

from src.entities.entity_data import TOWERS

dirs = PlatformDirs("CityDefenders", "nautrw", ensure_exists=True)
DATA_FILE = dirs.user_data_path / "save.json"
logger.info(f"Save data file: {DATA_FILE}")


@dataclass
class PlayerSave:
    shards: int = 0

    # can't use [] as a default value because all instances would share the same
    # list; this likely won't be a problem for a player save but LSP will scream
    # at me
    unlocked_towers: list[str] = field(default_factory=list)
    beaten_maps: list[str] = field(default_factory=list)

    def unlock_tower(self, tower_name: str) -> None:
        if not tower_name in TOWERS:
            raise ValueError(f"can not unlock invlaid tower: {tower_name}")

        if not tower_name in self.unlocked_towers:
            self.unlocked_towers.append(tower_name)


def ensure_data_file(path: Path = DATA_FILE) -> None:
    if not os.path.isfile(path):
        logger.info(f"data file does not exist at {path}, creating")

        with open(path, "w") as f:
            fresh_save = PlayerSave()
            json_output = json.dumps(asdict(fresh_save))
            f.write(json_output)


def save_data_to_file(save: PlayerSave, path: Path = DATA_FILE) -> None:
    ensure_data_file()

    json_output = json.dumps(asdict(save))

    with open(path, "w") as f:
        f.write(json_output)

    logger.success(f"Successfully wrote save file: {save}")


def load_data_from_file(path: Path = DATA_FILE) -> PlayerSave:
    ensure_data_file()

    with open(path, "r") as f:
        json_output = json.load(f)
        save = PlayerSave(**json_output)
        logger.success(f"Successfully loaded save file: {save}")

    return save


def reset_data(path: Path = DATA_FILE) -> None:
    if not os.path.isfile(path):
        ensure_data_file(path)
        return

    os.remove(path)
    fresh_save = PlayerSave()
    save_data_to_file(fresh_save)

    logger.info(f"reset data at path {path}")
