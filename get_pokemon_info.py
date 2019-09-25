"""
This program retrieves pokemon information from http://www.serebii.net
and saves the information in text files:
- List of pokemon and their number in the B/W national dex
  e.g. { 001 : "Bulbasaur" }
- Moveset of pokemon from the B/W pokedex
  e.g. { 001 : ["Tackle", "Growl", ...] }
- Moves from the B/W attackdex
  e.g. { "Tackle" : [50, 100, "Physical"] }
- Base stats for each pokemon
  
"""
import urllib.request
import os.path
import ast
import random
from bs4 import BeautifulSoup

def get_pokemon_from_region(main_text, first_pokemon, last_pokemon, region):
    # First string is e.g. "001 Bulbasaur", argument provides "Bulbasaur"
    main_text = main_text[main_text.find(region):]
    start = main_text.find(first_pokemon) - 4
    end = main_text.find(last_pokemon) + len(last_pokemon)
    
    return main_text[start : end] + "\n", main_text[start:]
        
def get_pokemon_list():
    url = "http://www.serebii.net/pokedex-bw/001.shtml"
    main_text = get_html(url, "text")
    text = main_text
    #print(main_text)
    pokemon = ""
    # Mew requires the number as 150 is Mewtwo, so just providing "Mew"
    # causes the program to stop at Mewtwo
    p, text = get_pokemon_from_region(text, "Bulbasaur", "151 Mew", "Kanto:")
    pokemon += p
    p, text = get_pokemon_from_region(text, "Chikorita", "Celebi", "Johto:")
    pokemon += p
    p, text = get_pokemon_from_region(text, "Treecko", "Deoxys", "Hoenn:")
    pokemon += p
    p, text = get_pokemon_from_region(text, "Turtwig", "Arceus", "Sinnoh:")
    pokemon += p
    p, text = get_pokemon_from_region(text, "Victini", "Genesect", "Unova:")
    pokemon += p

    return pokemon.split("\n")
    
def pokemon_list_to_dict_string(pokemon_list):
    # Convert list to dict {num : "name", ...}
    dict_string = "{\n"
    for element in pokemon_list:
        element = element.strip()
        if len(element) < 2: break
        space = element.find(" ")
        dict_string += "\t \"" + element[:space] + "\" : "
        dict_string += "\"" + element[space + 1:] + "\""
        if element != pokemon_list[-2]: dict_string += ",\n"
    dict_string += "\n}"

    # Write list to a txt file
    with open("Resources\\numbered_pokemon.txt", 'w') as file:
        file.write(dict_string)
        
    return dict_string
    
def get_html(url, form):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")

    if form == "messy": return soup
    if form == "neat": return soup.prettify()
    if form == "text": return soup.get_text()
    else:
        raise Exception("Incorrect form argument in get_html(url, form)")

def get_numbered_pokemon():
    if not(os.path.isfile("Resources\\numbered_pokemon.txt")):    
        pokemon_list = get_pokemon_list()
        pokemon_list_to_dict_string(pokemon_list)
    else: print("numbered_pokemon.txt already exists! Using the existing file.")    

def pokemon_number(number):
    if int(number) < 1 or int(number) > 649: number = "001"
    number = str(number)
    return ["00" + number, "0" + number, number][len(number) - 1]

def is_integer(string_):
    try:
        i = int(string_)
        return True
    except:
        return False

def get_pokemon_movesets():
    if not(os.path.isfile("Resources\\pokemon_movesets.txt")):
        move_sets = {} # {pokemon_num : [move name, attack, accuracy]}
        with open("Resources\\numbered_pokemon.txt", 'r') as file:
            numbered_pokemon = ast.literal_eval(file.read())
        for n in range(1, 650):
            pokemon = n
            move_level = 0
            pokemon_num = pokemon_number(str(pokemon))
            url = "http://www.serebii.net/pokedex-bw/" + pokemon_num + ".shtml"
            page_text = get_html(url, "text")
            page_text = page_text[page_text.find("Level Up"):]
            #print(page_text)
            moves_list = page_text.split("\n")
            m = moves_list
            temp_moves = []
            for i in range(1, len(m)):
                if m[i] != "" and m[i] != "Details" and m[i][0].isalpha() \
                   and len(m[i]) < 20:
                    # Check move level (m[i - 1])
                    if is_integer(m[i - 1]) or m[i - 1] == "-":
                        # Continue loop until the highest level up move is found
                        if int(m[i - 1]) < move_level: break
                        else:
                            temp_moves += [m[i]]
                            move_level = int(m[i - 1])
            pokemon_name = numbered_pokemon[pokemon_num]
            print(pokemon_num + " -- " + pokemon_name + " done!")
            move_sets[pokemon_name] = temp_moves

        write_string_to_file(dict_to_string(move_sets), "pokemon_movesets.txt")         
    else: print("pokemon_movesets.txt already exists! Using the existing file.")
          
