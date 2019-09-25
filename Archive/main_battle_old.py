import sys, pygame, time, random
import battle, get_pokemon_info
from PIL import Image

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

def get_pokemon_names(pokemon_numbers):
    numbered_pokemon = get_pokemon_info.get_dict("numbered_pokemon.txt")
    names = []
    for num in pokemon_numbers:
        names += [numbered_pokemon[num]]

    return names

def get_moves(pokemon_name):
    moves = get_pokemon_info.get_random_moves(pokemon_name)
    return moves

def get_move_surface(move, anti_alias, text_colour):
    return myfont.render(move, True, text_colour)

def get_random_pokemon(number_of_pokemon):
    # Returns a list of n random pokemon from
    # 001 - 649 (Bulbasaur to Genesect)    
    pokemon_numbers = []
    for i in range(number_of_pokemon):
        num = random.randrange(1, 650)
        num = get_pokemon_info.pokemon_number(num)
        pokemon_numbers += [num]

    return pokemon_numbers 

def create_pokemon(pokemon_numbers, moves):
    pokemon = []
    numbered_pokemon = get_pokemon_info.get_dict("numbered_pokemon.txt")
    # TODO:
    # - Get the following placeholder stats from a dict instead
    i = 0
    all_stats = get_pokemon_info.get_dict("pokemon_stats.txt")
    
    for num in pokemon_numbers:
        name = numbered_pokemon[get_pokemon_info.pokemon_number(num)]
        pokemon += [battle.Pokemon(name, moves[i], all_stats[name])]
        i += 1

    return pokemon

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

