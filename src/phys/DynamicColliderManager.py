# src/physics/DynamicCollisionManager.py
import math
from ursina import *
from src.level.tile.Tile import Tile

class DynamicColliderManager:
    def __init__(self, level, player):
        self.level = level
        self.player = player
        self.collision_entities = {}
        self.collision_area_size = 7
        self.collision_height = 7
        
        self.last_player_chunk_x = None
        self.last_player_chunk_y = None
        self.last_player_chunk_z = None
        
    def update(self):
        player_x = int(math.floor(self.player.x))
        player_y = int(math.floor(self.player.y))
        player_z = int(math.floor(self.player.z))
        
        chunk_x = player_x // self.collision_area_size
        chunk_y = player_y // self.collision_height
        chunk_z = player_z // self.collision_area_size
        
        if (chunk_x != self.last_player_chunk_x or 
            chunk_y != self.last_player_chunk_y or 
            chunk_z != self.last_player_chunk_z):
            
            self.last_player_chunk_x = chunk_x
            self.last_player_chunk_y = chunk_y
            self.last_player_chunk_z = chunk_z
            
            # self._update_collision_area(player_x, player_y, player_z)
    
    def _update_collision_area(self, center_x, center_y, center_z):
        self._clear_collision_entities()
        
        half_size = self.collision_area_size // 2
        half_height = self.collision_height // 2
        
        min_x = center_x - half_size
        max_x = center_x + half_size + 1
        min_y = max(0, center_y - half_height)
        max_y = min(self.level.depth, center_y + half_height + 1)
        min_z = center_z - half_size
        max_z = center_z + half_size + 1
        
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                for z in range(min_z, max_z):
                    self._create_collision_block(x, y, z)
    
    def _create_collision_block(self, x, y, z):
        if (x < 0 or y < 0 or z < 0 or 
            x >= self.level.width or y >= self.level.depth or z >= self.level.height):
            return

        if not self.level.isTile(x, y, z):
            return
        
        # print("create")
            
        collision_entity = Entity(
            model='cube',
            position=(x + 0.5, y + 0.5, z + 0.5),
            scale=(1, 1, 1),
            color=color.white,
            collider='box',
            visible=False
        )
        
        key = f"{x}_{y}_{z}"
        self.collision_entities[key] = collision_entity
    
    def _clear_collision_entities(self):
        for entity in self.collision_entities.values():
            destroy(entity)
        self.collision_entities.clear()
    
    def cleanup(self):
        self._clear_collision_entities()
