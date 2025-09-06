import math
from src.level.tile.Tile import Tile


class Bush(Tile):
    def __init__(self, id):
        super().__init__(id)
        
        self.textureID = 15
        
        
    def render(self, tessellator, level, layer, x, y, z):
        if (level.isLit(x, y, z) ^ layer != 1):
            return
        
        textureID: int = self.getTexture(self.textureID)
        
        
        tile_size = 1.0 / 16.0 
        
        col = textureID % 16
        row = textureID // 16
        
        minU = col * tile_size
        maxU = minU + tile_size
        minV = 1.0 - (row * tile_size) - tile_size
        maxV = 1.0 - (row * tile_size)
        
        tessellator.color(1.0, 1.0, 1.0)
        
        for i in range(2):
            rad = i * math.pi / 2.0 + math.pi / 4.0
            sin = math.sin(rad) * 0.5
            cos = math.cos(rad) * 0.5
            
            x1 = x + 0.5 - sin
            z1 = z + 0.5 - cos
            x2 = x + 0.5 + sin
            z2 = z + 0.5 + cos
            
            tessellator.vertexUV(x1, y + 1, z1, minU, maxV) 
            tessellator.vertexUV(x2, y + 1, z2, maxU, maxV)
            tessellator.vertexUV(x2, y + 0, z2, maxU, minV)
            tessellator.vertexUV(x1, y + 0, z1, minU, minV)
            
            tessellator.vertexUV(x2, y + 1, z2, maxU, maxV)
            tessellator.vertexUV(x1, y + 1, z1, minU, maxV)
            tessellator.vertexUV(x1, y + 0, z1, minU, minV)
            tessellator.vertexUV(x2, y + 0, z2, maxU, minV)
            
    def getAABB(self, x, y, z):
        return None
    
    def blocksLight(self):
        return False
    
    def isSolid(self):
        return False