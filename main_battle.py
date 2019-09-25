"""
    
"""

import sys, os, pygame, time, random
import battle, get_pokemon_info
from PIL import Image

def load_resources(screen = None, my_pk = None, opp_pk = None):
    """my_pk and opp_pk must be the national dex numbers
    of the pokemon"""
    
    # State machine functions
    res["show moves logic"] = show_moves_logic
    res["show moves display"] = show_moves_display
    res["first attack logic"] = attack_logic
    res["first attack display"] = attack_display
    res["second attack logic"] = attack_logic
    res["second attack display"] = attack_display
    res["game over logic"] = game_over_logic
    res["game over display"] = game_over_display
    
    res["font"] = pygame.font.Font("Resources\\Pokemon Fonts\\pkmnrs.ttf", 30)
    res["black"] = (0, 0, 0)
    res["red"] = (255, 0, 0)
    res["green"] = (0, 255, 0)
    res["yellow"] = (255, 255, 0)
    res["blue"] = (0, 0, 255)
    res["text colour"] = res["black"]
    res["anti alias"] = True
    res["size"] = 720, 480

    os.environ["SDL_VIDEO_CENTERED"] = "1" # Centres game window
    if screen:
        res["screen"] = screen
    else:
        res["screen"] = pygame.display.set_mode(res["size"])    
        
    number_of_pokemon = 2
    pokemon_numbers = get_random_pokemon(number_of_pokemon)
    
    if my_pk:
        my_pk = get_pokemon_info.pokemon_number(my_pk)
        pokemon_numbers[0] = my_pk
    if opp_pk:
        opp_pk = get_pokemon_info.pokemon_number(opp_pk)
        pokemon_numbers[1] = opp_pk
    
    pokemon_names = get_pokemon_names(pokemon_numbers)
    pokemon_1 = pokemon_numbers[0]
    pokemon_2 = pokemon_numbers[1]
    
    res["my moves"] = get_moves(pokemon_names[0])
    res["opp moves"] = get_moves(pokemon_names[1])
    res["all moves"] = get_pokemon_info.get_dict("all_moves.txt")
    res["physical moves"] = get_pokemon_info.get_dict("physical_moves.txt")
    res["special moves"] = get_pokemon_info.get_dict("special_moves.txt")
    res["other moves"] = get_pokemon_info.get_dict("other_moves.txt")
    res["pokemon"] = create_pokemon(pokemon_numbers, [res["my moves"], res["opp moves"]])
    p0 = res["pokemon"][0]
    p1 = res["pokemon"][1]
    
    # Original size: 96 x 96, scaled size = 288, 288
    f2 = pygame.image.load("Resources\\bw-001n\\" + pokemon_2 + ".png")
    pokemon_position = get_opponent_position(pokemon_2)
    res["positions"] = [(60, 150), pokemon_position]
    f2 = pygame.transform.scale(f2, (192, 192))
    f1 = pygame.image.load("Resources\\bwback-001n\\" + pokemon_1 + ".png")
    f1 = pygame.transform.scale(f1, (288, 288))
    res["opp pokemon sprite"] = f2
    res["my pokemon sprite"] = f1
    res["bg"] = pygame.image.load("Resources\\battle_screen_with_moves_blank.png")
    res["type icons"] = load_pokemon_type_icons()
    res["moves bar"] = pygame.image.load("Resources\\moves_bar.png")
    res["move selection"] = pygame.image.load("Resources\\move_selection.png")
    res["text bar"] = pygame.image.load("Resources\\text_bar.png")
    res["my hp bar"] = pygame.image.load("Resources\\hp_bar_01.png")
    res["opp hp bar"] = pygame.image.load("Resources\\hp_bar_02.png")
    res["my green hp"] = pygame.image.load("Resources\\hp_bars\\green.png")
    res["opp green hp"] = pygame.image.load("Resources\\hp_bars\\green.png")
    res["my yellow hp"] = pygame.image.load("Resources\\hp_bars\\yellow.png")
    res["opp yellow hp"] = pygame.image.load("Resources\\hp_bars\\yellow.png")
    res["my red hp"] = pygame.image.load("Resources\\hp_bars\\red.png")
    res["opp red hp"] = pygame.image.load("Resources\\hp_bars\\red.png")
    res["my empty hp"] = pygame.image.load("Resources\\hp_bars\\empty.png")
    res["opp empty hp"] = pygame.image.load("Resources\\hp_bars\\empty.png")
    res["hp bars pos"] = [(380, 225), (30, 43)]
    res["hp colour pos"] = [(res["hp bars pos"][1][0] + 95, res["hp bars pos"][1][0] + 61)]
    res["hp colour pos"] += [(res["hp bars pos"][1][0] + 459, res["hp bars pos"][1][0] + 242)]
    res["hp max colour width"] = 144
    res["hp widths"] = [144, 144]
    res["hp percent"] = [p0.stats["HP"] / p0.original_stats["HP"]]
    res["hp percent"] += [p1.stats["HP"] / p1.original_stats["HP"]]
    res["my hp bar status"] = {"colour" : "green", "width" : 144 * res["hp percent"][0]}
    res["opp hp bar status"] = {"colour" : "green", "width" : 144 * res["hp percent"][1]}
    res["hp bars"] = [{
                        "green" : res["my green hp"], "yellow" : res["my yellow hp"],
                        "red" : res["my red hp"], "empty" : res["my empty hp"]
                        }]
    res["hp bars"] += [{
                        "green" : res["opp green hp"], "yellow" : res["opp yellow hp"],
                        "red" : res["opp red hp"], "empty" : res["opp empty hp"]
                        }]
    
    res["prev hp"] = [p1.original_stats["HP"], p0.original_stats["HP"]]

    res["move surfaces"] = []
    for move in res["my moves"]:
        res["move surfaces"] += [get_move_surface(move, res["anti alias"], res["text colour"])]

    res["quadrants"] = initialise_display()
    res["move selection pos"] = []
    for quadrant in res["quadrants"]:
        res["move selection pos"] += [(quadrant[0] + 3, quadrant[1] + 3)]

    #res["battle music"] =
    load_sound("FRLG_Battle_01.mp3")

