import math
import random
from src.phys.AABB import AABB
import numpy as np
from src.level.LeveListener import LevelListener


class Level:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        
        self.blocks = [-1] * width * height * depth
        # self.blocks = np.ones(width * height * depth, dtype=np.uint8)
        self.lightDepths = [0] * width * height
        
        self.levelListeners: LevelListener = []
        
        for x in range(width):
            for z in range(height):
                for y in range(depth):
                   self.blocks[self.generate_index(x, y, z)] = (1 if (y <= int(depth * 2 / 3)) else 0)
                             
                             
        print(self.blocks)
        self.calcLightDepths(0, 0, width, height)
                    
    def generate_index(self, x, y, z):
        return x + y * self.width + z * self.width * self.depth
    
    def calcLightDepths(self, minX, minZ, maxX, maxZ):
        for x in range(minX, maxX):
            for z in range(minZ, maxZ):
                prevDepth = self.lightDepths[x + z * self.width]
                
                depth = self.depth - 1
                while (depth > 0 and not self.isLightBlocker(x, depth, z)):
                    depth -= 1
                    
                    
                self.lightDepths[x + z * self.width] = depth
                
                if (prevDepth != depth):
                    minTileChangeY = min(prevDepth, depth)
                    maxTileChangeY = max(prevDepth, depth)
                    
                    for listener in self.levelListeners:
                        listener.lightColumnChanged(x, z, minTileChangeY, maxTileChangeY)
            
    def isSolidTile(self, x, y, z):
        return self.isTile(x, y, z)
    
    def getTile(self, x, y, z):
        if (not self.isTile(x, y, z)):
            return -1
        
        return self.blocks[self.generate_index(x, y, z)]
    
    def isTile(self, x, y, z):
        if (x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height):
            return False
        
        # print(x, y, z)
        
        return self.blocks[self.generate_index(x, y, z)] != 0
    
    def isLightBlocker(self, x, y, z):
        return self.isSolidTile(x, y, z)
    
    def getBrightness(self, x, y, z):
        dark = 0.5
        light = 1.0
        
        if (x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height):
            return light
        
        if (y < self.lightDepths[x + z * self.width]):
            return dark
        
        return light    # Unknown bright
    
    def isLit(self, x, y, z):
        return (x < 0 or y < 0 or z < 0 or x >= self.width or z >= self.height or y >= self.lightDepths[x + z * self.width])
    
    def getCubes(self, boundingBox: AABB) -> list[AABB]:
        boundingBoxList: list[AABB] = []
        
        minX: int = int(math.floor(boundingBox.min_x) - 1)
        maxX: int = int(math.ceil(boundingBox.max_x) + 1)
        minY: int = int(math.floor(boundingBox.min_y) - 1)
        maxY: int = int(math.ceil(boundingBox.max_y) + 1)
        minZ: int = int(math.floor(boundingBox.min_z) - 1)
        maxZ: int = int(math.ceil(boundingBox.max_z) + 1)
        
        minX = max(0, minX)
        minY = max(0, minY)
        minZ = max(0, minZ)
        
        maxX = min(self.width, maxX)
        maxY = min(self.depth, maxY)
        maxZ = min(self.height, maxZ)
        
        for x in range(minX, maxX):
            for y in range(minY, maxY):
                for z in range(minZ, maxZ):
                    if (self.isSolidTile(x, y, z)):
                        boundingBoxList.append(AABB(x, y, z, x+1, y+1, z+1))
                        
        return boundingBoxList
    
    def addListener(self, listener: LevelListener):
        self.levelListeners.append(listener)
    
    def setTile(self, x, y, z, id):
        if (x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height):
            return
        
        if (self.blocks[self.generate_index(x, y, z)] == id):
            return
        
        self.blocks[self.generate_index(x, y, z)] = id
        
        self.calcLightDepths(x, z, x + 1, z + 1)
        
        for listener in self.levelListeners:
            listener.tileChanged(x, y, z)
        