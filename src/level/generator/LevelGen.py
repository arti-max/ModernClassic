# src/level/generator/LevelGen.py
import math
import random
import time
from src.level.LevelLoaderListener import LevelLoaderListener
from src.level.generator.NoiseFilter import NoiseFilter
import src.level.TileType as TileType
import numpy as np
from ursina import application

class LevelGen:
    def __init__(self, levelLoaderListener: LevelLoaderListener):
        self.levelLoaderListener = levelLoaderListener
        self.width = 0
        self.height = 0
        self.depth = 0
        self.blocks = None
        self.random = random.Random()
        
        # Для асинхронной генерации
        self.generation_steps = []
        self.current_step = 0
        self.is_generating = False
    
    def generateLevel(self, level, user_name: str, width: int, height: int, depth: int):
        """Начинает асинхронную генерацию уровня"""
        self.levelLoaderListener.beginLevelLoading("Generating level")
        
        self.width = width
        self.height = height 
        self.depth = depth
        self.blocks = np.zeros(width * height * depth, dtype=np.uint8)
        
        # Подготавливаем шаги генерации
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
        
        # Запускаем первый шаг
        self._continue_generation()
    
    def _continue_generation(self):
        """Продолжает генерацию (вызывается каждый кадр)"""
        if not self.is_generating or self.current_step >= len(self.preparation_steps):
            return
        
        step_name, step_function = self.preparation_steps[self.current_step]
        self.levelLoaderListener.levelLoadUpdate(step_name)
        
        # Выполняем шаг генерации
        step_function()
        
        self.current_step += 1
        
        # Если генерация завершена
        if self.current_step >= len(self.preparation_steps):
            self.is_generating = False
            self.levelLoaderListener.levelLoadComplete()
    
    def _prepare_height_map(self):
        """Создает карту высот"""
        noise_generator = NoiseFilter(seed=random.randint(0, 12345))
        self.height_map = [[0 for _ in range(self.height)] for _ in range(self.width)]
        
        for x in range(self.width):
            for z in range(self.height):
                noise_value = noise_generator.get_noise(x, z)
                base_height = self.depth // 2
                variation = 16
                self.height_map[x][z] = int(base_height + noise_value * variation)
                
                # Обновляем прогресс
                progress = ((x * self.height + z) / (self.width * self.height)) * 100
                if int(progress) % 10 == 0:  # Каждые 10%
                    self.levelLoaderListener.levelLoadUpdate(f"Raising... {int(progress)}%")
                    # application.step()  # Обновляем экран
    
    def _prepare_terrain_build(self):
        """Создает базовые блоки"""
        total = self.width * self.height * self.depth
        processed = 0
        
        for x in range(self.width):
            for z in range(self.height):
                world_height = self.height_map[x][z]
                for y in range(self.depth):
                    index = self._generate_index(x, y, z)
                    
                    if y < world_height - 5:
                        self.blocks[index] = TileType.STONE.id
                    elif y < world_height:
                        self.blocks[index] = TileType.DIRT.id
                    elif y == world_height:
                        self.blocks[index] = TileType.GRASS.id
                    
                    processed += 1
                    
                    # Обновляем прогресс и экран
                    if processed % (total // 100) == 0:  # Каждый 1%
                        progress = (processed / total) * 100
                        self.levelLoaderListener.levelLoadUpdate(f"Building terrain... {int(progress)}%")
                        # application.step()
    
    def _prepare_cave_carving(self):
        """Создает пещеры"""
        cave_count = self.width * self.height * self.depth // 8192
        
        for i in range(cave_count):
            # Создаем пещеру
            x = random.randint(10, self.width - 10)
            y = random.randint(10, self.depth - 10)
            z = random.randint(10, self.height - 10)
            
            for dx in range(-3, 4):
                for dy in range(-2, 3):
                    for dz in range(-3, 4):
                        if dx*dx + dy*dy + dz*dz <= 9:
                            nx, ny, nz = x + dx, y + dy, z + dz
                            if 0 <= nx < self.width and 0 <= ny < self.depth and 0 <= nz < self.height:
                                index = self._generate_index(nx, ny, nz)
                                if self.blocks[index] == TileType.STONE.id:
                                    self.blocks[index] = 0
            
            # Обновляем прогресс
            if i % max(1, cave_count // 20) == 0:  # Каждые 5%
                progress = (i / cave_count) * 100
                self.levelLoaderListener.levelLoadUpdate(f"Carving caves... {int(progress)}%")
                # application.step()
    
    def _finalize_level(self):
        """Финализирует уровень"""
        self.level.setData(self.width, self.height, self.depth, self.blocks)
        self.level.create_time = time.time()
        self.level.creator = self.user_name
        self.level.name = "A Nice World"
    
    def _generate_index(self, x: int, y: int, z: int) -> int:
        """Генерирует индекс для 3D координат"""
        if x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height:
            return -1
        return (y * self.height + z) * self.width + x
    
    def is_generation_complete(self):
        """Проверяет, завершена ли генерация"""
        return not self.is_generating
