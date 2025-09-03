from src.render.Tessellator import Tessellator
from src.level.Chunk import Chunk
from src.level.LeveListener import LevelListener
from src.HitResult import HitResult
import src.level.TileType as TileType
from ursina import destroy, Vec3
import math
import time

CHUNK_SIZE = 16

class LevelRenderer(LevelListener):
    
    def __init__(self, level):
        level.addListener(self)
        
        self.level = level
        
        self.tessellator = Tessellator()
        
        self.hit_entity = None
        
        self.chunkAmountX = level.width // CHUNK_SIZE
        self.chunkAmountY = level.depth // CHUNK_SIZE
        self.chunkAmountZ = level.height // CHUNK_SIZE
        
        self.chunks = [0] * (self.chunkAmountX * self.chunkAmountY * self.chunkAmountZ)
        
        for x in range(0, self.chunkAmountX):
            for y in range(0, self.chunkAmountY):
                for z in range(0, self.chunkAmountZ):
                    # Calculate min bounds for chunk
                    minChunkX = x * CHUNK_SIZE
                    minChunkY = y * CHUNK_SIZE
                    minChunkZ = z * CHUNK_SIZE

                    # Calculate max bounds for chunk
                    maxChunkX = (x + 1) * CHUNK_SIZE
                    maxChunkY = (y + 1) * CHUNK_SIZE
                    maxChunkZ = (z + 1) * CHUNK_SIZE

                    # Check for chunk bounds out of level
                    maxChunkX = min(level.width, maxChunkX)
                    maxChunkY = min(level.depth, maxChunkY)
                    maxChunkZ = min(level.height, maxChunkZ)
                    
                    chunk = Chunk(level, minChunkX, minChunkY, minChunkZ, maxChunkX, maxChunkY, maxChunkZ)
                    
                    index = x + z * self.chunkAmountX + y * self.chunkAmountX * self.chunkAmountZ
                    
                    self.chunks[index] = chunk
                    
                    
    def render(self, layer):
        
        Chunk.REBUILT_THIS_FRAME = 0
        
        for chunk in self.chunks:
            if chunk:
                chunk.render(layer)
                
                
    def setDirty(self, minX, minY, minZ, maxX, maxY, maxZ):
        
        minX /= CHUNK_SIZE
        minY /= CHUNK_SIZE
        minZ /= CHUNK_SIZE
        maxX /= CHUNK_SIZE
        maxY /= CHUNK_SIZE
        maxZ /= CHUNK_SIZE
        
        minX = math.floor(max(minX, 0))
        minY = math.floor(max(minY, 0))
        minZ = math.floor(max(minZ, 0))
        
        maxX = math.floor(min(maxX, self.chunkAmountX - 1))
        maxY = math.floor(min(maxY, self.chunkAmountY - 1))
        maxZ = math.floor(min(maxZ, self.chunkAmountZ - 1))
        
        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                for z in range(minZ, maxZ + 1):
                    index = x + z * self.chunkAmountX + y * self.chunkAmountX * self.chunkAmountZ
                    
                    if (0 <= index < len(self.chunks)):
                        chunk = self.chunks[index]
                        if chunk:
                            chunk.setDirty()
                    
                    
    def renderHit(self, hitResult: HitResult):
        if self.hit_entity:
            destroy(self.hit_entity)
            self.hit_entity = None
            
        if hitResult is None:
            return

        alpha = math.sin(time.time() * 10) * 0.2 + 0.4

        offset_vec = Vec3(0,0,0)
        offset_amount = 0.002
        
        face = hitResult.face
        if face == 0: offset_vec.y = -offset_amount  # Y-
        elif face == 1: offset_vec.y = offset_amount   # Y+
        elif face == 2: offset_vec.z = -offset_amount  # Z-
        elif face == 3: offset_vec.z = offset_amount   # Z+
        elif face == 4: offset_vec.x = -offset_amount  # X-
        elif face == 5: offset_vec.x = offset_amount   # X+
        
        x = hitResult.x + offset_vec.x
        y = hitResult.y + offset_vec.y
        z = hitResult.z + offset_vec.z
        
        self.tessellator.clear()
        TileType.STONE.renderFace(self.tessellator, x, y, z, hitResult.face)

        self.hit_entity = self.tessellator.flush()
        
        if self.hit_entity:
            self.hit_entity.unlit = True
            
            self.hit_entity.color = (1, 1, 1, alpha)
            
                    
    def tileChanged(self, x, y, z):
        self.setDirty(x - 1, y - 1, z - 1, x + 1, y + 1, z + 1)
        
    def lightColumnChanged(self, x, z, minY, maxY):
        self.setDirty(x - 1, minY - 1, z - 1, x + 1, maxY + 1, z + 1)
        
    def allChanged(self):
        self.setDirty(0, 0, 0, self.level.width, self.level.depth, self.level.height)
                    
                    
        