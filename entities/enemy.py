from konstante import LIJEVO_OKRENUT, DESNO_OKRENUT
from entities.entity import Entity

class Enemy(Entity):
    def __init__(self, file):
        super().__init__(file)
        
        self.should_update_walk = 0
        self.health = 0
        
    def update_animation(self, delta_time: float = 1 / 60):
        #je li triba okrenit livo ili desno
        if self.change_x < 0 and self.facing_direction == DESNO_OKRENUT:
            self.facing_direction = LIJEVO_OKRENUT
        elif self.change_x > 0 and self.facing_direction == LIJEVO_OKRENUT:
            self.facing_direction = DESNO_OKRENUT
            
        #stajaca animacija
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return
        
        #hodajuca animacija
        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
            self.should_update_walk = 0
            return
        
        self.should_update_walk += 1