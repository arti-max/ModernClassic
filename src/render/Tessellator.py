from ursina import *

class Tessellator:
    
    MAX_VERTICES = 100000
    
    def __init__(self):
        self.atlas = None
        
        self.vertexBuffer = []
        self.textureCoordBuffer = []
        self.colorBuffer = []
        
        self.vertices = 0
        
        self.hasTexture = False
        self.textureU = 0.0
        self.textureV = 0.0
        
        self.hasColor = False
        self.r = 1
        self.g = 1
        self.b = 1
        
        self.clear()
        
    def set_texture_atlas(self, texture):
        self.atlas = texture
        
    def vertex(self, x, y, z):
        self.vertexBuffer.append((x, y, z))
        
        if (self.hasTexture):
            self.textureCoordBuffer.append((self.textureU, self.textureV))
            
        if (self.hasColor):
            self.colorBuffer.append(color.rgba(self.r * 255, self.g * 255, self.b * 255, 255))
        
        self.vertices += 1
        
        if (self.vertices == Tessellator.MAX_VERTICES):
            self.flush()
            
    def vertexUV(self, x, y, z, u, v):
        self.texture(u, v)
        self.vertex(x, y, z)
            
    def texture(self, u, v):
        self.hasTexture = True
        self.textureU = u
        self.textureV = v
        
    def color(self, r, g, b):
        self.hasColor = True
        self.r = r
        self.g = g
        self.b = b
            
    def flush(self):
        # print(f"Tessellator Flush! Vertices: {self.vertices}, Quads: {self.vertices // 4}, vertexes: {len(self.vertexBuffer)}")
        
        if not self.vertexBuffer:
            # print("Предупреждение: Попытка отрисовки без вершин.")
            return None
        

        triangles = []
        for i in range(0, self.vertices, 4):

            triangles.extend([i, i + 1, i + 2, i, i + 2, i + 3])
        

        entity = Entity(
            model=Mesh(
                vertices=self.vertexBuffer,
                triangles=triangles,
                uvs=self.textureCoordBuffer if self.hasTexture else None,
                colors=self.colorBuffer if self.hasColor else None,
            ),
            texture=self.atlas
        )
        
        self.clear()
        
        return entity
    
        
    def clear(self):
        self.vertexBuffer.clear()
        self.textureCoordBuffer.clear()
        self.colorBuffer.clear()
        self.vertices = 0
        
        self.hasColor = False
        self.hasTexture = False
        
       
        
if __name__ == "__main__":
    app = Ursina()
    
    tessellator = Tessellator()
    
    def render_cube(tessellator, x, y, z, textureId):
        minU = textureId / 16.0;
        maxU = minU + 16 / 256;
        minV = 0.0;
        maxV = minV + 16 / 256;
        
        minX = x + 0.0;
        maxX = x + 1.0;
        minY = y + 0.0;
        maxY = y + 1.0;
        minZ = z + 0.0;
        maxZ = z + 1.0;
        
        # Нижняя грань (-Y)
        tessellator.vertexUV(minX, minY, maxZ, minU, maxV)
        tessellator.vertexUV(maxX, minY, maxZ, maxU, maxV)
        tessellator.vertexUV(maxX, minY, minZ, maxU, minV)
        tessellator.vertexUV(minX, minY, minZ, minU, minV)

        # Верхняя грань (+Y)
        tessellator.vertexUV(maxX, maxY, maxZ, maxU, maxV)
        tessellator.vertexUV(minX, maxY, maxZ, minU, maxV)
        tessellator.vertexUV(minX, maxY, minZ, minU, minV)
        tessellator.vertexUV(maxX, maxY, minZ, maxU, minV)

        # Задняя грань (-Z)
        tessellator.vertexUV(minX, maxY, minZ, maxU, minV)
        tessellator.vertexUV(minX, minY, minZ, maxU, maxV)
        tessellator.vertexUV(maxX, minY, minZ, minU, maxV)
        tessellator.vertexUV(maxX, maxY, minZ, minU, minV)

        # Передняя грань (+Z)
        tessellator.vertexUV(minX, maxY, maxZ, minU, minV)
        tessellator.vertexUV(maxX, maxY, maxZ, maxU, minV)
        tessellator.vertexUV(maxX, minY, maxZ, maxU, maxV)
        tessellator.vertexUV(minX, minY, maxZ, minU, maxV)
        
        # Левая грань (-X)
        tessellator.vertexUV(minX, maxY, maxZ, maxU, minV)
        tessellator.vertexUV(minX, minY, maxZ, maxU, maxV)
        tessellator.vertexUV(minX, minY, minZ, minU, maxV)
        tessellator.vertexUV(minX, maxY, minZ, minU, minV)

        # Правая грань (+X)
        tessellator.vertexUV(maxX, minY, maxZ, maxU, maxV)
        tessellator.vertexUV(maxX, maxY, maxZ, maxU, minV)
        tessellator.vertexUV(maxX, maxY, minZ, minU, minV)
        tessellator.vertexUV(maxX, minY, minZ, minU, maxV)
        

    render_cube(tessellator, 0, 0, 0, 0)
    
    combined_entity = tessellator.flush(texture='res/terrain.png')

    EditorCamera()
    
    app.run()