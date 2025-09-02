from src.Entity import Entity
from src.InputManager import input_manager as keyboard

class Player(Entity):
    def __init__(self, level):
        super().__init__(level)
        

    def tick(self):
        self.prevX = self.x
        self.prevY = self.y
        self.prevZ = self.z
        
        forward = 0.0
        vertical = 0.0
        
        if (keyboard.is_pressed('r')):   # R
            self.resetPosition()
            
        if (keyboard.is_pressed('w')):   # W
            forward += 1
            
        if (keyboard.is_pressed('s')):   # S
            forward -= 1
            
        if (keyboard.is_pressed('a')):   # A
            vertical -= 1
            
        if (keyboard.is_pressed('d')):   # D
            vertical += 1
            
        if (keyboard.is_pressed('space')):   # Space
            if (self.onGround):
                self.motionY = 0.12
                
        self.moveRelative(vertical, forward, 0.02 if self.onGround else 0.005)
        
        self.motionY -= 0.005
        
        self.move(self.motionX, self.motionY, self.motionZ)
        
        self.motionX *= 0.97
        self.motionY *= 0.98
        self.motionZ *= 0.97
        
        if (self.onGround):
            self.motionX *= 0.9
            self.motionZ *= 0.9
        