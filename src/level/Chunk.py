from src.level.tile.Tile import Tile
import src.level.TileType as TileType
from src.render.Tessellator import Tessellator
from dataclasses import dataclass, field
import numpy as np
from typing import Dict
from ursina import load_texture, Entity, destroy


@dataclass
class MeshData:
    """Класс для хранения данных сгенерированного меша."""
    # Используем массивы numpy для эффективности
    vertexBuffer: np.ndarray = field(default_factory=lambda: np.array([], dtype=np.float32))
    textureCoordBuffer: np.ndarray = field(default_factory=lambda: np.array([], dtype=np.float32))
    colorBuffer: np.ndarray = field(default_factory=lambda: np.array([], dtype=np.float32))
    
    vertices: int = 0
    hasTexture: bool = False
    hasColor: bool = False

class Chunk:
    UPDATES = 0
    REBUILT_THIS_FRAME = 0
    
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
        for i, entity in self.layers.items():
            if (i == layer):
                destroy(entity)
        if layer in self.layers:
            self.layers.pop(layer)
        
        if Chunk.REBUILT_THIS_FRAME == 2:
            return
        
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
                            # TileType.BUSH.render(Chunk.TESSELLATOR, self.level, layer, x, y, z)
                        # elif (id != -1):
                        #     TileType.STONE.render(Chunk.TESSELLATOR, self.level, layer, x, y, z)
        
        # self.cacheMeshData(layer)
        newEntity = Chunk.TESSELLATOR.flush()
        if (newEntity):
            self.layers[layer] = newEntity
        
    def render(self, layer):
        if (self.dirty):
            self.rebuild(0)
            self.rebuild(1)     
        
    def setDirty(self):
        self.dirty = True
        