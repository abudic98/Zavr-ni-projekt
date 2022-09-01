from entities.enemy import Enemy

class Zombie(Enemy):
    def __init__(self):
        file = ":resources:images/animated_characters/zombie/zombie"
        super().__init__(file)
        self.health = 50