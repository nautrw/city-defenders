from pathlib import Path
import json
from dataclasses import dataclass, asdict, field
from platformdirs import PlatformDirs

dirs = PlatformDirs("CityDefenders", "nautrw", ensure_exists=True)
DATA_FILE = dirs.user_data_path / "save.json"

@dataclass
class PlayerSave:
    shards: int = 0

    # can't use [] as a default value because all instances would share the same
    # list; this likely won't be a problem for a player save but LSP will scream
    # at me
    unlocked_towers: list[str] = field(default_factory=list)
    beaten_maps: list[str] = field(default_factory=list)

def save_data_to_file(save: PlayerSave, path: Path=DATA_FILE) -> None:
    json_output = json.dumps(asdict(save))

    with open(path, 'w') as f:
        f.write(json_output)

def load_data_from_file(path: Path=DATA_FILE) -> PlayerSave:
    with open(path, 'r') as f:
        json_output = json.load(f)
        save = PlayerSave(**json_output)
    
    return save