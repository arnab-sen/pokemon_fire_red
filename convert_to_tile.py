"""
This takes a PNG image as input, and for given tile dimensions, converts
that image into a series of tiles, and saves the tiles to a folder.
"""
import os
from PIL import Image
TILE_SIZE_ORIGINAL = (16, 16)
SCALE = 2
TILE_SIZE = (TILE_SIZE_ORIGINAL[0] * SCALE, TILE_SIZE_ORIGINAL[1] * SCALE)
TILE_DIM = TILE_SIZE[0]
TEST_OPEN_PATH = "Resources/Overworld/Tiles/Input/"
TEST_SAVE_PATH = "Resources/Overworld/Tiles/Saved/"
maps = {}

def scale_image(scale, image):
    width, height = image.size
    image = image.resize((width * scale, height * scale))

    return image

def get_map(filename):
    image = Image.open(TEST_OPEN_PATH + filename + ".png")
    maps["current"] = filename
    maps[filename] = {}
    image = scale_image(SCALE, image)
    maps[filename]["tiles per row"] = round(image.size[0] / TILE_SIZE[0])
    maps[filename]["tiles per col"] = round(image.size[1] / TILE_SIZE[1])
    maps[filename]["dimensions"] = image.size
    maps[filename]["image"] = image

    return image

def make_tiles(image):
    tiles = []
    tile_pos = [0, 0]
    current_map = maps["current"]
    crop_pos = [0, 0, *TILE_SIZE]
    for depth in range(maps[current_map]["tiles per col"]):
        crop_pos[1] = (TILE_DIM * depth)
        crop_pos[3] = crop_pos[1] + TILE_DIM
        for tile in range(maps[current_map]["tiles per row"]):
            crop_pos[0] = (TILE_DIM * tile)
            crop_pos[2] = crop_pos[0] + TILE_DIM
            tiles.append(image.crop(crop_pos))

    return tiles

def split_list(cols, linear_list):
    temp_list = []
    split_list = []
    for i in range(len(linear_list)):
        temp_list += [linear_list[i]]
        if (i + 1) % cols == 0:
            split_list += [temp_list]
            temp_list = []

    return split_list

def save_tiles(tiles):
    tiles_per_row = maps[maps["current"]]["tiles per row"]
    tiles = split_list(tiles_per_row, tiles)
    directory = TEST_SAVE_PATH + maps["current"]

    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save base image
    base = maps[maps["current"]]["image"]
    base.save(directory + "/" + maps["current"] + ".png")
    
    # Save tiles
    for i in range(len(tiles)):
        for j in range(tiles_per_row):
            name = directory + "/"
            name += maps["current"] + " [{}, {}].png".format(i, j)
            tiles[i][j].save(name)

def main():
    filename = "pallet town"
    image = get_map(filename)
    tiles = make_tiles(image)
    save_tiles(tiles)

if __name__ == "__main__":
    main()
    
