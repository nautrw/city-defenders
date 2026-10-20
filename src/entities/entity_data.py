from src.entities.towers.tower import Tower
from typing import TypedDict
from src.entities.enemies.armored_crab import ArmoredCrab
from src.entities.enemies.bat import Bat
from src.entities.enemies.crab import Crab
from src.entities.enemies.fast_slime import FastSlime
from src.entities.enemies.ghost import Ghost
from src.entities.enemies.lava_slime import LavaSlime
from src.entities.enemies.slime import Slime
from src.entities.enemies.tank_slime import TankSlime
from src.entities.towers.ballista import BallistaTower
from src.entities.towers.cannon import CannonTower
from src.entities.towers.crossbow import CrossbowTower
from src.entities.towers.frostspire import FrostspireTower
from src.entities.towers.venom_shooter import VenomShooterTower

ENEMIES = {
    "slime": Slime,
    "fast_slime": FastSlime,
    "tank_slime": TankSlime,
    "ghost": Ghost,
    "crab": Crab,
    "armored_crab": ArmoredCrab,
    "bat": Bat,
    "lava_slime": LavaSlime,
}

class TowersDict(TypedDict):
    type: type[Tower]
    requires: str | None

TOWERS: dict[str, TowersDict] = {
    "crossbow": { "type": CrossbowTower, "requires": None },
    "ballista": { "type": BallistaTower, "requires": "crossbow", },
    "cannon": { "type": CannonTower, "requires": "ballista", },
    "frostspire": {"type": FrostspireTower, "requires": "cannon" },
    "venomshooter": { "type": VenomShooterTower, "requires": "frostspire", },
}