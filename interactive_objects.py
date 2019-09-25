"""
Defines the interactive objects in Pokemon World (e.g. NPCs, signs, doors)

## NPC ##
* Sprites are filenames (e.g. "Professor Oak L 0.png" or just
  "Professor Oak L 0" for the first left-facing frame of the sprite),
  and are loaded into pygame within the class

"""

import pygame, tile_viewer, copy
from PIL import Image

SCALE = 3

class Interactive:

    def __init__(self, name):
        self.name = name
        self.text = ""
        #self.sprite = self.load_sprite(name)

    def load_sprite(self, filename, folder = None):
        if not folder:
            folder = "Resources/Overworld/Interactive/" + str(self.name) + "/"
        image = Image.open(folder + filename)
        image = tile_viewer.scale_image(SCALE, image)
        
        sprite = tile_viewer.image_to_pygame(image)
        
        return sprite

class NPC(Interactive):

    def __init__(self, name, pokemon = None, can_battle = None):
        super().__init__(name)
        self.sprites = self.load_sprites()
        self.messages = None
        self.text = None
        self.at_tile = None
        self.dir = "D"
        self.frame_num = 0
        self.message_num = 0
        self.line_num = 0
        self.num_lines = 99999
        self.turned_to_player = False
        if pokemon:
            self.pokemon = pokemon
        self.can_battle = True if can_battle else False
        self.final_line = False
        self.message_surfaces = []

    def load_sprites(self):
        loaded_sprites = {}
        frames = []
        folder = "Resources/Overworld/Interactive/NPCs/" + str(self.name) + "/"
        self.path = folder

        directions = ["U", "D", "L", "R"]
        num_frames = 4
        for direction in directions:
            for i in range(num_frames):
                filename = "{} {} {}.png".format(self.name, direction, i)
                #frames.append(pygame.image.load(folder + filename))
                sprite = super().load_sprite(filename, folder = folder)
                frames.append(sprite)
            loaded_sprites[direction] = frames
            frames = []      

        return loaded_sprites
    def update_line(self):
        if self.text:
            self.num_lines = len(self.messages[self.message_num])
            #self.line_num = (self.line_num + 1) % num_lines
            if self.line_num < self.num_lines:
                self.line_num += 1


        return True
    
    def reset_dialogue(self):
        self.line_num = 0 #len(self.text[self.message_num]) - 1

    def next_message(self):
        self.message_num += 1
        self.line_num = 0

if __name__ == "__main__":
    test = Interactive("test name", "test text")
    print(test.name, test.text)
            
