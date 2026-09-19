from src.entities.enemies.fast_slime import FastSlime
from src.entities.enemies.slime import Slime
from src.entities.enemies.tank_slime import TankSlime
from src.entities.turrets.ballista import BallistaTurret
from src.entities.turrets.cannon import CannonTurret
from src.entities.turrets.crossbow import CrossbowTurret
from src.entities.turrets.frostspire import Frostspire

ENEMIES = {"slime": Slime, "fast_slime": FastSlime, "tank_slime": TankSlime}
TURRETS = {
    "crossbow": CrossbowTurret,
    "ballista": BallistaTurret,
    "cannon": CannonTurret,
    "frostspire": Frostspire,
}
