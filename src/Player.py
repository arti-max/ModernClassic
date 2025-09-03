from src.Entity import Entity
from ursina import held_keys

class Player(Entity):
    def __init__(self, level):
        super().__init__(level)
        

    def tick(self):
        self.prevX = self.x
        self.prevY = self.y
        self.prevZ = self.z
        
        forward = 0.0
        vertical = 0.0
        
        if held_keys['r']:
            self.resetPosition()
            
        if held_keys['w']:
            forward += 1
            
        if held_keys['s']:
            forward -= 1
            
        if held_keys['a']:
            vertical -= 1
            
        if held_keys['d']:
            vertical += 1
            
        if held_keys['space']:
            if self.onGround:
                self.motionY = 0.32
                
        self.moveRelative(vertical, forward, 0.02 if self.onGround else 0.009)
        
        self.motionY -= 0.03
        
        self.move(self.motionX, self.motionY, self.motionZ)
        
        self.motionX *= 0.97
        self.motionY *= 0.98
        self.motionZ *= 0.97
        
        if (self.onGround):
            self.motionX *= 0.9
            self.motionZ *= 0.9
        