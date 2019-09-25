"""
"""

import sys, pygame, time, os
from PIL import Image
import tile_viewer, interactive_objects, pw_utils, main_battle

res = {}
BLACK = 0, 0, 0
ANTI_ALIAS = True
SIZE = 720, 480
os.environ["SDL_VIDEO_CENTERED"] = "1" # Centres game window
screen = pygame.display.set_mode(SIZE)
SCALE = 3
TILE_DIM = 16 * SCALE
TILE_MOVEMENT = TILE_DIM // 2
A_BUTTON = pygame.K_a
B_BUTTON = pygame.K_s

def location(filename):
    #return "Resources\\Overworld\\" + filename
    return "Resources/Overworld/" + filename

def scale_image(scale, image):
    width, height = image.size
    image = image.resize((width * scale, height * scale))#, Image.ANTIALIAS)
    # including Image.ANTIALIAS makes a blurry scaled image

    return image

def load_image(name):
    image = Image.open(location(name + ".png"))
    image = scale_image(3, image)
    image_data = image.tobytes(), image.size, image.mode
    
    return pygame.image.fromstring(*image_data)

def load_character(character_name):
    pass

def load_resources():
    pygame.init()
    pygame.display.set_caption("Pokemon World")
    window_icon = pygame.image.load("Resources/pokemon world icon.png")
    pygame.display.set_icon(window_icon)
    #screen = pygame.display.set_mode(SIZE)

    #res["pallet town"] = pygame.image.load(location("pallet town.png"))
    res["current map name"] = "pallet town"
    image = Image.open(location("pallet town.png"))
    image = scale_image(3, image)
    image_data = image.tobytes(), image.size, image.mode
    res["pallet town"] = load_image("pallet town")
    res["map"] = res["pallet town"]
    res["map pos"] = [0, 0]
    mc = {}
    mc["down"], mc["up"], mc["left"], mc["right"] = [], [], [], []
    res["mc"] = mc
    for i in range(4):
        res["mc"]["down"].append(load_image("mc down " + str(i)))
        res["mc"]["up"].append(load_image("mc up " + str(i)))
        res["mc"]["left"].append(load_image("mc left " + str(i)))
        res["mc"]["right"].append(load_image("mc right " + str(i)))
    #res["mc pos"] = [SIZE[0] / 2 - 21, SIZE[1] / 2 - 28]
    #place_at(7, 5)
    res["mc tile"] = [SIZE[0] // 2 // TILE_DIM, SIZE[1] // 2 // TILE_DIM]
    place_at(*res["mc tile"])
    #place_at(3, 3)
    res["mc current"] = res["mc"]["down"]
    res["last direction"] = "down"
    res["current direction"] = "down"
    res["mc frame"] = 0
    tile_viewer.initialise(res["current map name"])
    rows, cols = tile_viewer.get_base(res["current map name"])
    res["tile states"] = tile_viewer.get_tile_states(rows, cols)
    res["text bar"] = pygame.image.load("Resources/text_bar.png")
    res["show text"] = False
    res["current button"] = "arrow"
    res["font"] = pygame.font.Font("Resources/Pokemon Fonts/pkmnrs.ttf", 30)
    res["current event"] = None
    res["interacting with"] = None
    
    get_NPC_list()

def get_NPC_list():
    # Open txt file in the current map's folder and read in
    # the list of NPCs on the current map, then use add_NPC
    # while looping through the list
    #pass
    res["NPCs"] = []

    # Testing with Prof. Oak:
    res["Oak"] = add_NPC("Oak", tile = (16, 14), pokemon = 25, can_battle = True)
    res["NPCs"].append(res["Oak"])

def add_NPC(name, tile, pokemon = None, can_battle = None):
    npc = interactive_objects.NPC(name, pokemon, can_battle)
    # Load NPC dialogue from txt file
    pw_utils.get_NPC_dialogue("base", npc)
    npc.at_tile = tile
    place_at(*tile, name = npc.name)
    
    return npc

def place_at(tile_row, tile_col, name = None):
    """
    Player/NPC sprite offset from the tile it's on:
    * Let tile top left be 0, 0
    * Offset = -1 * SCALE, -4 * SCALE
    """
    i, j = tile_row, tile_col
    tile_pos = i * TILE_DIM - res["map pos"][0], j * TILE_DIM - res["map pos"][1]
    offset = -1 * SCALE, -4 * SCALE

    if not name:
        res["mc pos"] = [tile_pos[0] + offset[0], tile_pos[1] + offset[1]]
    else:
        res[name + " pos"] = [tile_pos[0] + offset[0], tile_pos[1] + offset[1]]
        # add NPC to collection of NPCs on the current map

def move_sprite(direction):
    # Cannot move while reading text
    if res["show text"]: return "interact"
    
    if direction == "down":
        map_index = 1
        map_movement = -1
    elif direction == "up":
        map_index = 1
        map_movement = 1
    elif direction == "right":
        map_index = 0
        map_movement = -1
    elif direction == "left":
        map_index = 0
        map_movement = 1
    
    #res["moving"] = not(res["moving"])
    move_to_tile = res["mc tile"][:]
    current_tile = res["mc tile"][:]
    
    move_to_tile[map_index] -= map_movement
    y, x = current_tile
    j, i = move_to_tile

    """
    print("\nCurrent tile: {}\nMove to: {}".format((x, y), (i, j)))   
    print("Current tile state:", res["tile states"][x][y])
    print("Move to tile state:", res["tile states"][i][j])
    """

    tile_state = res["tile states"][move_to_tile[1]][move_to_tile[0]]
    # Check if any NPCs are at move_to_tile
    for npc in res["NPCs"]:
        if list(npc.at_tile) == move_to_tile:
            tile_state = 2
            res["interacting with"] = npc
            break
    
    if tile_state == 0 and res["current button"] == "arrow":
        res["interacting with"] = None
        #print("Currently at tile {}".format(res["mc tile"]))
        res["mc tile"][map_index] -= map_movement
        res["mc frame"] = (res["mc frame"] + 1) % len(res["mc current"])
        #res["map pos"][map_index] += map_movement * TILE_MOVEMENT
        sm = 10
        smooth_map_movement(map_index, map_movement, smoothness = sm)
        
        #if res["animate"]:
        #    update_screen()
        #    advance_frame()
        # Restrict frames
        #res["map pos"][map_index] += map_movement * TILE_MOVEMENT
        res["mc frame"] = (res["mc frame"] + 1) % len(res["mc current"])
        smooth_map_movement(map_index, map_movement, smoothness = sm)
        pygame.time.Clock().tick(30)
        
        
        return "default"
    elif tile_state == 1:
        res["interacting with"] = None
        return "collide"    
    elif tile_state == 2: return "interact"      

    #print(res["map pos"])

def smooth_map_movement(map_index, map_movement, smoothness = None):
    move = TILE_MOVEMENT
    if not smoothness: smoothness = 10
    increment = move // smoothness
    remainder = move % smoothness
    
    for i in range(1, smoothness + 1):
        res["map pos"][map_index] += map_movement * increment
        res["Oak pos"][map_index] += map_movement * increment
        update_screen()
        advance_frame()
    res["map pos"][map_index] += map_movement * remainder
    res["Oak pos"][map_index] += map_movement * remainder
   
    
def update_screen():
    screen.fill(BLACK)
    screen.blit(res["map"], res["map pos"])
            
    ### TEMP ###
    npc = res["Oak"]
    screen.blit(npc.sprites[npc.dir][npc.frame_num], res["Oak pos"])
    ### END OF TEMP ###
    
    if res["show text"]:
        #screen.blit(res["text bar"], (0, 338))
        display_speech_text()


    # Always have the mc on top of all other objects on the map
    screen.blit(res["mc current"][res["mc frame"]], res["mc pos"])
    
    if not res["animate"]:
        screen.fill(BLACK)

def advance_frame():
    #screen.blit(res["text bar"], (0, 0))
    pygame.display.flip()

def reposition(movement_sequence):
    directions = {
                    "u" : "up",
                    "d" : "down",
                    "l" : "left",
                    "r" : "right"
                    }
    
    for direction in movement_sequence:
            move_sprite(directions[direction])
            
    res["animate"] = True

def interact():
    """
    Interact by facing an interact tile and pressing A,
    display text on valid interaction
    """
    tile_state = move_sprite(res["current direction"])
    res["last direction"] = res["current direction"]
    if tile_state == "interact":
        obj = res["interacting with"]
        if obj:
            obj.turned_to_player = False
        display_speech_text(obj)

        ### BATTLE TESTING ###
        if obj:
            if obj.can_battle and obj.final_line:
                start_battle(my_pk = 158, opp_pk = obj.pokemon)
                obj.can_battle = False
                obj.next_message()

def display_speech_text(obj = None):
    """
    * Will display a pygame Surface containing the input text,
      allowing for scrolling/advancing through text with the A
      or B keys
    * The speech_surfaces output is a list containing all the
      speech boxes required to show all the text
    """
    if not obj:
        obj = res["interacting with"]
    screen.blit(res["text bar"], (0, 338))
    speech_surfaces = []
    text_position = (25, 398)
    
    if obj:
        inverted_directions = {
                            "U" : "D",
                            "L" : "R",
                            "D" : "U",
                            "R" : "L"
                            }
        for message in obj.messages:      
            for line in message:
                speech_surfaces.append(res["font"].render(line, True, BLACK))
            obj.message_surfaces.append(speech_surfaces)
            speech_surfaces = []

        try:
            screen.blit(obj.message_surfaces[obj.message_num][obj.line_num], \
                        text_position)
        except IndexError:
            print(obj.line_num, obj.message_num)
            print(obj.messages[0][obj.line_num])
        
        if not obj.turned_to_player:
            obj.dir = inverted_directions[res["current direction"][0].upper()]
            obj.turned_to_player = True
    else:
        text_surface = res["font"].render("Test text", True, BLACK)
        screen.blit(text_surface, text_position)
        
    res["show text"] = True

    return speech_surfaces

def start_battle(my_pk = None, opp_pk = None):
    main_battle.play(screen, my_pk, opp_pk)

def play():
    load_resources()
    res["animate"] = False
    reposition("lddd")

    while 1:
        for event in pygame.event.get():
            res["current event"] = event
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        #if button_press and event.key == pygame.K_DOWN:
        event = res["current event"]
        if not res["show text"]:
            if keys[pygame.K_DOWN]:
                res["current button"] = "arrow"
                direction = "down"
                res["last direction"] = res["current direction"]
                res["current direction"] = direction
                res["mc current"] = res["mc"][direction]
                move_sprite(direction)
            elif keys[pygame.K_LEFT]:
                res["current button"] = "arrow"
                direction = "left"
                res["last direction"] = res["current direction"]
                res["current direction"] = direction
                res["mc current"] = res["mc"][direction]
                move_sprite(direction)
            elif keys[pygame.K_RIGHT]:
                res["current button"] = "arrow"
                direction = "right"
                res["last direction"] = res["current direction"]
                res["current direction"] = direction
                res["mc current"] = res["mc"][direction]
                move_sprite(direction)
            elif keys[pygame.K_UP]:
                res["current button"] = "arrow"
                direction = "up"
                res["last direction"] = res["current direction"]
                res["current direction"] = direction
                res["mc current"] = res["mc"][direction]
                move_sprite(direction)
        if event and event.type == pygame.KEYUP and event.key == A_BUTTON:
            res["current button"] = "A"
            interact()
            obj = res["interacting with"]
            if obj:
                obj.update_line()
                if obj.line_num == obj.num_lines:
                    obj.reset_dialogue()
                    res["show text"] = False
                elif obj.line_num == obj.num_lines - 1:
                    obj.final_line = True
            event.key = None
        elif keys[B_BUTTON]:
            res["current button"] = "B"
            res["show text"] = False
            obj = res["interacting with"]
            if obj: obj.reset_dialogue()

        update_screen()
        advance_frame()
        
        # Restrict framerate
        #pygame.time.Clock().tick(60)

play()
    
