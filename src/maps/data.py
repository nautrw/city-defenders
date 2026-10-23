from dataclasses import dataclass

ALL_MAP_MUSIC = ["Heroic Demise", "Soliloquy", "The Fall of Arcana"]


@dataclass
class MapData:
    display_name: str
    waves: list[tuple[str, ...]]
    initial_coins: int
    shards_reward: int
    health: int
    music: list[str]
    ground_on_top: bool = False


MAPS_DATA = {
    "magic_forest": MapData(
        display_name="Magic Forest",
        waves=[
            ("slime", "slime", ),
            ("slime", "slime", "slime", "slime"),
            ("slime", "fast_slime", "ghost"),
            ("fast_slime", "ghost", "slime", "ghost"),
            ("slime", "fast_slime", "fast_slime", "ghost", "crab"),
            ("fast_slime", "fast_slime", "ghost", "crab", "crab", "phantom"),
            ("slime", "fast_slime", "ghost", "crab", "crab", "phantom", "tank_slime"),
            ("fast_slime", "fast_slime", "ghost", "ghost", "crab", "tank_slime", "phantom"),
            (
                "fast_slime", "fast_slime", "ghost", "ghost",
                "crab", "crab", "tank_slime", "phantom", "armored_crab",
            ),
        ],
        initial_coins=200,
        shards_reward=75,
        health=25,
        music=ALL_MAP_MUSIC,
    ),

    "frontier": MapData(
        display_name="Frontier",
        waves=[
            ("slime", "slime", "fast_slime", "ghost"),
            ("slime", "fast_slime", "fast_slime", "ghost", "crab"),
            ("fast_slime", "fast_slime", "ghost", "ghost", "crab", "slime"),
            ("fast_slime", "fast_slime", "ghost", "crab", "crab", "phantom"),
            ("fast_slime", "fast_slime", "ghost", "ghost", "crab", "crab", "phantom"),
            ("fast_slime", "ghost", "ghost", "crab", "crab", "tank_slime", "phantom"),
            (
                "fast_slime", "fast_slime", "ghost", "ghost",
                "crab", "crab", "tank_slime", "phantom",
            ),
            (
                "fast_slime", "fast_slime", "ghost", "phantom",
                "crab", "crab", "tank_slime", "tank_slime",
            ),
            (
                "fast_slime", "fast_slime", "ghost", "ghost",
                "crab", "phantom", "tank_slime", "armored_crab",
            ),
        ],
        initial_coins=250,
        shards_reward=150,
        health=30,
        music=ALL_MAP_MUSIC,
    ),

    "gate_to_the_volcano": MapData(
        display_name="Gate to the Volcano",
        waves=[
            ("slime", "fast_slime", "ghost"),
            ("slime", "fast_slime", "ghost", "crab", ),
            ("fast_slime", "fast_slime", "ghost", "crab", "crab" ),
            (
                "fast_slime", "fast_slime", "ghost", "ghost",
                "crab", "crab", "ghost", "ghost"
            ),
            (
                "fast_slime", "fast_slime", "fast_slime", "ghost",
                "ghost", "crab", "phantom", "phantom", "ghost",
            ),
            (
                "fast_slime", "fast_slime", "ghost", "ghost",
                "crab", "crab", "phantom",
            ),
            (
                "fast_slime", "fast_slime", "fast_slime", "ghost",
                "ghost", "crab", "crab", "phantom",
            ),
            (
                "fast_slime", "fast_slime", "ghost", "ghost",
                "ghost", "crab", "crab", "phantom",
                "tank_slime", "armored_crab",
            ),
            (
                "fast_slime", "fast_slime", "fast_slime", "ghost",
                "ghost", "crab", "crab", "phantom", "tank_slime",
                "armored_crab", "armored_crab",
            ),
            (
                "fast_slime", "fast_slime", "fast_slime", "ghost",
                "ghost", "ghost", "crab", "crab", "phantom",
                "phantom", "tank_slime", "tank_slime",
                "armored_crab", "armored_crab",
            ),
        ],
        initial_coins=310,
        shards_reward=240,
        health=40,
        music=ALL_MAP_MUSIC,
    ),

    "archipelago": MapData(
        display_name="Archipelago",
        waves=[
            ("slime", "slime", "fast_slime"),
            ("fast_slime", "fast_slime", "ghost", "ghost"),
            (
                "slime", "slime", "fast_slime", "ghost",
                "crab", "crab",
            ),
            (
                "slime", "slime", "fast_slime", "fast_slime",
                "ghost", "crab", "ghost"
            ),
            (
                "slime", "fast_slime", "ghost", "ghost",
                "crab", "crab", "phantom"
            ),
            (
                "fast_slime", "fast_slime", "fast_slime", "ghost",
                "ghost", "crab", "crab", "phantom", "tank_slime",
                "armored_crab",
            ),
            (
                "fast_slime", "fast_slime", "fast_slime", "ghost",
                "ghost", "crab", "crab", "phantom",
                "tank_slime", "armored_crab",
            ),
            (
                "fast_slime", "fast_slime", "fast_slime", "ghost",
                "ghost", "crab", "crab", "phantom", "phantom",
                "tank_slime", "tank_slime", "armored_crab",
            ),
            (
                "fast_slime", "fast_slime", "fast_slime", "ghost",
                "ghost", "ghost", "crab", "crab", "phantom",
                "phantom", "tank_slime", "armored_crab", "armored_crab",
            ),
            (
                "fast_slime", "fast_slime", "fast_slime", "fast_slime",
                "ghost", "ghost", "ghost", "crab", "crab",
                "phantom", "phantom", "tank_slime", "tank_slime",
                "armored_crab", "armored_crab",
            ),
        ],
        initial_coins=300,
        shards_reward=90,
        health=50,
        music=ALL_MAP_MUSIC,
        ground_on_top=True,
    ),
}


MAP_PROGRESSION = [
    "magic_forest",
    "frontier",
    "molten_lands",
    "archipelago",
]
