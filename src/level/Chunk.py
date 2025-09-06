from src.level.tile.Tile import Tile
import src.level.TileType as TileType
from src.render.Tessellator import Tessellator
import numpy as np
from typing import Dict
from ursina import load_texture, Entity, destroy

class Chunk:
    UPDATES = 0
    REBUILT_THIS_FRAME = 0
    MAX_REBUILDS_PER_FRAME = 16
    
    TESSELLATOR = Tessellator()
    
    def __init__(self, level, minX, minY, minZ, maxX, maxY, maxZ):
        self.minX = minX
        self.minY = minY
        self.minZ = minZ
        self.maxX = maxX
        self.maxY = maxY
        self.maxZ = maxZ
        
        self.dirty = True
        self.level = level
        
        self.layers: Dict[int, Entity] = {}
        
    def rebuild(self, layer):
        if Chunk.REBUILT_THIS_FRAME == Chunk.MAX_REBUILDS_PER_FRAME:
            return
        
        for i, entity in self.layers.items():
            if (i == layer):
                destroy(entity)
        if layer in self.layers:
            self.layers.pop(layer)
        
        Chunk.UPDATES += 1
        Chunk.REBUILT_THIS_FRAME += 1
        Chunk.TESSELLATOR.set_texture_atlas(load_texture('res/terrain.png'))
        
        self.dirty = False
        
        Chunk.TESSELLATOR.clear()
        Chunk.TESSELLATOR.set_collider('mesh')
        
        for x in range(self.minX, self.maxX):
            for y in range(self.minY,self.maxY):
                for z in range(self.minZ, self.maxZ):
                    if (self.level.isTile(x, y, z)):
                        tileID: int = self.level.getTile(x, y, z)
                        
                        if (tileID > 0):
                            Tile.TILES[tileID].render(Chunk.TESSELLATOR, self.level, layer, x, y, z)
        
        newEntity = Chunk.TESSELLATOR.flush()
        if (newEntity):
            self.layers[layer] = newEntity
        
    def render(self, layer):
        if (self.dirty):
            self.rebuild(0)
            self.rebuild(1)     
        
    def setDirty(self):
        self.dirty = True
        