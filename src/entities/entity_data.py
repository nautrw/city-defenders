from src.entities.enemies.fast_slime import FastSlime
from src.entities.enemies.slime import Slime
from src.entities.enemies.tank_slime import TankSlime
from src.entities.towers.ballista import BallistaTower
from src.entities.towers.cannon import CannonTower
from src.entities.towers.crossbow import CrossbowTower
from src.entities.towers.frostspire import FrostspireTower
from src.entities.towers.venom_shooter import VenomShooterTower

ENEMIES = {"slime": Slime, "fast_slime": FastSlime, "tank_slime": TankSlime}
TOWERS = {
    "crossbow": CrossbowTower,
    "ballista": BallistaTower,
    "cannon": CannonTower,
    "frostspire": FrostspireTower,
    "venomshooter": VenomShooterTower,
}
