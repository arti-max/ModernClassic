from src.character.Vec3 import Vec3

class Vertex:
    
    def __init__(self, *args):
        # 1. Vertex(float x, float y, float z, float u, float v)
        if len(args) == 5:
            x, y, z, u, v = args
            self.position = Vec3(x, y, z)
            self.u = float(u)
            self.v = float(v)
        
        # 2. Vertex(Vec3 position, float u, float v)
        elif len(args) == 3 and isinstance(args[0], Vec3):
            position, u, v = args
            self.position = position
            self.u = float(u)
            self.v = float(v)

        # 3. Vertex(Vertex vertex, float u, float v)
        elif len(args) == 3 and isinstance(args[0], Vertex):
            other_vertex, u, v = args
            self.position = other_vertex.position
            self.u = float(u)
            self.v = float(v)

        else:
            raise TypeError("Invalid arguments for Vertex constructor")
        
    def remap(self, u, v):
        return Vertex(self, u, v)