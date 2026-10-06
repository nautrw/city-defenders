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
TOWERS = {
    "crossbow": {
        "class": CrossbowTower,
        "requires": None
    },
    "ballista": {
        "ballista": BallistaTower,
        "requires": "crossbow",
    },
    "cannon": {
        "class": CannonTower,
        "requires": "crossbow"
    },
    "frostspire": {
        "class": FrostspireTower,
        "requires": "cannon"
    },
    "venomshooter": {
        "class": VenomShooterTower,
        "requires": "frostspire"
    }
}
