"""
This takes an input folder of PNG tiles, displays them, and allows
the user to determine the status of each tile (can_collide, cannot_collide,
NPC, etc.) by clicking on it. Different colours surrounding the tiles
indicate different statuses.
"""
import pygame, sys, copy, os, ast
from PIL import Image
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
SIZE = 1000, 840
TILE_DIM_ORIGINAL = 16
SCALE = 2
TILE_DIM = TILE_DIM_ORIGINAL * SCALE
TILE_DIMENSIONS = TILE_DIM, TILE_DIM
GRID_SEP = 10
PATH = "Resources/Overworld/Tiles/Saved/"
map_info = {}

def scale_image(scale, image):
    width, height = image.size
    image = image.resize((width * scale, height * scale))

    return image

def get_base(filename):
    filename = PATH + "/" + filename + "/" + filename
    filename += ".png"
    image = Image.open(filename)
    image = scale_image(SCALE, image)
    row, col = round(image.size[0] / TILE_DIM), round(image.size[1] / TILE_DIM)

    return row, col  

def load_tiles(tiles_folder):
    tiles = []
    path = PATH + tiles_folder + "/"
    file_base = path + tiles_folder + " [{}, {}].png"
    tiles_per_row = map_info[tiles_folder][1]
    tiles_per_col = map_info[tiles_folder][2]
    #tiles = [[""] * tiles_per_row] * tiles_per_col
    tiles = [[""] * tiles_per_row for i in range(tiles_per_col)]

    for i in range(tiles_per_col):
        for j in range(tiles_per_row):
            tile = Image.open(file_base.format(i, j))
            position = (tile.size[0] * j + j * GRID_SEP,
                        tile.size[1] * i + i * GRID_SEP)
            tile = image_to_pygame(tile)
            tile_rect = pygame.Rect(*position, *TILE_DIMENSIONS)
            tiles[i][j] = [tile, position, tile_rect]
            #print(position, tiles[i][j][1])

    default_tile = Image.open("Resources/Overworld/Tiles/default.png")
    default_tile = scale_image(SCALE, default_tile)    
    map_info["default tile"] = default_tile
        
    collide_tile = Image.open("Resources/Overworld/Tiles/collide.png")
    collide_tile = scale_image(SCALE, collide_tile)    
    map_info["collide tile"] = collide_tile
    
    interact_tile = Image.open("Resources/Overworld/Tiles/interact.png")
    interact_tile = scale_image(SCALE, interact_tile)
    map_info["interact tile"] = interact_tile

    return tiles

def update_screen(tiles):
    #screen.blit(tiles[0][0]["image"], (0, GRID_SEP))
    #screen.blit(tiles[0][1]["image"], (TILE_DIM + GRID_SEP, GRID_SEP))

    rows, cols = map_info[map_info["current"]][1:]
    image_index = 0
    position_index = 1

    for i in range(cols):
        for j in range(rows):
            #print(tiles[i][j][position_index])
            #screen.blit(tiles[0][0][0], tiles[0][0][1])
            
            tile_pos = tiles[i][j][position_index]
            image = tiles[i][j][image_index]
            screen.blit(image, tile_pos)

def advance_frame():
    pygame.display.flip()

def image_to_pygame(image):
    image_data = image.tobytes(), image.size, image.mode

    return pygame.image.fromstring(*image_data)

def mouse_in_tile(mouse_position, tiles):
    rows, cols = map_info[map_info["current"]][1:]
    for i in range(cols):
        for j in range(rows):
            tile_rect = tiles[i][j][2]
            if tile_rect.collidepoint(mouse_position):
                return i, j

    return -1, -1

def show_tile_border(tiles, i, j, click):
    default = image_to_pygame(map_info["default tile"])
    collide = image_to_pygame(map_info["collide tile"])
    interact = image_to_pygame(map_info["interact tile"])
    
    tile_pos = tiles[i][j][1]
    tile_states = map_info["tile states"]
    if click:
        tile_states[i][j] = (tile_states[i][j] + 1) % 3
    highlight = [default, collide, interact][tile_states[i][j]]
    
    screen.blit(highlight, (tile_pos[0] - 3, tile_pos[1] - 3))

def get_tile_states(rows, cols):
    filename = map_info["current"]
    filename += "/" + filename + ".txt"
    if not os.path.isfile(PATH + filename):
        map_info["tile states"] = [[0] * rows for i in range(cols)]
    else:
        with open(PATH + filename) as file:
            states = ast.literal_eval(file.read())

    map_info["tile states"] = states
    
    return states

def save_tile_states():
    """
    Saves a 2D array of integers to a text file in the form:
    [
        [...],
        [...],
        [...]
    ]
    """

    tile_states = map_info["tile states"]
    tile_states_string = "["
    for row in tile_states:
        tile_states_string += "\n\t" + str(row) + ","
    tile_states_string = tile_states_string[:-1] # remove final comma
    tile_states_string += "\n]"

    filename = map_info["current"]
    filename += "/" + filename + ".txt"
    with open(PATH + filename, "w") as file:
        file.write(tile_states_string)

def initialise(tiles_folder):
    tiles_folder = "pallet town"
    map_info["current"] = tiles_folder
    
def play():
    #tiles_folder = input("Enter your tiles folder name: ")
    initialise("pallet town")
    tiles_folder = map_info["current"]
    
    rows, cols = tiles_per_row, tiles_per_col = get_base(tiles_folder)
    tile_info = [tiles_folder, tiles_per_row, tiles_per_col]
    map_info[tiles_folder] = tile_info
    tiles = load_tiles(tiles_folder)
    get_tile_states(tiles_per_row, tiles_per_col)
    
    screen.fill(WHITE)
    
    while 1:
        for i in range(cols):
            for j in range(rows):
                show_tile_border(tiles, i, j, click = False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                clicked_tile = mouse_in_tile(mouse_position, tiles)
                if clicked_tile[0] != -1:
                    print("Tile [{}, {}] selected!".format(clicked_tile[1],\
                                                           clicked_tile[0]))
                    show_tile_border(tiles, *clicked_tile, click = True)

        save_tile_states()
                
        update_screen(tiles)
        advance_frame()

if __name__ == "__main__":
    screen = pygame.display.set_mode(SIZE)
    play()
