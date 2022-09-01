import arcade

from konstante import PODESAVANJE_LIKA, DESNO_OKRENUT

def load_texture_pair(filename):
    '''ucitaj sliku i zrcali'''
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]
    
class Entity(arcade.Sprite):
    def __init__(self, file):
        super().__init__()
        
        #defoltno okrenut lik
        self.facing_direction = DESNO_OKRENUT
        
        #koristi se za sekvence slika
        self.cur_texture = 0
        self.scale = PODESAVANJE_LIKA
        
        self.animations = {}
        
        self.idle_texture_pair = load_texture_pair(f"{file}_idle.png")
        self.jump_texture_pair = load_texture_pair(f"{file}_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{file}_fall.png")
        
        #texture za hodanje
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{file}_walk{i}.png")
            self.walk_textures.append(texture)
            
        #texture za penjanje
        self.climbing_textures = []
        texture = arcade.load_texture(f"{file}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{file}_climb1.png")
        self.climbing_textures.append(texture)
        
        #set inicijalnu texturu
        self.texture = self.idle_texture_pair[0]
        