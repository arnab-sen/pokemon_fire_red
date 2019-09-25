"""
TODO:
- Import two fighters from a dict in a txt file
- Begin with fighters having two stats: HP and attack power
- Fighters have up to four moves each and take turns attacking
- First one to 0 HP loses the battle
"""
import ast
import get_pokemon_info
import random

class Fighter:
    "Has HP and ATK"

    def __init__(self, name, HP, ATK):
        self._name = name
        self._HP = HP
        self._ATK = ATK

    def set_name(self, value):
        self._name = value

    def get_name(self):
        return self._name

    def set_HP(self, value):
        self._HP = value

    def get_HP(self):
        return self._HP

    def set_ATK(self, value):
        self._name = value

    def get_ATK(self):
        return self._ATK

    name = property(get_name, set_name)
    HP = property(get_HP, set_HP)
    ATK = property(get_ATK, set_ATK)
    
def get_pokemon_names():
    pokemon = get_pokemon_info.get_dict("numbered_pokemon.txt")
    return pokemon

def get_battle_data():
    with open("Resources\\fighters.txt") as file:
        names_dict = ast.literal_eval(file.read())
        names = [names_dict["fighter1"], names_dict["fighter2"]]
    return names

def initialise_battle(names, HPs, ATKs):
    fighter1 = Fighter(names[0], HPs[0], ATKs[0])
    fighter2 = Fighter(names[1], HPs[1], ATKs[1])
    #print(fighter1.name, fighter1.HP, fighter1.ATK)
    #print(fighter2.name, fighter2.HP, fighter2.ATK)
    fighters = [fighter1, fighter2]
    return fighters

def attack(attacker, defender):
    a = attacker
    d = defender
    print(a.name + " attacks " + d.name)
    print(d.name + "'s HP fell from " + str(d.HP), end = "")
    d.HP = d.HP - a.ATK
    print(" to " + str(d.HP))

def battle(fighters):
    pass

def main():
    pokemon = get_pokemon_names()
    #names = get_battle_data()
    nums = [random.randrange(1, 650), random.randrange(1, 650)]
    nums[0] = get_pokemon_info.pokemon_number(nums[0])
    nums[1] = get_pokemon_info.pokemon_number(nums[1])
    names = [pokemon[nums[0]], pokemon[nums[1]]]
    HPs = [100, 150]
    ATKs = [50, 25]
    fighters = initialise_battle(names, HPs, ATKs)
    f1 = fighters[0]
    f2 = fighters[1]
    print(f1.name + "'s HP: " + str(f1.HP))
    attack(f1, f2)
    attack(f2, f1)

main()    
