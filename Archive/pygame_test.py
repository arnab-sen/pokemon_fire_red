import sys, pygame, time, random
import get_pokemon_info, battle
# Get a random pokemon with random moves selected from that
# Pokemon's moveset (will need multiple dicts for pokemon
# and their movesets --> use webscraping from serebii
# or bulbapedia to get stats and movesets) -->
# use web scraping to get all info required just once,
# and store that info in txt files

# Make moves into buttons using mouse.get_pos() and
# having a button rectangle set around each move
# (perform an action if the mouse click is within
# that rectangle)
# Move rectangle quadrants in the form (top left), (bottom right):
# Quadrant 1 (top left): (18, 356), (240, 410)
# Quadrant 2 = top right, 3 = bottom left, 4 = bottom right 
moves_top_left = (18, 356)
moves_center = (240, 410)
quadrant_width = moves_center[0] - 18
quadrant_height = moves_center[1] - 356
quadrant_1 = pygame.Rect(18, 356, quadrant_width, quadrant_height)
quadrant_2 = pygame.Rect(241, 356, quadrant_width, quadrant_height)
quadrant_3 = pygame.Rect(18, 410, quadrant_width, quadrant_height)
quadrant_4 = pygame.Rect(241, 410, quadrant_width, quadrant_height)
move_quadrants = [quadrant_1, quadrant_2, quadrant_3, quadrant_4]

pygame.init()
pygame.font.init()
#myfont = pygame.font.SysFont('Verdana', 25)
your_pokemon = "Totodile"
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

# Get pokemon
pokemon_1 = str(random.randrange(1, 650))
if len(pokemon_1) == 1: pokemon_1 = "00" + pokemon_1
elif len(pokemon_1) == 2: pokemon_1 = "0" + pokemon_1
pokemon_2 = str(random.randrange(1, 650))
if len(pokemon_2) == 1: pokemon_2 = "00" + pokemon_2
elif len(pokemon_2) == 2: pokemon_2 = "0" + pokemon_2
#pokemon_2 = "466"
pokemon_1 = "158" # Totodile
pokemon_2 = "006" # Charizard
pokemon_position = (420, 50)
if pokemon_1 == "632": pokemon_position = (380, 20)
# Test pokemon
# Original size: 96 x 96, scaled size = 288, 288
f2 = pygame.image.load("Resources\\bw-001n\\" + pokemon_2 + ".png")
#f2 = pygame.transform.scale(f2, (288, 288))
f2 = pygame.transform.scale(f2, (192, 192))
f1 = pygame.image.load("Resources\\bwback-001n\\" + pokemon_1 + ".png")
f1 = pygame.transform.scale(f1, (288, 288))
bg = pygame.image.load("Resources\\battle_screen_with_moves_blank.png")
moves_bar = pygame.image.load("Resources\\moves_bar.png")

# Get moves
#move_1 = input("Enter move 1: ")
moves = ["Scratch", "Water Gun", "Bite", "Ice Fang"]
physical_moves = get_pokemon_info.get_dict("physical_moves.txt")
special_moves = get_pokemon_info.get_dict("special_moves.txt")
all_moves = {**physical_moves, **special_moves}
movesets = get_pokemon_info.get_dict("pokemon_movesets.txt")
poke_1 = "Totodile"
poke_2 = "Charizard"
moves = get_pokemon_info.get_random_moves(poke_1) 

# Note that positions are in (width, height) or (x, y) rather than (row, col)
move_1_surface = myfont.render(moves[0], anti_alias, text_colour)
move_2_surface = myfont.render(moves[1], anti_alias, text_colour)
move_3_surface = myfont.render(moves[2], anti_alias, text_colour)
move_4_surface = myfont.render(moves[3], anti_alias, text_colour)
move_power = myfont.render('Move Power', anti_alias, text_colour)
#screen.blit(textsurface,(0,0))

def mouse_in_quadrant(mouse_position, move_quadrants):
    for i in range(4):
        if move_quadrants[i].collidepoint(mouse_position):
            return i
    return -1

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
            i = mouse_in_quadrant(mouse_position, move_quadrants)
            if i > -1:
                current_move = moves[i]
                print(your_pokemon + " used " + current_move + "!")

    screen.fill(black)
    screen.blit(bg, (0, 0))
    screen.blit(f1, (60, 150))
    screen.blit(f2, pokemon_position)
    screen.blit(moves_bar, (0, 337))
    # Show move quadrants
    #screen.fill(yellow, quadrant_1)
    #screen.fill(red, quadrant_2)
    #screen.fill(green, quadrant_3)
    #screen.fill(blue, quadrant_4)
    screen.blit(move_1_surface,(quadrant_1[0] + 30, quadrant_1[1] + 15))
    screen.blit(move_2_surface,(quadrant_2[0] + 10, quadrant_2[1] + 15))
    screen.blit(move_3_surface,(quadrant_3[0] + 30, quadrant_3[1] + 10))
    screen.blit(move_4_surface,(quadrant_4[0] + 10, quadrant_4[1] + 10))
    screen.blit(move_power,(525, 395))
    
    
    # update whole screen (use display.update(rectangle) to update
    # chosen rectangle portions of the screen to update
    pygame.display.flip()


