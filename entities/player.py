from konstante import LIJEVO_OKRENUT, DESNO_OKRENUT
from entities.entity import Entity

class Player(Entity):
    '''Player sprite'''
    
    def __init__(self, file):
        
        super().__init__(file)
        
        #pracenje stanja
        self.can_jump = False
        self.climbing = False
        self.is_on_ladder = False
        
    def update_animation(self, delta_time: float = 1 / 60):
        #vidit triba li gledat livo ili desno
        if self.change_x < 0 and self.facing_direction == DESNO_OKRENUT:
            self.facing_direction = LIJEVO_OKRENUT
        elif self.change_x > 0 and self.facing_direction == LIJEVO_OKRENUT:
            self.facing_direction = DESNO_OKRENUT
            
        #animacija za penjanje
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return
        
        #animacija za skakanje
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.facing_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.facing_direction]
            
        #stajaca animacija
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return
        
        #animacija hodanja
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.facing_direction]