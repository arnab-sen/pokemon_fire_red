"""
Defines the pokemon class and battle logic between two pokemon

TODO:
- Change class functions to get stats from get_pokemon_info
- Import two pokemon from a dict in a txt file
- Begin with pokemon having two stats: HP and attack power
- Pokemon have up to four moves each and take turns attacking
- First one to 0 HP loses the battle
"""

import ast
import get_pokemon_info
import random

class Pokemon:

    def __init__(self, name, moves, stats):
        self.name = name
        self.moves = moves
        #print(stats[0], type(stats[0]))
        # Stats based on:
        # https://pokemondb.net/pokebase/200194/how-do-base-stats-work
        
        self.original_stats = {
                                    "HP" : stats[0] * 2 + 110,
                                    "ATK" : stats[1] * 2 + 5,
                                    "DEF" : stats[2] * 2 + 5,
                                    "SP.ATK" : stats[3] * 2 + 5,
                                    "SP.DEF" : stats[4] * 2 + 5,
                                    "SPEED" : stats[5] * 2 + 5
                               }

        self.stats = {
                            "HP" : stats[0] * 2 + 110,
                            "ATK" : stats[1] * 2 + 5,
                            "DEF" : stats[2] * 2 + 5,
                            "SP.ATK" : stats[3] * 2 + 5,
                            "SP.DEF" : stats[4] * 2 + 5,
                            "SPEED" : stats[5] * 2 + 5
                      }


def get_pokemon_names():
    return get_pokemon_info.get_dict("numbered_pokemon.txt")

def type_effectiveness(move, attacker, defender):
    pass

def calculate_damage(attacker, defender, move):
    # This calculates the damage dealt to the defender
    # EXCEPTIONS:
    # - "Other" attacks in the other_attacks dict
    # - Direct damaging moves (e.g. Dragon Rage, Bide):
    #   http://bulbapedia.bulbagarden.net/wiki/
    #   Category:Moves_that_deal_direct_damage
    #   These moves will be in their own dict and will
    #   either have a constant value (e.g. Dragon Rage - 40)
    #   or will have a custom-calculated value (e.g. Bide, Counter)
    all_moves = get_pokemon_info.get_dict("all_moves.txt")
    move_data = all_moves[move]
    pokemon_types = get_pokemon_info.get_dict("pokemon_types.txt")
    level = 100
    modifier = 1
    
    if move_data[1] == "physical":
        attack = attacker.stats["ATK"]
        defence = defender.stats["DEF"]
    elif move_data[1] == "special":
        attack = attacker.stats["SP.ATK"]
        defence = defender.stats["SP.DEF"]
    elif move_data[1] == "other":
        attack = 1
        defence = 1
    else:
        print("\nError with move type of: " + move_data[1])
        attack = 1
        defence = 1
    
    if move_data[3] == "--":
        power = 0
    else:
        power = int(move_data[3])
    damage = power * (attack / defence) / 50
    damage *= (2 * level / 5 + 2)

    # STAB multiplier
    if move_data[0] in pokemon_types[attacker.name]:
        modifier *= 1.5

    damage *= modifier
    damage = round(damage)
    
    return damage

def initialise_battle(names, HPs, ATKs):
    pokemon1 = Pokemon(names[0], HPs[0], ATKs[0])
    pokemon2 = Pokemon(names[1], HPs[1], ATKs[1])
    #print(pokemon1.name, pokemon1.HP, pokemon1.ATK)
    #print(pokemon2.name, pokemon2.HP, pokemon2.ATK)
    pokemon = [pokemon1, pokemon2]
    return pokemon

def attack(attacker, defender, move):
    a = attacker
    d = defender
    damage = calculate_damage(a, d, move)
    #print(a.name + " attacks " + d.name)
    #print(d.name + "'s HP fell from " + str(d.HP), end = "")
    d.stats["HP"] = d.stats["HP"] - damage
    if d.stats["HP"] < 0: d.stats["HP"] = 0
    #print(" to " + str(d.HP))

if __name__ == "__main__":
    pass
