from src.render.Tessellator import Tessellator
from src.level.Chunk import Chunk

CHUNK_SIZE = 16

class LevelRenderer:
    def __init__(self, level):
        self.level = level
        
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
                    self.chunks[(x + y * self.chunkAmountX) * self.chunkAmountZ + z] = chunk
                    
                    
    def render(self, layer):
        
        Chunk.REBUILT_THIS_FRAME = 0
        
        for chunk in self.chunks:
            if chunk:
                chunk.render(layer)
        