def get_random_pokemon(number_of_pokemon):
    # Returns a list of n random pokemon from
    # 001 - 649 (Bulbasaur to Genesect)    
    pokemon_numbers = []
    for i in range(number_of_pokemon):
        num = random.randrange(1, 650)
        num = get_pokemon_info.pokemon_number(num)
        pokemon_numbers += [num]

    return pokemon_numbers

def get_pokemon_names(pokemon_numbers):
    numbered_pokemon = get_pokemon_info.get_dict("numbered_pokemon.txt")
    names = []
    for num in pokemon_numbers:
        names += [numbered_pokemon[num]]

    return names

def get_moves(pokemon_name):
    moves = get_pokemon_info.get_random_moves(pokemon_name)
    return moves

def create_pokemon(pokemon_numbers, moves):
    pokemon = []
    numbered_pokemon = get_pokemon_info.get_dict("numbered_pokemon.txt")
    i = 0
    all_stats = get_pokemon_info.get_dict("pokemon_stats.txt")
    
    for num in pokemon_numbers:
        name = numbered_pokemon[get_pokemon_info.pokemon_number(num)]
        pokemon += [battle.Pokemon(name, moves[i], all_stats[name])]
        i += 1

    return pokemon

def split_list(cols, linear_list):
    temp_list = []
    split_list = []
    for i in range(len(linear_list)):
        temp_list += [linear_list[i]]
        if (i + 1) % cols == 0:
            split_list += [temp_list]
            temp_list = []

    return split_list

def get_opponent_position(opponent_number):
    # Find the bottom-most pixel in the middle column, and align
    # that with the center of the opponent stage
    image = Image.open("Resources\\bw-001n\\" + opponent_number + ".png")
    image = image.resize((192, 192), Image.ANTIALIAS)
    image = image.convert("RGBA")
    pixel_data = list(image.getdata())
    pixel_data = split_list(192, pixel_data)
    middle = 96
    stage_middle = (520, 195)
    
    for i in range(96, len(pixel_data)):
            if pixel_data[i][middle][3] != 0:
                    bottom = i
                    
    return (stage_middle[0] - middle, stage_middle[1] - bottom)

def load_pokemon_type_icons():
    type_icons = {}
    move_types = ["bug", "dark", "dragon", "electric", "fighting", "fire",
                  "flying", "ghost", "grass", "ground", "ice", "normal",
                  "other", "physical", "poison", "psychic", "rock",
                  "special", "steel", "water"]
    
    for i in move_types:
        icon = pygame.image.load("Resources\\Move Icons\\" + i + ".png")
        if i != "physical" and i != "special" and i != "other":
            icon = pygame.transform.scale(icon, (64, 32))
        else:
            icon = pygame.transform.scale(icon, (56, 28))
        type_icons[i] = icon
    return type_icons

