from entities.enemy import Enemy

class Robot(Enemy):
    def __init__(self):
        file = ":resources:images/animated_characters/robot/robot"
        super().__init__(file)
        self.health = 100