def get_dict(dict_name):
    if not(file_exists("Resources\\" + dict_name + ".txt")):
        try:
            with open("Resources\\" + dict_name, 'r') as file:
                return ast.literal_eval(file.read())
        except SyntaxError:
            print("Dictionary has incorrect syntax!")
            print("Check that it follows the form {key1:value, key2:value}")
    else:
        print("File " + dict_name + " not found!")

def fix_dict(dict_name):
    # This changes a dict from {key : [[elements]]} -> {key : [elements]}
    # and adds a comma after each element except for the last one if there
    # isn't one
    with open("Resources\\" + dict_name, 'r') as file:
            dict_string = file.read()
    
    moves = dict_string.split("\n")
    for i in range(len(moves)):
        if ":" in moves[i]:
            opening_bracket = moves[i].find("[")
            closing_bracket = moves[i].find("]")
            moves[i] = moves[i][:opening_bracket] +\
                       moves[i][opening_bracket + 1 : closing_bracket + 1] + ","
    moves = "\n".join(moves)
    write_string_to_file(moves, "cleaned_moves.txt")

def get_list_from_text(start_key, end_key, text):
    # Returns (segment, reduced text)
    start = text.find(start_key)
    end = text.find(end_key) + len(end_key)
    return text[start : end], text[end:]

def get_attackdex():
    # First get the move list to be used to iterate through urls
    url = "http://www.serebii.net/attackdex-bw/"
    main_text = get_html(url, "text")
    text = main_text
    text = text[text.find("AttackDex: A - G"):]
    attacks = ""
    a, text = get_list_from_text("Absorb", "Gyro Ball", text)
    attacks += a
    a, text = get_list_from_text("Hail", "Round", text)
    attacks += a
    a, text = get_list_from_text("Sacred Fire", "Zen Headbutt", text)
    attacks += a
    attacks = attacks.split("\n")
    
    # Write attacks to attacks.txt
    with open("Resources\\attacks.txt", "w") as file:
        for i in attacks:
            file.write(i + "\n")
 
    physical_moves = get_all_moves("physical")
    special_moves = get_all_moves("special")
    other_moves = get_all_moves("other")
    
    # Combine all dicts
    all_moves = {**physical_moves, **special_moves, **other_moves}

    # Write all dicts to separate files:
    write_string_to_file(dict_to_string(physical_moves), "physical_moves.txt")
    write_string_to_file(dict_to_string(special_moves), "special_moves.txt")
    write_string_to_file(dict_to_string(other_moves), "other_moves.txt")
    write_string_to_file(dict_to_string(all_moves), "all_moves.txt")

def get_all_moves(physical_special_other):
    # Returns a dict of moves from either the physical, special, or other category
    pso = physical_special_other
    url = "http://www.serebii.net/attackdex-bw/" + pso.lower() + ".shtml"
    
    html = get_html(url, "neat")
    text = get_html(url, "text")
    html_list = html.split("\n")
    
    a = 0
    b = len(html_list)
    for i in range(len(html_list)):
        if 'table class="dextable"' in html_list[i]:
            a = i
        if '<td bgcolor="#507C36" height="86" valign="top" width="1%">' in html_list[i]:
            b = i
    html_list = html_list[a : b]
    
    clean_list = []
    # Remove tags except for <a href = "..."> and <img src="...">
    for i in html_list:
        if ("<" not in i and ">" not in i) or "a href" in i or "img src" in i:
            clean_list += [i]

    # Grab move data from the clean list        
    move_dict = get_move_dict(clean_list)

    return move_dict

def get_move_dict(move_list):
    # Example:
    #<a href="/attackdex-bw/aquajet.shtml">
    #    Aqua Jet
    #   <img src="/attackdex/type/water.gif">
    #   <img src="/pokedex-dp/type/physical.png">
    #   20
    #   40
    #   100
    #   The user lunges at the target at a speed that makes it almost invisible.\
    #   It is sure to strike first.
    
    # <a href> = clean_list[0] (start point)
    # 1 = Move name, 2 = move type, 3 = move physical/special/other
    # 4 = PP, 5 = attack power, 6 = accuracy, 7 = move description
    
    m = move_list
    move_dict = {}
    for i in range(len(m)):
        if "a href" in m[i]:
            name = m[i+1].strip()
            move_type = m[i+2][m[i+2].rfind("/") + 1 : m[i+2].rfind(".")]
            move_phys = m[i+3][m[i+3].rfind("/") + 1: m[i+3].rfind(".")]
            move_pp = "--" if "--" in m[i+4] else int(m[i+4].strip())
            att = "--" if "--" in m[i+5] else int(m[i+5].strip())
            acc = "--" if "--" in m[i+6] else int(m[i+6].strip())
            desc = m[i+7].strip()
            
            move_dict[name] = [move_type, move_phys, move_pp, att, acc, desc]

    return move_dict