def get_move_surface(move, anti_alias, text_colour):
    return res["font"].render(move, True, text_colour)

def initialise_display():
    moves_top_left = (18, 356)
    moves_center = (240, 410)
    quadrant_width = moves_center[0] - 18
    quadrant_height = moves_center[1] - 356
    quadrant_1 = pygame.Rect(18, 356, quadrant_width, quadrant_height)
    quadrant_2 = pygame.Rect(241, 356, quadrant_width, quadrant_height)
    quadrant_3 = pygame.Rect(18, 410, quadrant_width, quadrant_height)
    quadrant_4 = pygame.Rect(241, 410, quadrant_width, quadrant_height) 
    
    return [quadrant_1, quadrant_2, quadrant_3, quadrant_4]

def mouse_in_quadrant(mouse_position, move_quadrants):
    for i in range(4):
        if move_quadrants[i].collidepoint(mouse_position):
            return i
    return -1

def update_state_machine():
    """
    Game states:
    State progression via mouse click (or specifically, mouse up)
    show moves -> highlight move -> attack1 if able -> attack2 if able -> game over if able
    States to be worked on include healing pokemon/using item, show current party,
    switching pokemon out, running from battle
    Can call game state functions via the res dict, e.g.:
    res["game over"] = game_over
    res["game over"]()
    Check if HP == 0 for either pokemon and if so, return game over and the winner
    """
    current = res["game state"]
    if current == "start":
        next_state = "show moves"
    elif current == "show moves" and res["selected index"] == res["current quadrant"]:
        next_state = "first attack"
    elif current == "first attack":
        if res["fainted"]:
            next_state = "game over"
        else:
            next_state = "second attack"
    elif current == "second attack":
        if res["fainted"]:
            next_state = "game over"
        else:
            next_state = "show moves"
    else:
        next_state = current

    return next_state

def show_moves_logic():
    if res["current quadrant"] != -1:
        res["selected index"] = res["current quadrant"]
        res["current move"] = res["my moves"][res["selected index"]]

def show_moves_display():
    move_surfaces = res["move surfaces"]
    quadrants = res["quadrants"]
    screen = res["screen"]
    moves_bar = res["moves bar"]
    move_selection = res["move selection"]
    moves = res["my moves"]
    selected_index = res["selected index"]
    anti_alias = res["anti alias"]
    text_colour = res["text colour"]
    type_icons = res["type icons"]
    
    screen.blit(moves_bar, (0, 337))
    screen.blit(move_surfaces[0],(quadrants[0][0] + 30, quadrants[0][1] + 15))
    screen.blit(move_surfaces[1],(quadrants[1][0] + 10, quadrants[1][1] + 15))
    screen.blit(move_surfaces[2],(quadrants[2][0] + 30, quadrants[2][1] + 10))
    screen.blit(move_surfaces[3],(quadrants[3][0] + 10, quadrants[3][1] + 10))

    if res["selected index"] != -2:
        screen.blit(move_selection, res["move selection pos"][res["selected index"]])

        # Display move information
        highlighted_move = moves[selected_index]
        move_data = res["all moves"][highlighted_move]
        move_type = move_data[0]
        move_phys_spec = move_data[1]
        move_power = move_data[3]
        move_accuracy = move_data[4]
        move_text = ["Power: " + str(move_power)]
        #move_text += ["Type: " + move_type[0:4].upper() + "/" + move_phys_spec[0:3].upper()]
        move_text += ["Type: "]            
        move_text += ["Accuracy: " + str(move_accuracy) + "%"]
        right_box = [res["font"].render(move_text[0] , anti_alias, text_colour)]
        right_box += [res["font"].render(move_text[1] , anti_alias, text_colour)]
        right_box += [res["font"].render(move_text[2] , anti_alias, text_colour)]
        screen.blit(right_box[0],(505, 360))
        screen.blit(right_box[1],(505, 395))
        screen.blit(right_box[2],(505, 430))
        screen.blit(type_icons[move_type],(573, 392))
        screen.blit(type_icons[move_phys_spec],(641, 394))     

def get_opponent_move():
    return res["opp moves"][random.randrange(3)]

