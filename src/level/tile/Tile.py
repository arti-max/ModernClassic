from src.phys.AABB import AABB


class Tile:
    
    TILES = [0] * 256
    
    def __init__(self, id, textureId=None):
        self.id = id
        
        if textureId != None:
            self.textureID = textureId
        
        Tile.TILES[id] = self
        
    
    def render(self, tessellator, level, layer, x, y, z):
        shadeX: float = 0.6
        shadeY: float = 1.0
        shadeZ: float = 0.8
        
        
        if (self.shouldRenderFace(level, x, y - 1, z, layer)):
            brightness = level.getBrightness(x, y-1, z) * shadeY
            tessellator.color(brightness, brightness, brightness)
            self.renderFace(tessellator, x, y, z, 0)
            
        if (self.shouldRenderFace(level, x, y + 1, z, layer)):
            brightness = level.getBrightness(x, y+1, z) * shadeY
            tessellator.color(brightness, brightness, brightness)
            self.renderFace(tessellator, x, y, z, 1)
            
        if (self.shouldRenderFace(level, x, y, z - 1, layer)):
            brightness = level.getBrightness(x, y, z-1) * shadeZ
            tessellator.color(brightness, brightness, brightness)
            self.renderFace(tessellator, x, y, z, 2)
            
        if (self.shouldRenderFace(level, x, y, z + 1, layer)):
            brightness = level.getBrightness(x, y, z+1) * shadeZ
            tessellator.color(brightness, brightness, brightness)
            self.renderFace(tessellator, x, y, z, 3)
            
        if (self.shouldRenderFace(level, x - 1, y, z, layer)):
            brightness = level.getBrightness(x-1, y, z) * shadeX
            tessellator.color(brightness, brightness, brightness)
            self.renderFace(tessellator, x, y, z, 4)
            
        if (self.shouldRenderFace(level, x + 1, y, z, layer)):
            brightness = level.getBrightness(x+1, y, z) * shadeX
            tessellator.color(brightness, brightness, brightness)
            self.renderFace(tessellator, x, y, z, 5)
        
        
    def shouldRenderFace(self, level, x, y, z, layer):
        return not level.isSolidTile(x, y, z) and (level.isLit(x, y, z) ^ layer == 1)
    
    def getTexture(self, face):
        return self.textureID
    
    def renderFace(self, tessellator, x, y, z, face):
        textureID: int = self.getTexture(face)
        
        tile_size = 1.0 / 16.0 
        
        col = textureID % 16
        row = textureID // 16
        
        minU = col * tile_size
        maxU = minU + tile_size
        
        minV = 1.0 - (row * tile_size) - tile_size
        maxV = 1.0 - (row * tile_size)

        
        minX = x + 0.0
        maxX = x + 1.0
        minY = y + 0.0
        maxY = y + 1.0
        minZ = z + 0.0
        maxZ = z + 1.0
        
        # Y-
        if face == 0:
            tessellator.vertexUV(minX, minY, minZ, minU, minV)
            tessellator.vertexUV(minX, minY, maxZ, minU, maxV)
            tessellator.vertexUV(maxX, minY, maxZ, maxU, maxV)
            tessellator.vertexUV(maxX, minY, minZ, maxU, minV)
        # Y+ 
        if face == 1:
            tessellator.vertexUV(minX, maxY, maxZ, minU, maxV)
            tessellator.vertexUV(minX, maxY, minZ, minU, minV)
            tessellator.vertexUV(maxX, maxY, minZ, maxU, minV)
            tessellator.vertexUV(maxX, maxY, maxZ, maxU, maxV)
        # Z- 
        if face == 2:
            tessellator.vertexUV(minX, minY, minZ, maxU, minV)
            tessellator.vertexUV(maxX, minY, minZ, minU, minV)
            tessellator.vertexUV(maxX, maxY, minZ, minU, maxV)
            tessellator.vertexUV(minX, maxY, minZ, maxU, maxV)
        # Z+ 
        if face == 3:
            tessellator.vertexUV(maxX, minY, maxZ, maxU, minV)
            tessellator.vertexUV(minX, minY, maxZ, minU, minV)
            tessellator.vertexUV(minX, maxY, maxZ, minU, maxV)
            tessellator.vertexUV(maxX, maxY, maxZ, maxU, maxV)
        # X- 
        if face == 4:
            tessellator.vertexUV(minX, minY, maxZ, maxU, minV)
            tessellator.vertexUV(minX, minY, minZ, minU, minV)
            tessellator.vertexUV(minX, maxY, minZ, minU, maxV)
            tessellator.vertexUV(minX, maxY, maxZ, maxU, maxV)
        # X+ 
        if face == 5:
            tessellator.vertexUV(maxX, minY, minZ, maxU, minV)
            tessellator.vertexUV(maxX, minY, maxZ, minU, minV)
            tessellator.vertexUV(maxX, maxY, maxZ, minU, maxV)
            tessellator.vertexUV(maxX, maxY, minZ, maxU, maxV)
            
    def getAABB(self, x, y, z):
        return AABB(x, y, z, x + 1, y + 1, z + 1)
    
    def blocksLight(self):
        return True
    
    def isSolid(self):
        return True
    
    def onTick(self, level, x, y, z):
        pass