def file_exists(file_path):
    if os.path.isfile(file_path): return True
    else: return False

def get_pokemon_types_list():
    # Returns a list of all pokemon types
    all_types = ["bug", "dark", "dragon", "electric", "fighting",\
                 "fire", "flying", "ghost", "grass", "ground",\
                 "ice", "normal", "poison", "psychic", "rock",\
                 "steel", "water"]
    
    return all_types

def get_pokemon_types_dict():
    # Returns a dict of form {"pokemon" : ["type1", "type2"]},
    # where type2 is "" if the pokemon only has one type
    all_types = get_pokemon_types_list()
    pokemon = get_dict("numbered_pokemon.txt")
    types_dict = {}
    for i in all_types:
        url = "http://www.serebii.net/pokedex-bw/" + i + ".shtml"
        html = get_html(url, "neat")
        html = html.split("\n")
        start = 0
        end = len(html) - 1
        # Shorten the html list
        for j in range(len(html)):
            if 'table class="pkmn"' in html[j]:
                start = j
                break
        for j in range(len(html)):
            if 'td bgcolor="#507C36" height="86"' in html[j]:
                end = j
                break
        html = html[start : end]
        for j in html:
            name = j.strip()
            if name in pokemon.values():
                if name in types_dict:
                    types_dict[name] += [i]
                else:
                    types_dict[name] = [i]
        print("Type: " + i + " done!")
    print("All done!")
    return types_dict
                
def generate_moveset(*types):
    # Returns all moves of the type types[0] and all
    # moves of types[1] if there is a second type
    # Currently excludes the moves from the "other" set
    if not(file_exists("Resources\\all_moves.txt")):
        get_attackdex()
    physical_moves = get_dict("physical_moves.txt")
    special_moves = get_dict("special_moves.txt")
    #other_moves = get_dict("other_moves.txt")
    # Can just combine movesets with m3 = {**m1, **m2}

    moves = []
    # Get all physical and special moves of the type(s)
    for i in range(len(types)):
        for key in physical_moves:
            if physical_moves[key][0] == types[i]:
                moves += [key]
        for key in special_moves:
            if special_moves[key][0] == types[i]:
                moves += [key]

    return moves

def get_random_elements(list_, num_elements_wanted, no_repeats):
    random_selection = []
    for i in range(num_elements_wanted):
        rand = random.randrange(len(list_))
        if no_repeats:
            while list_[rand] in random_selection:
                rand = random.randrange(len(list_))
        random_selection += [list_[rand]]
        
    return random_selection

def dict_to_string(dictionary):
    # A neater alternative for converting a dict to a string:
    # While str(dict) creates "{key_1:value_1, ..., key_n:value_n}",
    # dict_to_string(dict) creates
    # "{
    #   key_1 : value_1,
    #   ...,
    #   key_n : value_n
    # }"
    d = dictionary
    dict_string = "{"
    for key in d:
        dict_string += '\n\t"' + str(key) + '" : ' + str(d[key]) + ","
    dict_string = dict_string[:-1] # remove the final comma
    dict_string += "\n}"
    return dict_string

def write_string_to_file(content, filename):
    with open("Resources\\" + filename, "w") as file:
        file.write(content)

def get_random_moves(pokemon_name):
    # Return a set of four unique moves for a given pokemon, based
    # on its type(s); a new moveset is created if one doesn't already
    # exist
    all_moves = get_dict("all_moves.txt")
    movesets = get_dict("pokemon_movesets.txt")
    moveset_exists = move_exists(pokemon_name, movesets)
    if moveset_exists:       
        move_pool = movesets[pokemon_name]
        # Cross reference moves with all_moves and remove invalid moves
        temp_pool = []
        for i in move_pool:
            if i in all_moves: temp_pool += [i]
        move_pool = temp_pool
    else:
        pokemon_types = get_dict("pokemon_types.txt")
        move_pool = generate_moveset(*pokemon_types[pokemon_name])

    #print(move_pool)
        
    no_repeats = True
    number_of_moves = 4
    random_moveset = get_random_elements(move_pool, number_of_moves, no_repeats)

    return random_moveset

def move_exists(key, movesets):
    if len(movesets[key]) < 4:
        return False
    else: return True
  