def show_attack(attacker, defender, current_move):
    a = attacker
    d = defender
    battle_over = False
    temp_HP = defender.stats["HP"]
    battle_text_message = []
    battle_text = []
            
    battle.attack(attacker, defender, current_move)
    
    if temp_HP != defender.stats["HP"]:
        battle_text_message += ["", attacker.name + " used " +\
                            current_move + "!", ""]
    else:
        battle_text_message = [""]
        battle_text_message += [attacker.name + " used " +\
                            current_move]
        battle_text_message[1] += "... but it had no effect!"
        battle_text_message += [""]
        
    #print(attacker.name + " used " + current_move + "!")
    #print(defender.name + "'s HP fell from " + \
    #      str(temp_HP) + \
    #      " to " + str(defender.stats["HP"]))
    #print()
    
    if attacker.stats["HP"] == 0:
        battle_text_message += [attacker.name + " fainted... " + defender.name + " wins!"]
        battle_over = True
        return battle_over, battle_text
    if defender.stats["HP"] == 0:
        battle_text_message += [defender.name + " fainted... " + attacker.name + " wins!"]
        battle_over = True

    for i in range(len(battle_text_message)):
        battle_text += [res["font"].render(battle_text_message[i] , True , (0, 0, 0))]

    return battle_over, battle_text

def attack_logic():
    if res["game state"] == "first attack":
        attacker = res["pokemon"][0]
        defender = res["pokemon"][1]
    elif res["game state"] == "second attack":
        res["current move"] = get_opponent_move()
        attacker = res["pokemon"][1]
        defender = res["pokemon"][0]
        
    res["fainted"], res["battle text"] = show_attack(attacker, defender, res["current move"])

def attack_display():
    screen = res["screen"]
    text_bar = res["text bar"]
    battle_text = res["battle text"]
    
    screen.blit(text_bar, (0, 337))
    #screen.blit(battle_text[0], (25, 360))
    screen.blit(battle_text[1], (25, 398))
    #screen.blit(battle_text[2], (25, 435))

def game_over_logic():
    res["game over"] = True

def game_over_display():
    screen = res["screen"]
    text_bar = res["text bar"]
    battle_text = res["battle text"]
    
    screen.blit(text_bar, (0, 337))
    screen.blit(battle_text[3], (25, 398))
    res["exit game"] = True

def update_hp_bars():
    # Change hp bars:
    #if p0.stats["HP"] * p1.stats["HP"] != 0:
    screen = res["screen"]
    p0 = res["pokemon"][0]
    p1 = res["pokemon"][1]
    p0_hp_bar = res["my hp bar status"]
    p1_hp_bar = res["opp hp bar status"]
    myfont = res["font"]
    hp_bars = res["hp bars"]
    hp_colour_pos = res["hp colour pos"]
    prev_hp = res["prev hp"]
    pokemon = res["pokemon"]
    anti_alias = res["anti alias"]
    text_colour = res["text colour"]
    
    hp_percent = [p0.stats["HP"] / p0.original_stats["HP"]]
    hp_percent += [p1.stats["HP"] / p1.original_stats["HP"]]
    if hp_percent[1] > 0.5:
        p0_hp_bar["colour"] = "green"
    elif hp_percent[1] > 0.2 :
        p0_hp_bar["colour"] = "yellow"
    elif hp_percent[1] <= 0.2:
        p0_hp_bar["colour"] = "red"
    elif hp_percent[1] == 0:
        p0_hp_bar["colour"] = "empty"
    if hp_percent[0] > 0.5:
        p1_hp_bar["colour"] = "green"
    elif hp_percent[0] > 0.2:
        p1_hp_bar["colour"] = "yellow"
    elif hp_percent[0] <= 0.2:
        p1_hp_bar["colour"] = "red"
    elif hp_percent[0] == 0:
        p1_hp_bar["colour"] = "empty"
    #print(hp_percent)
    new_widths = [144 * hp_percent[0], 144 * hp_percent[1]]
    #print(hp_percent[0], hp_widths[0])
    hp_1 = hp_bars[0][p0_hp_bar["colour"]]
    hp_2 = hp_bars[1][p1_hp_bar["colour"]]
    hp_1 = pygame.transform.scale(hp_1, (round(new_widths[1]), 6))              
    hp_2 = pygame.transform.scale(hp_2, (round(new_widths[0]), 6))
    hp_bars[0][p0_hp_bar["colour"]] = hp_1
    hp_bars[1][p1_hp_bar["colour"]] = hp_2

    # Green/red/yellow/empty hp:
    #screen.blit(red_hp, (hp_bars_pos[0][0] + 95, hp_bars_pos[0][0] + 61))
    screen.blit(hp_bars[0][p0_hp_bar["colour"]], hp_colour_pos[0])
    screen.blit(hp_bars[1][p1_hp_bar["colour"]], hp_colour_pos[1])
    hp_text_message = [str(prev_hp[1]) + "/" + \
                        str(pokemon[0].original_stats["HP"])]
    hp_text_message += [str(prev_hp[0]) + "/" + \
                        str(pokemon[1].original_stats["HP"])]
    res["prev hp"] = [pokemon[1].stats["HP"], pokemon[0].stats["HP"]]
    hp_text = [myfont.render(hp_text_message[0] , anti_alias, text_colour)]
    hp_text += [myfont.render(hp_text_message[1] , anti_alias, text_colour)]
    screen.blit(hp_text[1], (hp_colour_pos[0][0] + 80, hp_colour_pos[0][1] + 15))
    screen.blit(hp_text[0], (hp_colour_pos[1][0] + 80, hp_colour_pos[1][1] + 15))

