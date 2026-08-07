from dataclasses import dataclass

@dataclass(frozen=True)
class ShipType:
    id: str
    display_name: str
    description: str

    # Fielname (including extension) of the ship sprite, inside the
    # assets/ships directory
    sprite_name: str

    health: float = 100.0

    fire_rate_multiplier: float = 1.0
    projectile_damage_multiplier: float = 1.0
    movement_speed_multiplier: float = 1.0

    can_dash: bool = False
    dash_cooldown_secs: float = 10.0
    evade_change_percentage: float = 0.0

    guns_amount: int = 1
    # this should be changed and i'm just giving it a default value
    # so that it lets me group them
    gun_placements: list[tuple[int | float, int | float]] = [(0, 0)]

SHIPS: tuple[ShipType, ...] = (
    ShipType(
        id="corvette",
        display_name="Corvette Class",
        description="A very run-of-the-mill ship.",
        sprite_name="corvette-ship.png",
    ),
)
