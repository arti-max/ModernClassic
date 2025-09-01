


class Tile:
    
    def __init__(self, textureID):
        self.textureID = textureID
        
        
    def render(self, tessellator, level, layer, x, y, z):
        minU = self.textureID / 16.0;
        maxU = minU + 16 / 256;
        maxV = 1.0; # Верхний край текстуры
        minV = maxV - (16 / 256); # Отступаем вниз на высоту тайла
        
        shadeX = 0.6
        shadeY = 1.0
        shadeZ = 0.8
        
        minX = x + 0.0;
        maxX = x + 1.0;
        minY = y + 0.0;
        maxY = y + 1.0;
        minZ = z + 0.0;
        maxZ = z + 1.0;
        
        # Y-
        if (not level.isSolidTile(x, y-1, z)):
            
            brightness = level.getBrightness(x, y - 1, z) * shadeY
            
            if ((layer == 1) ^ (brightness == shadeY)):
                tessellator.color(brightness, brightness, brightness)
                tessellator.vertexUV(minX, minY, maxZ, minU, maxV)
                tessellator.vertexUV(maxX, minY, maxZ, maxU, maxV)
                tessellator.vertexUV(maxX, minY, minZ, maxU, minV)
                tessellator.vertexUV(minX, minY, minZ, minU, minV)
                
        # Y+
        if (not level.isSolidTile(x, y+1, z)):
            brightness = level.getBrightness(x, y + 1, z) * shadeY
            
            if ((layer == 1) ^ (brightness == shadeY)):
                tessellator.color(brightness, brightness, brightness)
                tessellator.vertexUV(maxX, maxY, maxZ, maxU, maxV)
                tessellator.vertexUV(minX, maxY, maxZ, minU, maxV)
                tessellator.vertexUV(minX, maxY, minZ, minU, minV)
                tessellator.vertexUV(maxX, maxY, minZ, maxU, minV)
                
        # Z-
        if (not level.isSolidTile(x, y, z-1)):
            brightness = level.getBrightness(x, y, z - 1) * shadeZ
            
            if ((layer == 1) ^ (brightness == shadeZ)):
                tessellator.color(brightness, brightness, brightness)
                tessellator.vertexUV(minX, maxY, minZ, maxU, minV)
                tessellator.vertexUV(minX, minY, minZ, maxU, maxV)
                tessellator.vertexUV(maxX, minY, minZ, minU, maxV)
                tessellator.vertexUV(maxX, maxY, minZ, minU, minV)
                
        # Z+
        if (not level.isSolidTile(x, y, z + 1)):
            brightness = level.getBrightness(x, y, z + 1) * shadeZ
            
            if ((layer == 1) ^ (brightness == shadeZ)):
                tessellator.color(brightness, brightness, brightness)
                tessellator.vertexUV(minX, maxY, maxZ, minU, minV)
                tessellator.vertexUV(maxX, maxY, maxZ, maxU, minV)
                tessellator.vertexUV(maxX, minY, maxZ, maxU, maxV)
                tessellator.vertexUV(minX, minY, maxZ, minU, maxV)
                
        # X-
        if (not level.isSolidTile(x - 1, y, z)):
            brightness = level.getBrightness(x - 1, y, z) * shadeX
            
            if ((layer == 1) ^ (brightness == shadeX)):
                tessellator.color(brightness, brightness, brightness)
                tessellator.vertexUV(minX, maxY, maxZ, maxU, minV)
                tessellator.vertexUV(minX, minY, maxZ, maxU, maxV)
                tessellator.vertexUV(minX, minY, minZ, minU, maxV)
                tessellator.vertexUV(minX, maxY, minZ, minU, minV)
                
        # X+
        if (not level.isSolidTile(x + 1, y, z)):
            brightness = level.getBrightness(x + 1, y, z) * shadeX
            
            if ((layer == 1) ^ (brightness == shadeX)):
                tessellator.color(brightness, brightness, brightness)
                tessellator.vertexUV(maxX, minY, maxZ, maxU, maxV)
                tessellator.vertexUV(maxX, maxY, maxZ, maxU, minV)
                tessellator.vertexUV(maxX, maxY, minZ, minU, minV)
                tessellator.vertexUV(maxX, minY, minZ, minU, maxV)