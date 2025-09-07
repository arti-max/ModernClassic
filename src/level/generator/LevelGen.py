# src/level/generator/LevelGen.py
import math
import random
import time
from src.level.LevelLoaderListener import LevelLoaderListener
from src.level.generator.NoiseFilter import NoiseFilter
import src.level.TileType as TileType
import numpy as np

class LevelGen:
    def __init__(self, levelLoaderListener: LevelLoaderListener):
        self.levelLoaderListener = levelLoaderListener
        self.width = 0
        self.height = 0
        self.depth = 0
        self.blocks = None
        self.random = random.Random()
        
        self.current_step = 0
        self.is_generating = False
        self.sub_progress = 0
        self.sub_total = 0
    
    def generateLevel(self, level, user_name: str, width: int, height: int, depth: int):
        self.levelLoaderListener.beginLevelLoading("Generating level")
        
        self.width = width
        self.height = height 
        self.depth = depth
        self.blocks = np.zeros(width * height * depth, dtype=np.uint8)
        
        self.level = level
        self.user_name = user_name
        self.preparation_steps = [
            ("Raising...", self._prepare_height_map),
            ("Building terrain...", self._prepare_terrain_build),
            ("Carving caves...", self._prepare_cave_carving),
            ("Finalizing...", self._finalize_level),
        ]
        
        self.current_step = 0
        self.is_generating = True
        self.sub_progress = 0
        
        step_name, _ = self.preparation_steps[self.current_step]
        self.levelLoaderListener.levelLoadUpdate(step_name)
    
    def _continue_generation(self):
        if not self.is_generating or self.current_step >= len(self.preparation_steps):
            return False
        
        step_name, step_function = self.preparation_steps[self.current_step]
        
        completed = step_function()
        
        if completed:
            self.current_step += 1
            self.sub_progress = 0
            
            if self.current_step < len(self.preparation_steps):
                step_name, _ = self.preparation_steps[self.current_step]
                self.levelLoaderListener.levelLoadUpdate(step_name)
            else:
                self.is_generating = False
                self.levelLoaderListener.levelLoadComplete()
                return True
        
        return False
    
    def _prepare_height_map(self):
        BATCH_SIZE = 256
        
        if self.sub_progress == 0:
            self.noise_generator = NoiseFilter(seed=random.randint(0, 12345))
            self.height_map = [[0 for _ in range(self.height)] for _ in range(self.width)]
            self.sub_total = self.width * self.height
        
        start_idx = self.sub_progress
        end_idx = min(start_idx + BATCH_SIZE, self.sub_total)
        
        for i in range(start_idx, end_idx):
            x = i // self.height
            z = i % self.height
            
            noise_value = self.noise_generator.get_noise(x, z)
            base_height = self.depth // 2
            variation = 16
            self.height_map[x][z] = int(base_height + noise_value * variation)
        
        self.sub_progress = end_idx
        
        progress = (self.sub_progress / self.sub_total) * 100
        self.levelLoaderListener.levelLoadUpdate(f"Raising... {int(progress)}%")
        
        return self.sub_progress >= self.sub_total
    
    def _prepare_terrain_build(self):
        BATCH_SIZE = 6000
        
        if self.sub_progress == 0:
            self.sub_total = self.width * self.height * self.depth
        
        start_idx = self.sub_progress
        end_idx = min(start_idx + BATCH_SIZE, self.sub_total)
        
        for i in range(start_idx, end_idx):
            x = i % self.width
            y = (i // self.width) % self.depth
            z = i // (self.width * self.depth)
            
            world_height = self.height_map[x][z]
            index = self._generate_index(x, y, z)
            
            if index >= 0:
                if y < world_height - 5:
                    self.blocks[index] = TileType.STONE.id
                elif y < world_height:
                    self.blocks[index] = TileType.DIRT.id
                elif y == world_height:
                    self.blocks[index] = TileType.GRASS.id
        
        self.sub_progress = end_idx
        
        progress = (self.sub_progress / self.sub_total) * 100
        self.levelLoaderListener.levelLoadUpdate(f"Building terrain... {int(progress)}%")
        
        return self.sub_progress >= self.sub_total
    
    def _prepare_cave_carving(self):
        BATCH_SIZE = 8
        
        if self.sub_progress == 0:
            self.sub_total = self.width * self.height * self.depth // 6000
            if self.sub_total == 0:
                return True
        
        start_cave = self.sub_progress
        end_cave = min(start_cave + BATCH_SIZE, self.sub_total)
        
        for i in range(start_cave, end_cave):
            x = random.randint(15, self.width - 15)
            y = random.randint(8, self.depth - 25)
            z = random.randint(15, self.height - 15)
            
            tunnel_length = random.randint(25, 60)
            direction_x = random.uniform(-0.3, 0.3)
            direction_z = random.uniform(-0.3, 0.3)
            
            for step in range(tunnel_length):
                direction_x += random.uniform(-0.1, 0.1)
                direction_z += random.uniform(-0.1, 0.1)
                
                x += direction_x
                y += random.uniform(-0.2, 0.1)
                z += direction_z
                
                radius = random.randint(2, 3)
                
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        for dz in range(-radius, radius + 1):
                            distance = dx*dx + dy*dy + dz*dz
                            if distance <= radius*radius:
                                nx, ny, nz = int(x) + dx, int(y) + dy, int(z) + dz
                                if (0 <= nx < self.width and 5 <= ny < self.depth - 5 and 
                                    0 <= nz < self.height and ny < self.height_map[nx][nz] - 3):
                                    index = self._generate_index(nx, ny, nz)
                                    if index >= 0:
                                        self.blocks[index] = 0
        
        self.sub_progress = end_cave
        progress = (self.sub_progress / self.sub_total) * 100
        self.levelLoaderListener.levelLoadUpdate(f"Carving caves... {int(progress)}%")
        
        return self.sub_progress >= self.sub_total
    
    def _finalize_level(self):
        self.level.setData(self.width, self.height, self.depth, self.blocks)
        self.level.create_time = time.time()
        self.level.creator = self.user_name
        self.level.name = "A Nice World"
        
        self.levelLoaderListener.levelLoadUpdate("Finalizing... 100%")
        return True
    
    def _generate_index(self, x: int, y: int, z: int) -> int:
        if x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height:
            return -1
        return (y * self.height + z) * self.width + x
    
    def is_generation_complete(self):
        return not self.is_generating