def load_sound(filename):
    path = "Resources/Sounds/"
    if not pygame.mixer:
        return None
    else:
        return pygame.mixer.music.load(path + filename)

def update_screen():
    screen = res["screen"]
    f2 = res["opp pokemon sprite"]
    f1 = res["my pokemon sprite"]
    p0 = res["pokemon"][0]
    p1 = res["pokemon"][1]
    
    # Display background, pokemon, hp bars, and moves/battle text:
    screen.fill(res["black"])
    screen.blit(res["bg"], (0, 0))
    screen.blit(f1, res["positions"][0])
    screen.blit(f2, res["positions"][1])
    screen.blit(res["my hp bar"], res["hp bars pos"][0])
    screen.blit(res["opp hp bar"], res["hp bars pos"][1])

    # Display pokemon names above their respective HP bars
    p1_name_text = res["font"].render(p1.name, True, res["text colour"])
    p0_name_text = res["font"].render(p0.name, True, res["text colour"])
    name_text_pos = [(420, 236), (55, 54)]
    screen.blit(p1_name_text, name_text_pos[1])
    screen.blit(p0_name_text, name_text_pos[0])

    update_hp_bars()

def advance_frame():
    # update whole screen (use display.update(rectangle) to update
    # chosen rectangle portions of the screen to update
    pygame.display.flip()

def main(screen = None, my_pk = None, opp_pk = None):
    # res is a dict of all resource variables
    res["keep playing"] = True
    while res["keep playing"]:
        res["keep playing"] = False
        # Initialise
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        load_resources(screen, my_pk, opp_pk)
        
        p0 = res["pokemon"][0]
        p1 = res["pokemon"][1]
        #res["game state"] = "start"
        res["game state"] = "show moves"
        res["game over"] = False
        res["my turn"] = True
        res["exit game"] = False
        res["move selected"] = -1 # [-1, 0, 1] = [not selected, selected, confirmed]
        res["selected index"] = -2 # random value that isn't a possible index and not -1
        #res["battle music"].play()
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()

        while 1:
            if res["game over"]:
                for event in pygame.event.get():
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_r]:
                        res["keep playing"] = True
                    elif keys[pygame.K_ESCAPE] or keys[pygame.K_a]:
                        #pygame.display.quit()
                        #sys.exit()
                        pygame.mixer.music.stop()
                        return
                if res["keep playing"]:
                    break
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    pygame.mixer.music.stop()
                    pygame.display.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_position = pygame.mouse.get_pos()
                    res["current quadrant"] = mouse_in_quadrant(mouse_position,
                                                                res["quadrants"])
                    res["game state"] = update_state_machine()
                    res[res["game state"] + " logic"]()
                elif keys[pygame.K_r]:
                    res["keep playing"] = True
            if res["keep playing"]:
                    break

            update_screen()
            res[res["game state"] + " display"]()

            advance_frame()

        #res["battle music"].stop()
        pygame.mixer.music.stop()

def play(screen = None, my_pk = None, opp_pk = None):
    main(screen, my_pk, opp_pk)

res = {} # Resources dict kept as a global variable for easy access
if __name__ == "__main__":
    main()
