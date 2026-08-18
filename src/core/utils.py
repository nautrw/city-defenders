import pygame

# A coord type to not have to type it out
Coordinate = pygame.Vector2 | tuple[int | float, int | float]

def split_tileset(image: pygame.Surface, tile_width: int, tile_height: int) -> dict[int, pygame.Surface]:
    image_dimensions = image.get_rect().size

    image_tiles_width = image_dimensions[0] // tile_width
    image_tiles_height = image_dimensions[1] // tile_height

    result = {}

    for tile_x in range(image_tiles_width):
        for tile_y in range(image_tiles_height):
            tile_i = tile_y * image_tiles_width + tile_x

            tile_rect_left = (tile_x * tile_width) % image_dimensions[0]
            tile_rect_top = (tile_y * tile_height) % image_dimensions[1]

            result[tile_i + 1] = image.subsurface(tile_rect_left, tile_rect_top, tile_width, tile_height)

    return result
