import math
import json
from os import PathLike
from typing import LiteralString

import numpy as np
import pygame

import src.core.config as Config


def split_tileset(
    image: pygame.Surface, tile_width: int, tile_height: int
) -> dict[int, pygame.Surface]:
    image_dimensions = image.get_rect().size

    image_tiles_width = image_dimensions[0] // tile_width
    image_tiles_height = image_dimensions[1] // tile_height

    result = {}

    for tile_x in range(image_tiles_width):
        for tile_y in range(image_tiles_height):
            tile_i = tile_y * image_tiles_width + tile_x

            tile_rect_left = (tile_x * tile_width) % image_dimensions[0]
            tile_rect_top = (tile_y * tile_height) % image_dimensions[1]

            result[tile_i + 1] = image.subsurface(
                tile_rect_left, tile_rect_top, tile_width, tile_height
            )

    return result


def load_json_file(file: PathLike | LiteralString) -> dict:
    with open(file, "r") as f:
        return json.load(f)


def clean_map_json(map_json: dict) -> dict:
    map_width, map_height = map_json["width"], map_json["height"]
    result = {"width": map_width, "height": map_height, "layers": {}}

    for wanted_layer_name in (
        Config.TILES.ground_tiles_layer_name,
        Config.TILES.path_tiles_layer_name,
        Config.TILES.enemy_path_layer_name,
    ):
        new_layer = next(
            layer for layer in map_json["layers"] if layer["name"] == wanted_layer_name
        ).copy()

        if new_layer["type"] == "tilelayer":
            # tiled saves the normal tilemaps as 1d arrays so i reshape to make it into 2d

            # TILED USES 0 FOR EMPTY TILES; THE GENERATED MAP TILE IDS ARE NOT
            # 0 BASED
            new_layer["data"] = np.reshape(new_layer["data"], (map_height, map_width))
        elif new_layer["name"] == Config.TILES.enemy_path_layer_name:
            obj = new_layer["objects"][0]

            # the polyline is its own small surface in the tiled map editor
            # and points are saved relative to the surface instead of the whole
            # map surface; so i add the offset again so its relative to the
            # full map image
            x_offset, y_offset = int(obj["x"]), int(obj["y"])

            new_layer["data"] = [
                (point["x"] + x_offset, point["y"] + y_offset)
                for point in obj["polyline"]
            ]
            del new_layer["objects"]

        result["layers"][wanted_layer_name] = new_layer

    return result

def angle_to_point(origin: Coordinate, target: Coordinate):
    direction = pygame.Vector2(target) - pygame.Vector2(origin)
    return 360 - math.degrees(math.atan2(direction.x, -direction.y))
    # return (360 - (math.atan2(origin[1]-target[1],origin[0]-target[0]))) * (180 / math.pi)
