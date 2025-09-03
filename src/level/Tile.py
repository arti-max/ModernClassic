


class Tile:
    
    def __init__(self, textureID):
        self.textureID = textureID
        
    
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
    
    def renderFace(self, tessellator, x, y, z, face):
        minU = self.textureID / 16.0;
        maxU = minU + 16 / 256;
        maxV = 1.0; # Верхний край текстуры
        minV = maxV - (16 / 256); # Отступаем вниз на высоту тайла
        
        minX = x + 0.0;
        maxX = x + 1.0;
        minY = y + 0.0;
        maxY = y + 1.0;
        minZ = z + 0.0;
        maxZ = z + 1.0;
        
        # Y-
        if face == 0:
            tessellator.vertexUV(minX, minY, maxZ, minU, maxV)
            tessellator.vertexUV(maxX, minY, maxZ, maxU, maxV)
            tessellator.vertexUV(maxX, minY, minZ, maxU, minV)
            tessellator.vertexUV(minX, minY, minZ, minU, minV)
                
        # Y+
        if face == 1:
            tessellator.vertexUV(maxX, maxY, maxZ, maxU, maxV)
            tessellator.vertexUV(minX, maxY, maxZ, minU, maxV)
            tessellator.vertexUV(minX, maxY, minZ, minU, minV)
            tessellator.vertexUV(maxX, maxY, minZ, maxU, minV)
                
        # Z-
        if face == 2:
            tessellator.vertexUV(minX, maxY, minZ, maxU, minV)
            tessellator.vertexUV(minX, minY, minZ, maxU, maxV)
            tessellator.vertexUV(maxX, minY, minZ, minU, maxV)
            tessellator.vertexUV(maxX, maxY, minZ, minU, minV)
                
        # Z+
        if face == 3:
            tessellator.vertexUV(minX, maxY, maxZ, minU, minV)
            tessellator.vertexUV(maxX, maxY, maxZ, maxU, minV)
            tessellator.vertexUV(maxX, minY, maxZ, maxU, maxV)
            tessellator.vertexUV(minX, minY, maxZ, minU, maxV)
                
        # X-
        if face == 4:
            tessellator.vertexUV(minX, maxY, maxZ, maxU, minV)
            tessellator.vertexUV(minX, minY, maxZ, maxU, maxV)
            tessellator.vertexUV(minX, minY, minZ, minU, maxV)
            tessellator.vertexUV(minX, maxY, minZ, minU, minV)
                
        # X+
        if face == 5:
            tessellator.vertexUV(maxX, minY, maxZ, maxU, maxV)
            tessellator.vertexUV(maxX, maxY, maxZ, maxU, minV)
            tessellator.vertexUV(maxX, maxY, minZ, minU, minV)
            tessellator.vertexUV(maxX, minY, minZ, minU, maxV)