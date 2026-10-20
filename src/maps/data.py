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

MAPS_DATA = {
    "ground_zero": MapData(
        display_name="Ground Zero",
        waves=[
            ("slime", "slime"),
            ("slime", "ghost", "slime"),
            ("slime", "fast_slime", "ghost", "crab"),
            ("fast_slime", "fast_slime", "slime", "ghost", "crab"),
            ("slime", "slime", "fast_slime", "ghost", "crab", "bat"),
            ("fast_slime", "fast_slime", "ghost", "ghost", "crab", "bat"),
            ("slime", "fast_slime", "ghost", "crab", "crab", "bat", "bat"),
            ("fast_slime", "fast_slime", "ghost", "ghost", "crab", "bat", "tank_slime"),
            ("slime", "fast_slime", "fast_slime", "ghost", "ghost", "crab", "bat", "armored_crab"),
        ],
        initial_coins=260,
        shards_reward=100,
        health=25,
        music=ALL_MAP_MUSIC,
    ),
    "frontier": MapData(
        display_name="Frontier",
        waves=[
            ("slime", "slime", "ghost"),
            ("slime", "fast_slime", "ghost", "crab"),
            ("fast_slime", "fast_slime", "ghost", "crab", "bat"),
            ("slime", "fast_slime", "ghost", "ghost", "crab", "bat"),
            ("fast_slime", "fast_slime", "crab", "crab", "bat", "bat"),
            ("slime", "ghost", "ghost", "crab", "bat", "bat", "tank_slime"),
            ("fast_slime", "fast_slime", "ghost", "crab", "crab", "bat", "bat"),
            ("fast_slime", "ghost", "ghost", "crab", "crab", "bat", "tank_slime"),
            ("fast_slime", "fast_slime", "ghost", "ghost", "crab", "crab", "bat", "armored_crab"),
        ],
        initial_coins=300,
        shards_reward=100,
        health=25,
        music=ALL_MAP_MUSIC,
    ),
    "molten_lands": MapData(
        display_name="Molten Lands",
        waves=[
            ("slime", "fast_slime", "ghost", "crab"),
            ("fast_slime", "fast_slime", "ghost", "crab", "bat"),
            ("slime", "fast_slime", "ghost", "ghost", "crab", "bat", "lava_slime"),
            ("fast_slime", "fast_slime", "ghost", "crab", "crab", "bat", "lava_slime"),
            ("fast_slime", "fast_slime", "ghost", "ghost", "crab", "bat", "bat", "lava_slime"),
            ("fast_slime", "fast_slime", "fast_slime", "ghost", "ghost", "crab", "crab", "bat", "lava_slime"),
            ("fast_slime", "fast_slime", "ghost", "ghost", "crab", "crab", "bat", "lava_slime", "lava_slime"),
            ("fast_slime", "fast_slime", "ghost", "ghost", "crab", "crab", "bat", "bat", "lava_slime", "tank_slime"),
            ("fast_slime", "fast_slime", "ghost", "ghost", "ghost", "crab", "crab", "bat", "lava_slime", "lava_slime", "armored_crab"),
            ("fast_slime", "fast_slime", "fast_slime", "ghost", "ghost", "crab", "crab", "bat", "bat", "lava_slime", "lava_slime", "tank_slime", "armored_crab"),
        ],
        initial_coins=350,
        shards_reward=100,
        health=25,
        music=ALL_MAP_MUSIC,
    ),
}

MAP_PROGRESSION = ["ground_zero", "frontier", "molten_lands"]