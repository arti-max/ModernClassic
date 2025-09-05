import math
from random import random
from src.Entity import Entity
from src.character.Cube import Cube
from src.render.Tessellator import Tessellator
import time as ttime
from src.render.Texture import *

from ursina import destroy



class Human(Entity):
    
    def __init__(self, level, x, y, z):
        super().__init__(level)
        
        self.rotation: float = random() * math.pi * 2
        self.rotationMotionFactor: float = (random() + 1.0) * 0.01
        
        self.timeOffset: float = random() * 1239813.0
        self.speed: float = 1.0
        
        self.x = x
        self.y = y
        self.z = z

        self.model_entity = None
        self.tessellator = Tessellator()
        
        self.head = Cube(0, 0).addBox(-4.0, -8.0, -4.0, 8, 8, 8)
        self.body = Cube(16, 16).addBox(-4.0, 0.0, -2.0, 8, 12, 4)
        
        self.rightArm = Cube(40, 16).addBox(-3.0, -2.0, -2.0, 4, 12, 4)
        self.rightArm.setPosition(-5.0, -2.0, 0.0)
        
        self.leftArm = Cube(40, 16).addBox(-1.0, -2.0, -2.0, 4, 12, 4)
        self.leftArm.setPosition(5.0, 2.0, 0.0)
        
        self.rightLeg = Cube(0, 16).addBox(-2.0, 0.0, -2.0, 4, 12, 4)
        self.rightLeg.setPosition(-2.0, -12.0, 0.0)
        
        self.leftLeg = Cube(0, 16).addBox(-2.0, 0.0, -2.0, 4, 12, 4)
        self.leftLeg.setPosition(2.0, -12.0, 0.0)
        
        
    def tick(self):
        super().tick()
        
        self.rotation += self.rotationMotionFactor
        
        self.rotationMotionFactor *= 0.99
        self.rotationMotionFactor += (random() - random()) * random() * random() * 0.009999999776482582 # Very big float number, xd
        
        vertical: float = math.sin(self.rotation)
        forward: float = math.cos(self.rotation)
        
        if (self.onGround and random() < 0.01):
            self.motionY = 0.12
            
        self.moveRelative(vertical, forward, 0.02 if self.onGround else 0.005)
        
        self.motionY -= 0.005
        
        self.move(self.motionX, self.motionY, self.motionZ)
        
        self.motionX *= 0.91
        self.motionY *= 0.98
        self.motionZ *= 0.91
        
        if (self.y < -100): 
            self.resetPosition()
        
        if (self.onGround):
            self.motionX *= 0.8
            self.motionZ *= 0.8
            
    def render(self, partialTicks: float):
        
        if self.model_entity:
            destroy(self.model_entity)
            self.model_entity = None
            
        self.tessellator.clear()
        
        bind_texture('res/char.png')
        self.tessellator.set_texture_atlas(BINDED_TEXTURE)
        
        time = ttime.time() * 10.0 * self.speed + self.timeOffset
        
        interpolatedX = self.prevX + (self.x - self.prevX) * partialTicks
        interpolatedY = self.prevY + (self.y - self.prevY) * partialTicks
        interpolatedZ = self.prevZ + (self.z - self.prevZ) * partialTicks
        
        self.head.yRotation = math.degrees(math.sin(time * 0.83))
        self.head.xRotation = math.degrees(math.sin(time) * 0.8)
        self.rightArm.xRotation = math.degrees(math.sin(time * 0.6662 + math.pi) * 2.0)
        self.rightArm.zRotation = math.degrees(math.sin(time * 0.2312) + 1.0)
        self.leftArm.xRotation = math.degrees(math.sin(time * 0.6662 + math.pi) * 2.0)
        self.leftArm.zRotation = math.degrees(math.sin(time * 0.2312) - 1.0)
        self.rightLeg.xRotation = math.degrees(math.sin(time * 0.6662) * 1.4)
        self.leftLeg.xRotation = math.degrees(math.sin(time * 0.6662 + math.pi) * 1.4)
        
        self.tessellator.push_matrix()
        
        self.tessellator.translate(interpolatedX, interpolatedY, interpolatedZ)
        self.tessellator.scale(1.0, -1.0, 1.0)
        
        size = 7.0 / 120.0
        self.tessellator.scale(size, size, size)
        
        offsetY = abs(math.sin(time * 2.0 / 3.0)) * 5.0 + 23.0
        self.tessellator.translate(0.0, -offsetY, 0.0)
        
        self.tessellator.rotate(math.degrees(self.rotation) + 180, 0.0, 1.0, 0.0)
        
        
        self.head.render(self.tessellator)
        self.body.render(self.tessellator)
        self.rightArm.render(self.tessellator)
        self.leftArm.render(self.tessellator)
        self.rightLeg.render(self.tessellator)
        self.leftLeg.render(self.tessellator)
        
        self.tessellator.pop_matrix()
        
        self.model_entity = self.tessellator.flush()
        
        # print(f"Flushed entity: {self.model_entity}") 
        
        # if self.model_entity:
        #     self.model_entity.scale = 7.0 / 120.0
        
        
    def remove(self):
        if self.model_entity:
            destroy(self.model_entity)