import math
import random
from src.phys.AABB import AABB
import numpy as np


class Level:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        
        self.blocks = np.ones(width * height * depth, dtype=np.uint8)
        self.lightDepths = [0] * width * height
        
        for x in range(width):
            for z in range(height):
                for y in range(depth):
                   self.blocks[self.generate_index(x, y, z)] = 1 
                   
                   
        for i in range(400):
            caveSize = np.random.randint(1, 8)
            
            caveX = np.random.randint(0, width)
            caveY = np.random.randint(0, depth)
            caveZ = np.random.randint(0, height)
            
            for radius in range(1, caveSize): # Начинаем с 1
                radius_sq = radius * radius
                
                # 1. Генерируем 1000 случайных смещений за один вызов
                offsets = np.random.randint(-radius, radius + 1, size=(1000, 3))
                
                # 2. Вычисляем квадрат расстояния для всех 1000 точек сразу
                distances_sq = np.sum(np.square(offsets), axis=1)
                
                # 3. Находим только те точки, которые находятся внутри сферы
                valid_points_mask = distances_sq <= radius_sq
                valid_offsets = offsets[valid_points_mask]
                
                if valid_offsets.shape[0] == 0:
                    continue
                    
                # 4. Вычисляем абсолютные координаты всех валидных точек
                tile_coords = valid_offsets + [caveX, caveY, caveZ]
                
                # 5. Применяем фильтр по границам ко всем точкам
                in_bounds_mask = (
                    (tile_coords[:, 0] > 0) & (tile_coords[:, 0] < width - 1) &
                    (tile_coords[:, 1] > 0) & (tile_coords[:, 1] < depth) &
                    (tile_coords[:, 2] > 0) & (tile_coords[:, 2] < height - 1)
                )
                
                final_coords = tile_coords[in_bounds_mask]
                
                if final_coords.shape[0] == 0:
                    continue
                
                # 6. Вычисляем индексы для всех финальных точек за один раз
                indices_float = (final_coords[:, 0] + 
                final_coords[:, 1] * width + 
                final_coords[:, 2] * width * depth)
                
                indices = indices_float.astype(np.int64)
                
                # 7. Обнуляем все нужные блоки одной командой
                self.blocks[indices] = 0
                   
        self.calcLightDepths(0, 0, width, height)
                    
    def generate_index(self, x, y, z):
        return x + y * self.width + z * self.width * self.depth
    
    def calcLightDepths(self, minX, minZ, maxX, maxZ):
        for x in range(minX, maxX):
            for z in range(minZ, maxZ):
                prevData = self.lightDepths[x + z * self.width]
                
                depth = self.depth - 1
                while (depth > 0 and not self.isLightBlocker(x, depth, z)):
                    depth -= 1
                    
                    
                self.lightDepths[x + z * self.width] = depth
            
    def isSolidTile(self, x, y, z):
        return self.isTile(x, y, z)
    
    def isTile(self, x, y, z):
        if (x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height):
            return False
        
        # print(x, y, z)
        
        return self.blocks[self.generate_index(x, y, z)] != 0
    
    def isLightBlocker(self, x, y, z):
        return self.isSolidTile(x, y, z)
    
    def getBrightness(self, x, y, z):
        dark = 0.5
        light = 1.0
        
        if (x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height):
            return light
        
        if (y < self.lightDepths[x + z * self.width]):
            return dark
        
        return light    # Unknown bright
    
    def isLit(self, x, y, z):
        return (x < 0 or y < 0 or z < 0 or x >= self.width or z >= self.height or y >= self.lightDepths[x + z * self.width])
    
    def getCubes(self, boundingBox: AABB) -> list[AABB]:
        boundingBoxList: list[AABB] = []
        
        minX: int = int(math.floor(boundingBox.min_x) - 1)
        maxX: int = int(math.ceil(boundingBox.max_x) + 1)
        minY: int = int(math.floor(boundingBox.min_y) - 1)
        maxY: int = int(math.ceil(boundingBox.max_y) + 1)
        minZ: int = int(math.floor(boundingBox.min_z) - 1)
        maxZ: int = int(math.ceil(boundingBox.max_z) + 1)
        
        minX = max(0, minX)
        minY = max(0, minY)
        minZ = max(0, minZ)
        
        maxX = min(self.width, maxX)
        maxY = min(self.depth, maxY)
        maxZ = min(self.height, maxZ)
        
        for x in range(minX, maxX):
            for y in range(minY, maxY):
                for z in range(minZ, maxZ):
                    if (self.isSolidTile(x, y, z)):
                        boundingBoxList.append(AABB(x, y, z, x+1, y+1, z+1))
                        
        return boundingBoxList