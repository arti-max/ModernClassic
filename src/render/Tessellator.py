import numpy as np
from ursina import *
from ursina.shaders import unlit_shader

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
        
        self.collider=None
        
        self.matrix_stack = [np.identity(4)]
        
        self.clear()
        
    def set_texture_atlas(self, texture):
        self.atlas = texture
        
    def set_collider(self, collider):
        self.collider = collider
        
    def push_matrix(self):
        self.matrix_stack.append(np.copy(self.matrix_stack[-1]))
        
    def pop_matrix(self):
        if len(self.matrix_stack) > 1:
            self.matrix_stack.pop()

    def translate(self, x, y, z):
        translation_matrix = np.array([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ], dtype=float)
        
        self.matrix_stack[-1] = translation_matrix @ self.matrix_stack[-1]
        
    def rotate(self, angle_deg, x, y, z):
        if angle_deg == 0: return
        angle_rad = np.radians(angle_deg)
        c, s = np.cos(angle_rad), np.sin(angle_rad)
        axis = np.array([x, y, z], dtype=float)
        axis = axis / np.linalg.norm(axis)
        ux, uy, uz = axis
        rot_matrix = np.array([
            [c + ux*ux*(1-c),   ux*uy*(1-c) - uz*s, ux*uz*(1-c) + uy*s, 0],
            [uy*ux*(1-c) + uz*s, c + uy*uy*(1-c),   uy*uz*(1-c) - ux*s, 0],
            [uz*ux*(1-c) - uy*s, uz*uy*(1-c) + ux*s, c + uz*uz*(1-c),   0],
            [0, 0, 0, 1]
        ])
        self.matrix_stack[-1] = rot_matrix @ self.matrix_stack[-1]
        
    def scale(self, x, y, z):
        scale_matrix = np.array([
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1]
        ], dtype=float)
        self.matrix_stack[-1] = scale_matrix @ self.matrix_stack[-1]
        
    def vertex(self, x, y, z):
        vec4 = np.array([x, y, z, 1.0])
        transformed_vec = self.matrix_stack[-1] @ vec4
        tx, ty, tz = transformed_vec[0], transformed_vec[1], transformed_vec[2]
        
        self.vertexBuffer.append((tx, ty, tz))
        if self.hasTexture: self.textureCoordBuffer.append((self.textureU, self.textureV))
        if self.hasColor: self.colorBuffer.append(color.rgba(self.r, self.g, self.b, 1))
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
        if not self.vertexBuffer:
            return None
        
        triangles = []
        
        for i in range(0, self.vertices, 4):
            triangles.extend([i, i + 1, i + 2, i, i + 2, i + 3])
        entity = Entity(
            model=Mesh(
                vertices=list(self.vertexBuffer),
                triangles=triangles,
                uvs=list(self.textureCoordBuffer) if self.hasTexture else None,
                colors=list(self.colorBuffer) if self.hasColor else None,
            ),
            texture=self.atlas,
            collider=self.collider
        )
        self.clear()
        return entity
    
    def flush_lines(self):
        if not self.vertexBuffer:
            return None
        
        entity = Entity(
            model=Mesh(
                vertices=list(self.vertexBuffer),
                mode='line'
            )
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
        
        self.collider=None
        
        self.matrix_stack = [np.identity(4)]
        