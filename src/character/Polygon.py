from src.character.Vertex import Vertex
from src.render.Texture import BINDED_TEXTURE
from ursina import Mesh, Entity

class Polygon:
    def __init__(self, *args):
        
        if len(args) == 1 and isinstance(args[0], list):
            vertices: list[Vertex] = args[0]
            self.vertices = vertices
            self.vertexCount = len(vertices)
        elif len(args) == 5:
            vertices, minU, minV, maxU, maxV = args
            
            self.vertices: list[Vertex] = vertices
            self.vertexCount = len(vertices)
            
            self.vertices[0] = vertices[0].remap(maxU, minV)
            self.vertices[1] = vertices[1].remap(minU, minV)
            self.vertices[2] = vertices[2].remap(minU, maxV)
            self.vertices[3] = vertices[3].remap(maxU, maxV)
            
    def render(self, tessellator):
        for vertex in reversed(self.vertices):
            tessellator.vertexUV(
                vertex.position.x, vertex.position.y, vertex.position.z,
                vertex.u / 64.0, vertex.v / 32.0
            )