def get_base_stats():
    url = "http://bulbapedia.bulbagarden.net/wiki" + \
          "/List_of_Pok%C3%A9mon_by_base_stats_(Generation_II-V)"
    # STATS: Pokemon : [HP, ATT, DEF, SP.ATK, SP.DEF, SPEED]
    page_text = get_html(url, "text").split()
    # Since the list is ordered by national dex number, I can just
    # iterate using my numbered_pokemon dict
    numbered_pokemon = get_dict("numbered_pokemon.txt")
    pokemon_stats = {}
    # Find the first pokemon
    for i in range(len(page_text)):
        if page_text[i] == numbered_pokemon["001"]:
            start = i
            break
    page_list = page_text[start:]
    #for i in page_list: print(i)
    for i in range(1, 650):
        num = pokemon_number(i)
        for j in range(len(page_list)):
            if numbered_pokemon[num] in page_list[j]:
                stats = []
                for k in range(1, 7):
                    try:
                        stats += [int(page_list[j + k])]
                    except:
                        #print(page_list[j : j + 7])
                        if page_list[j] != "Unown": 
                            stats += [int(page_list[j + k + 2])]
                if numbered_pokemon[num] == "Unown":
                    pokemon_stats["Unown"] = [48, 72, 48, 72, 48, 48]
                else: pokemon_stats[numbered_pokemon[num]] = stats
                
    #Other special cases:
    pokemon_stats["Nidoran-F"] = [55, 47, 52, 40, 40, 41]
    pokemon_stats["Nidoran-M"] = [46, 57, 40, 40, 40, 50]
    pokemon_stats["Mr.Mime"] = [40, 45, 65, 100, 120, 90]
    pokemon_stats["Porygon 2"] = [85, 80, 90, 105, 95, 60]
    pokemon_stats["Ho-oh"] = [106, 130, 90, 110, 154, 90]
    pokemon_stats["Mime Jr."] = [20, 25, 45, 70, 90, 60]
   
    write_string_to_file(dict_to_string(pokemon_stats), "pokemon_stats.txt")

def get_stat_moves():
    # Basic filter between stat-changing and non stat-changing
    other_moves = get_dict("other_moves.txt")
    stat_changes = {}
    non_stat_changes = {}
    for move in other_moves:
        description = other_moves[move][5]
        if "stat" in description.lower():
            stat_changes[move] = description
        else:
            non_stat_changes[move] = description

    write_string_to_file(dict_to_string(stat_changes), "stat_changes.txt")
    write_string_to_file(dict_to_string(non_stat_changes), "non_stat_changes.txt")

    # Create different txt files for each stat being changed
    sp_atk_changes = {}
    atk_changes = {}
    sp_def_changes = {}
    def_changes = {}
    speed_changes = {}
    remaining_other = {}
    
    for move in other_moves:
        description = other_moves[move][5]
        desc = description.lower()
        if "sp. atk" in desc or "special at" in desc:
            sp_atk_changes[move] = description
        elif "sp. def" in desc or "special def" in desc:
            sp_def_changes[move] = description
        elif "attack" in desc or "atk" in desc:
            atk_changes[move] = description
        elif "defence" in desc or "defens" in desc:
            def_changes[move] = description
        elif "speed" in desc or "spd" in desc:
            speed_changes[move] = description
        else:
            remaining_other[move] = description

    write_string_to_file(dict_to_string(sp_atk_changes), "sp_atk_changes.txt")
    write_string_to_file(dict_to_string(sp_def_changes), "sp_def_changes.txt")
    write_string_to_file(dict_to_string(atk_changes), "atk_changes.txt")
    write_string_to_file(dict_to_string(def_changes), "def_changes.txt")
    write_string_to_file(dict_to_string(speed_changes), "speed_changes.txt")
    write_string_to_file(dict_to_string(remaining_other), "remaining_other.txt")
                
if __name__ == "__main__":
    #get_attackdex()
    #get_numbered_pokemon()
    #d = get_dict("numbered_pokemon.txt")
    #with open("Resources\\numbered_pokemon.txt", "r") as file:
    #    d = ast.literal_eval(file.read())
    #    print(d["003"])
    #get_pokemon_movesets()
    #d = get_dict("all_moves.txt")
    #fix_dict("pokemon_movesets.txt")
    #movesets = get_dict("pokemon_movesets.txt")
    #pokemon_names = get_dict("numbered_pokemon.txt")
    #write_string_to_file(dict_to_string(get_pokemon_types_dict()), "pokemon_types.txt")
    #html = get_html("http://www.serebii.net/pokedex-bw/bug.shtml", "neat")
    #print(html)
    #moveset_exists = True
    #print(get_random_moves("Gyarados"))
    #get_base_stats()
    #pokemon_stats = get_dict("pokemon_stats.txt")
    #numbered_pokemon = get_dict("numbered_pokemon.txt")
    #for num in numbered_pokemon:
    #    if numbered_pokemon[num] not in pokemon_stats:
    #        #print(numbered_pokemon[num])
    #        pass
    #get_stat_moves()
    pass