def mouse_in_quadrant(mouse_position, move_quadrants):
    for i in range(4):
        if move_quadrants[i].collidepoint(mouse_position):
            return i
    return -1

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
        battle_text += [myfont.render(battle_text_message[i] , True , (0, 0, 0))]

    return battle_over, battle_text

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
	

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    #myfont = pygame.font.SysFont('Verdana', 25)
    myfont = pygame.font.Font("Resources\\Pokemon Fonts\\pkmnrs.ttf", 30)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    yellow = (255, 255, 0)
    blue = (0, 0, 255)
    text_colour = black
    anti_alias = True

    size = width, height = 720, 480

    screen = pygame.display.set_mode(size)

    number_of_pokemon = 2
    pokemon_numbers = get_random_pokemon(number_of_pokemon)
    #pokemon_numbers[1] = "007"
    pokemon_names = get_pokemon_names(pokemon_numbers)
    pokemon_1 = pokemon_numbers[0]
    pokemon_2 = pokemon_numbers[1]
    #pokemon_position = (420, 50)
    moves = get_moves(pokemon_names[0])
    opponent_moves = get_moves(pokemon_names[1])
    all_moves = get_pokemon_info.get_dict("all_moves.txt")
    pokemon = create_pokemon(pokemon_numbers, [moves, opponent_moves])
    p0 = pokemon[0]
    p1 = pokemon[1]
    #if pokemon_1 == "632": pokemon_position = (380, 20)
    # Test pokemon
    # Original size: 96 x 96, scaled size = 288, 288
    f2 = pygame.image.load("Resources\\bw-001n\\" + pokemon_2 + ".png")
    pokemon_position = get_opponent_position(pokemon_2)
    #f2 = pygame.transform.scale(f2, (288, 288))
    f2 = pygame.transform.scale(f2, (192, 192))
    f1 = pygame.image.load("Resources\\bwback-001n\\" + pokemon_1 + ".png")
    f1 = pygame.transform.scale(f1, (288, 288))
    bg = pygame.image.load("Resources\\battle_screen_with_moves_blank.png")
    type_icons = load_pokemon_type_icons()
    moves_bar = pygame.image.load("Resources\\moves_bar.png")
    move_selection = pygame.image.load("Resources\\move_selection.png")
    text_bar = pygame.image.load("Resources\\text_bar.png")
    hp_bar_1 = pygame.image.load("Resources\\hp_bar_01.png")
    hp_bar_2 = pygame.image.load("Resources\\hp_bar_02.png")
    green_hp_1 = pygame.image.load("Resources\\hp_bars\\green.png")
    green_hp_2 = pygame.image.load("Resources\\hp_bars\\green.png")
    yellow_hp_1 = pygame.image.load("Resources\\hp_bars\\yellow.png")
    yellow_hp_2 = pygame.image.load("Resources\\hp_bars\\yellow.png")
    red_hp_1 = pygame.image.load("Resources\\hp_bars\\red.png")
    red_hp_2 = pygame.image.load("Resources\\hp_bars\\red.png")
    empty_hp_1 = pygame.image.load("Resources\\hp_bars\\empty.png")
    empty_hp_2 = pygame.image.load("Resources\\hp_bars\\empty.png")
    hp_bars_pos = [(380, 225), (30, 43)]
    hp_colour_pos = [(hp_bars_pos[1][0] + 95, hp_bars_pos[1][0] + 61)]
    hp_colour_pos += [(hp_bars_pos[1][0] + 459, hp_bars_pos[1][0] + 242)]
    hp_max_colour_width = 144
    hp_widths = [144, 144]
    hp_percent = [p0.stats["HP"] / p0.original_stats["HP"]]
    hp_percent += [p1.stats["HP"] / p1.original_stats["HP"]]
    p0_hp_bar = {"colour" : "green", "width" : 144 * hp_percent[0]}
    p1_hp_bar = {"colour" : "green", "width" : 144 * hp_percent[1]}
    hp_bars = [{
        "green" : green_hp_1, "yellow" : yellow_hp_1,
        "red" : red_hp_1, "empty" : empty_hp_1}]
    hp_bars += [{"green" : green_hp_2, "yellow" : yellow_hp_2,
                 "red" : red_hp_2, "empty" : empty_hp_2}]
    prev_hp = [p1.original_stats["HP"], p0.original_stats["HP"]]

    # Positions are in (width, height) or (x, y) rather than (row, col)
    move_surfaces = []
    # Get user's pokemon's moveset
    #print(pokemon_names)
    
    for move in moves:
        move_surfaces += [get_move_surface(move, anti_alias, text_colour)]
        
    quadrants = initialise_display()
    move_selection_pos = []
    for quadrant in quadrants:
        move_selection_pos += [(quadrant[0] + 3, quadrant[1] + 3)]

    # DEBUG printing:
    #print(pokemon[0].name, "'s stats:", pokemon[0].stats)
    #print()
    #print(pokemon[1].name, "'s stats:", pokemon[1].stats)
    game_state = "show_moves"
    game_over = False
    my_turn = True
    exit_game = False
    move_selected = -1 # [-1, 0, 1] = [not selected, selected, confirmed]
    selected_index = -2
    
    while 1:
        #time.sleep(0.01) # To slow down the animation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Close the window
                pygame.display.quit()
                # Exit the program
                sys.exit()
            # If the mouse button is (pressed and) released
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()
                i = mouse_in_quadrant(mouse_position, quadrants)
                if i != -1:
                    if move_selected == -1:
                        selected_index = i                        
                        move_selected = 1
                    elif move_selected == 0:
                        move_selected = 1
                    elif move_selected == 1:
                        if game_state == "show_moves":
                            if i == selected_index and pokemon[0].stats["HP"] * \
                                          pokemon[1].stats["HP"] != 0:
                                current_move = moves[i]
                                opponent_move = opponent_moves[random.randrange(3)]
                                if game_over:
                                    game_state = "game_over"
                                else:
                                    game_state = "battle_text_1"
                                if not game_over:
                                    game_over, battle_text_1 = show_attack(p0, p1, current_move)
                                    last_move = battle_text_1
                                if not game_over:
                                    game_over, battle_text_2 = show_attack(p1, p0, opponent_move)
                                    last_move = battle_text_2
                                battle_text = last_move
                            else:
                                if i > -1:
                                    selected_index = i                        
                        elif game_state == "battle_text_1":
                            if i > -1:
                                if game_over:
                                    if p1.stats["HP"] == 0:
                                        game_state = "game_over"
                                    else:
                                        game_state = "battle_text_2"
                                    if p0.stats["HP"] == 0:
                                        winner = p0.name
                                    elif p1.stats["HP"] == 0:
                                        winner = p1.name
                                else:
                                    game_state = "battle_text_2"
                        elif game_state == "battle_text_2":
                            if i > -1:
                                if game_over:
                                    game_state = "game_over"
                                    if p0.stats["HP"] == 0:
                                        winner = p0.name
                                    elif p1.stats["HP"] == 0:
                                        winner = p1.name
                                else:
                                    selected_index = -2
                                    move_selected = -1                                    
                                    game_state = "show_moves"
                        elif game_state == "game_over":
                            game_state = "exit_game"
            if game_state == "exit_game":
                pygame.display.quit()
                # Exit the program
                sys.exit()
                    
        screen.fill(black)
        # Display background, pokemon, hp bars, and moves/battle text:
        screen.blit(bg, (0, 0))
        screen.blit(f1, (60, 150))
        screen.blit(f2, pokemon_position)
        screen.blit(hp_bar_1, (380, 225))
        screen.blit(hp_bar_2, (30, 43))
        
        # Change hp bars:
        #if p0.stats["HP"] * p1.stats["HP"] != 0:
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
        prev_hp = [pokemon[1].stats["HP"], pokemon[0].stats["HP"]]
        hp_text = [myfont.render(hp_text_message[0] , anti_alias, text_colour)]
        hp_text += [myfont.render(hp_text_message[1] , anti_alias, text_colour)]
        screen.blit(hp_text[1], (hp_colour_pos[0][0] + 80, hp_colour_pos[0][1] + 15))
        screen.blit(hp_text[0], (hp_colour_pos[1][0] + 80, hp_colour_pos[1][1] + 15))      
        
        if game_state == "show_moves":
            screen.blit(moves_bar, (0, 337))
            screen.blit(move_surfaces[0],(quadrants[0][0] + 30, quadrants[0][1] + 15))
            screen.blit(move_surfaces[1],(quadrants[1][0] + 10, quadrants[1][1] + 15))
            screen.blit(move_surfaces[2],(quadrants[2][0] + 30, quadrants[2][1] + 10))
            screen.blit(move_surfaces[3],(quadrants[3][0] + 10, quadrants[3][1] + 10))
            
            if selected_index != -2:
                screen.blit(move_selection, move_selection_pos[selected_index])

                # Display move information
                highlighted_move = moves[selected_index]
                move_data = all_moves[highlighted_move]
                move_type = move_data[0]
                move_phys_spec = move_data[1]
                move_power = move_data[3]
                move_accuracy = move_data[4]
                move_text = ["Power: " + str(move_power)]
                #move_text += ["Type: " + move_type[0:4].upper() + "/" + move_phys_spec[0:3].upper()]
                move_text += ["Type: "]            
                move_text += ["Accuracy: " + str(move_accuracy) + "%"]
                right_box = [myfont.render(move_text[0] , anti_alias, text_colour)]
                right_box += [myfont.render(move_text[1] , anti_alias, text_colour)]
                right_box += [myfont.render(move_text[2] , anti_alias, text_colour)]
                screen.blit(right_box[0],(505, 360))
                screen.blit(right_box[1],(505, 395))
                screen.blit(right_box[2],(505, 430))
                screen.blit(type_icons[move_type],(573, 392))
                screen.blit(type_icons[move_phys_spec],(641, 394))
        
        elif game_state == "battle_text_1":
            screen.blit(text_bar, (0, 337))
            screen.blit(battle_text_1[0], (25, 360))
            screen.blit(battle_text_1[1], (25, 398))
            screen.blit(battle_text_1[2], (25, 435))
        elif game_state == "battle_text_2":
            screen.blit(text_bar, (0, 337))
            screen.blit(battle_text_2[0], (25, 360))
            screen.blit(battle_text_2[1], (25, 398))
            screen.blit(battle_text_2[2], (25, 435))
        elif game_state == "game_over":
            screen.blit(text_bar, (0, 337))
            screen.blit(battle_text[3], (25, 398))
            exit_game = True

        # Display pokemon names above their respective HP bars
        p1_name_text = myfont.render(p1.name, True, text_colour)
        p0_name_text = myfont.render(p0.name, True, text_colour)
        name_text_pos = [(420, 236), (55, 54)]
        screen.blit(p1_name_text, name_text_pos[1])
        screen.blit(p0_name_text, name_text_pos[0])

        cover_quadrants = False
        if cover_quadrants:
            screen.fill(yellow, quadrants[0])
            screen.fill(red, quadrants[1])
            screen.fill(green, quadrants[2])
            screen.fill(blue, quadrants[3])
            
        #screen.blit(move_selection, move_selection_pos[0])
        #screen.blit(move_selection, move_selection_pos[1])
        #screen.blit(move_selection, move_selection_pos[2])
        #screen.blit(move_selection, move_selection_pos[3])
        
        
        # update whole screen (use display.update(rectangle) to update
        # chosen rectangle portions of the screen to update
        pygame.display.flip()
