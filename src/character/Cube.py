from ursina import Entity, Mesh
from src.character.Polygon import Polygon
from src.character.Vertex import Vertex
from src.render.Texture import BINDED_TEXTURE

class Cube:
    
    def __init__(self, textureOffsetX: int, textureOffsetY: int):
        self.textureOffsetX = textureOffsetX
        self.textureOffsetY = textureOffsetY
        self.polygons: list[Polygon] = []
        
        self.x = 0
        self.y = 0
        self.z = 0
        self.xRotation = 0
        self.yRotation = 0
        self.zRotation = 0
        
    def setTextureOffset(self, textureOffsetX: int, textureOffsetY: int):
        self.textureOffsetX = textureOffsetX
        self.textureOffsetY = textureOffsetY
        
    def addBox(self, offsetX, offsetY, offsetZ, width, height, depth):
        self.polygons = [None] * 6
        x1, y1, z1 = offsetX, offsetY, offsetZ
        x2, y2, z2 = offsetX + width, offsetY + height, offsetZ + depth
        
        v_bottom1 = Vertex(x1, y1, z1, 0.0, 0.0)
        v_bottom2 = Vertex(x2, y1, z1, 0.0, 8.0)
        v_bottom3 = Vertex(x1, y1, z2, 0.0, 0.0)
        v_bottom4 = Vertex(x2, y1, z2, 0.0, 8.0)
        
        v_top1 = Vertex(x2, y2, z2, 8.0, 8.0)
        v_top2 = Vertex(x1, y2, z2, 8.0, 0.0)
        v_top3 = Vertex(x2, y2, z1, 8.0, 8.0)
        v_top4 = Vertex(x1, y2, z1, 8.0, 0.0)

        self.polygons[0] = Polygon([v_bottom4, v_bottom2, v_top3, v_top1], self.textureOffsetX + depth + width, self.textureOffsetY + depth, self.textureOffsetX + depth + width + depth, self.textureOffsetY + depth + height)
        self.polygons[1] = Polygon([v_bottom1, v_bottom3, v_top2, v_top4], self.textureOffsetX, self.textureOffsetY + depth, self.textureOffsetX + depth, self.textureOffsetY + depth + height)
        self.polygons[2] = Polygon([v_bottom4, v_bottom3, v_bottom1, v_bottom2], self.textureOffsetX + depth, self.textureOffsetY, self.textureOffsetX + depth + width, self.textureOffsetY + depth)
        self.polygons[3] = Polygon([v_top3, v_top4, v_top2, v_top1], self.textureOffsetX + depth + width, self.textureOffsetY, self.textureOffsetX + depth + width + width, self.textureOffsetY + depth)
        self.polygons[4] = Polygon([v_bottom2, v_bottom1, v_top4, v_top3], self.textureOffsetX + depth, self.textureOffsetY + depth, self.textureOffsetX + depth + width, self.textureOffsetY + depth + height)
        self.polygons[5] = Polygon([v_bottom3, v_bottom4, v_top1, v_top2], self.textureOffsetX + depth + width + depth, self.textureOffsetY + depth, self.textureOffsetX + depth + width + depth + width, self.textureOffsetY + depth + height)
        
        return self
    
    
    def setPosition(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def render(self, tessellator):
        tessellator.push_matrix()
        tessellator.translate(self.x, self.y, self.z)
        
        if self.zRotation != 0: tessellator.rotate(self.zRotation, 0, 0, 1)
        if self.yRotation != 0: tessellator.rotate(self.yRotation, 0, 1, 0)
        if self.xRotation != 0: tessellator.rotate(self.xRotation, 1, 0, 0)
        
        for polygon in self.polygons:
            polygon.render(tessellator)
            
        tessellator.pop_matrix()
        
        
        