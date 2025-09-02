



import math
import random
from src.phys.AABB import AABB


class Entity:
    def __init__(self, level):
        self.level = level
        
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0
        
        self.prevX: float = 0.0
        self.prevY: float = 0.0
        self.prevZ: float = 0.0
        
        self.motionX: float = 0.0
        self.motionY: float = 0.0
        self.motionZ: float = 0.0
        
        self.xRotation: float = 0.0
        self.yRotation: float = 0.0
        
        self.onGround: bool = False
        
        self.boundingBox: AABB = None
        
        self.resetPosition()
        
        
    def setPosition(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z
        
        width: float = 0.3
        height: float = 0.9
        
        self.boundingBox = AABB(x - width, y - height, z - width, x + width, y + height, z + width)
        
    def resetPosition(self) -> None:
        x: float = random.random() * self.level.width
        y: float = self.level.depth + 3
        z: float = random.random() * self.level.height
        
        self.setPosition(x, y, z)
        
    def turn(self, x: float, y: float) -> None:
        self.yRotation += x
        self.xRotation -= y
        
        self.xRotation = max(-90.0, self.xRotation)
        self.xRotation = min(90.0, self.xRotation)
        
    def move(self, x: float, y: float, z: float):
        prevX: float = x
        prevY: float = y
        prevZ: float = z
        
        aABBs: list[AABB] = self.level.getCubes(self.boundingBox.expand(x, y, z))
        
        for abb in aABBs:
            y = abb.clip_y_collide(self.boundingBox, y)
        self.boundingBox.move(0.0, y, 0.0)
        
        for abb in aABBs:
            x = abb.clip_x_collide(self.boundingBox, x)
        self.boundingBox.move(x, 0.0, 0.0)
        
        for abb in aABBs:
            z = abb.clip_z_collide(self.boundingBox, z)
        self.boundingBox.move(0.0, 0.0, z)
        
        self.onGround = prevY != y and prevY < 0.0
        
        if(prevX != x): self.motionX = 0.0
        if(prevY != y): self.motionY = 0.0
        if(prevZ != z): self.motionZ = 0.0
        
        self.x = (self.boundingBox.min_x + self.boundingBox.max_x) / 2.0
        self.y = self.boundingBox.min_y + 1.62
        self.z = (self.boundingBox.min_z + self.boundingBox.max_z) / 2.0
        
    def moveRelative(self, x: float, z: float, speed: float) -> None:
        distance: float = x*x + z*z
        
        if (distance < 0.01):
            return
        
        distance = speed / math.sqrt(distance)
        x *= distance
        z *= distance
        
        sin: float = math.sin(math.radians(self.yRotation))
        cos: float = math.cos(math.radians(self.yRotation))
        
        self.motionX += x * cos + z * sin
        self.motionZ += z * cos - x * sin