from src.level.Tile import Tile
from src.level.TileTypes import TileType
from src.render.Tessellator import Tessellator
from dataclasses import dataclass, field
import numpy as np
from typing import Dict
from ursina import load_texture


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
        
        self.mesh_cache: Dict[int, MeshData] = {}
        
    def rebuild(self, layer):
        if (Chunk.REBUILT_THIS_FRAME == 2):
            return
        
        Chunk.UPDATES += 1
        Chunk.REBUILT_THIS_FRAME += 1
        Chunk.TESSELLATOR.set_texture_atlas(load_texture('res/terrain.png'))
        
        self.dirty = False
        
        Chunk.TESSELLATOR.clear()
        
        for x in range(self.minX, self.maxX):
            for y in range(self.minY,self.maxY):
                for z in range(self.minZ, self.maxZ):
                    if (self.level.isTile(x, y, z)):
                        
                        if (y > self.level.depth - 7 and self.level.getBrightness(x, y, z) == 1.0):
                            Tile(TileType.GRASS).render(Chunk.TESSELLATOR, self.level, layer, x, y, z)
                        else:
                            Tile(TileType.STONE).render(Chunk.TESSELLATOR, self.level, layer, x, y, z)
        
        self.cacheMeshData(layer)
        Chunk.TESSELLATOR.flush()
        
    def cacheMeshData(self, layer):
        self.mesh_cache[layer] = MeshData(
            vertexBuffer=Chunk.TESSELLATOR.vertexBuffer,
            textureCoordBuffer=Chunk.TESSELLATOR.textureCoordBuffer,
            colorBuffer=Chunk.TESSELLATOR.colorBuffer,
            vertices=Chunk.TESSELLATOR.vertices,
            hasColor=Chunk.TESSELLATOR.hasColor,
            hasTexture=Chunk.TESSELLATOR.hasTexture
        )
        
    def render(self, layer):
        if (self.dirty):
            self.rebuild(0)
            self.rebuild(1)
            
        self.renderCachedMesh(layer)
            
    def renderCachedMesh(self, layer):
        cached = self.mesh_cache.get(layer, None)
        if (not cached or len(cached.vertexBuffer) == 0):
            return
        
        
        # print(f"cache")
        Chunk.TESSELLATOR.clear()
        
        Chunk.TESSELLATOR.set_texture_atlas(load_texture('res/terrain.png'))
        
        
        Chunk.TESSELLATOR.vertexBuffer=cached.vertexBuffer
        Chunk.TESSELLATOR.colorBuffer=cached.colorBuffer
        Chunk.TESSELLATOR.textureCoordBuffer=cached.textureCoordBuffer
        Chunk.TESSELLATOR.vertices=cached.vertices
        Chunk.TESSELLATOR.hasColor=cached.hasColor
        Chunk.TESSELLATOR.hasTexture=cached.hasTexture
        
        Chunk.TESSELLATOR.flush()
        