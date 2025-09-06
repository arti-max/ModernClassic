import math
import random
from src.level.tile.Tile import Tile
from src.phys.AABB import AABB
import numpy as np
from src.level.LeveListener import LevelListener
from src.level.generator.NoiseFilter import NoiseFilter
import src.level.TileType as TileType
from src.level.Util import nextInt
import pickle


class Level:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        
        self.blocks = [-1] * width * height * depth
        # self.blocks = np.ones(width * height * depth, dtype=np.uint8)
        self.lightDepths = [0] * width * height
        
        self.levelListeners: LevelListener = []
        
        height_map = self.generate_height_map(width, height)
        
        self.generate_map(height_map)
        
        # for x in range(width):
        #     for z in range(height):
        #         for y in range(depth):
        #            self.blocks[self.generate_index(x, y, z)] = (2 if (y < int(depth * 2 / 3)) else 0 if (y != int(depth * 2 / 3)) else 1)
                                                
        self.calcLightDepths(0, 0, width, height)
        
        self.load()
        
    def generate_height_map(self, width, height):

        noise_generator = NoiseFilter(seed=random.randint(0, 12345))
        height_map = [[0 for _ in range(height)] for _ in range(width)]

        for x in range(width):
            for z in range(height):
                noise_value = noise_generator.get_noise(x, z)
                
                base_height = self.depth // 2
                variation = 16
                
                height_map[x][z] = int(base_height + noise_value * variation)
                
        return height_map

    def generate_map(self, height_map):

        for x in range(self.width):
            for z in range(self.height):
                world_height = height_map[x][z]
                for y in range(self.depth):
                    index = self.generate_index(x, y, z)
                    if y < world_height:
                        self.blocks[index] = TileType.STONE.id
                    elif y == world_height:
                        self.blocks[index] = TileType.GRASS.id
                    else:
                        self.blocks[index] = 0 # Air
                    
    def generate_index(self, x, y, z):
        return x + y * self.width + z * self.width * self.depth
    
    def load(self):
        try:
            file = open("level.sav", "rb")
            self.blocks = pickle.load(file)
            self.calcLightDepths(0, 0, self.width, self.height)
            file.close()
            
            for listener in self.levelListeners:
                listener.allChanged()
        except Exception as e:
            print(f"Error while loading level: {e}")
    
    def save(self):
        try:
            file = open("level.sav", "wb")
            pickle.dump(self.blocks, file)
            file.close()
        except Exception as e:
            print(f"Error while saving level: {e}")
    
    def calcLightDepths(self, minX, minZ, maxX, maxZ):
        for x in range(minX, minX + maxX):
            for z in range(minZ, minZ + maxZ):
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
                        
    def onTick(self):
        totalTiles: int = self.width * self.height * self.depth
        
        ticks: int = int(totalTiles / 400)
        
        for i in range(ticks):
            x = nextInt(self.width)
            y = nextInt(self.depth)
            z = nextInt(self.height)
            
            tile = Tile.TILES[self.getTile(x, y, z)]
            if (tile):
                tile.onTick(self, x, y, z)
            
    def isSolidTile(self, x, y, z):
        tile = Tile.TILES[self.getTile(x, y, z)]
        return tile != 0 and tile.isSolid()
    
    def getTile(self, x, y, z):
        if (not self.isTile(x, y, z)):
            return 0
        
        return self.blocks[self.generate_index(x, y, z)]
    
    def isTile(self, x, y, z):
        if (x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height):
            return False
        
        # print(x, y, z)
        
        return self.blocks[self.generate_index(x, y, z)] != 0
    
    def isLightBlocker(self, x, y, z):
        tile = Tile.TILES[self.getTile(x, y, z)]
        return tile != 0 and tile.blocksLight()
    
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
                    
                    tile = Tile.TILES[self.getTile(x, y, z)]
                    
                    if (tile != 0):
                        aabb = tile.getAABB(x, y, z)
                        
                        if (aabb):
                            boundingBoxList.append(aabb)
                        
        return boundingBoxList
    
    def addListener(self, listener: LevelListener):
        self.levelListeners.append(listener)
    
    def setTile(self, x, y, z, id):
        if (x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height):
            return
        
        if (self.blocks[self.generate_index(x, y, z)] == id):
            return
        
        self.blocks[self.generate_index(x, y, z)] = id
        
        self.calcLightDepths(x, z, 1, 1)
        
        for listener in self.levelListeners:
            listener.tileChanged(x, y, z)
        