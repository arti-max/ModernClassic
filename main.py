import time
from ursina import *
from src.HitResult import HitResult
from src.render.Tessellator import Tessellator
from src.level.Level import Level
from src.level.LevelRenderer import LevelRenderer
from src.Player import Player
from src.Timer import Timer
from src.level.Chunk import Chunk
from src.character.Human import Human
from src.level.tile.Tile import Tile
import src.level.TileType as TileType

class Self:
    def __init__(self):
        pass

if __name__ == "__main__":
    app = Ursina(title='ModernClassic', development_mode=False, fullscreen=False, borderless=False) # size=(720, 480)
    window.color = color.rgba(0.5, 0.8, 1.0, 1.0)
    
    
    self = Self()
    
    self.hitResult = None 
    self.tessellator = Tessellator()
    
    self.crosshair_entity_1 = None
    self.crosshair_entity_2 = None
    self.held_block_entity = None
    
    self.held_block_entity_rotation_x = 30
    self.held_block_entity_rotation_y = 45
    
    self.level = Level(128, 128, 64)
    self.levelRenderer = LevelRenderer(self.level)
    self.player = Player(self.level)
    self.timer = Timer(20)
    
    self.humans = []
    
    self.current_block = TileType.STONE.id
    
    self.is_mouse_right = False
    self.is_mouse_left = False
    mouse.locked = True
    
    frames = 0
    lastTime = time.time()
    
    # for i in range(1):
    #     self.humans.append(Human(self.level, 0.0, 0.0, 0.0))
    
    
    def moveCameraToPlayer(partialTicks):
        global self
        
        player = self.player
        camera.rotation_x = player.xRotation
        camera.rotation_y = player.yRotation
        
        smooth_x = lerp(player.prevX, player.x, partialTicks)
        smooth_y = lerp(player.prevY, player.y, partialTicks)
        smooth_z = lerp(player.prevZ, player.z, partialTicks)
        

        camera.position = (smooth_x, smooth_y, smooth_z)
        
    def pick():
        global self
        
        self.hitResult = None
        
        hit_info = raycast(
            origin=camera.world_position, 
            direction=camera.forward, 
            distance=5,
            ignore=[self.levelRenderer.hit_entity]
        )
        
        # print(hit_info.)

        if hit_info.hit:
            block_pos = hit_info.point - hit_info.world_normal * 0.01
            
            x = floor(block_pos.x)
            y = floor(block_pos.y)
            z = floor(block_pos.z)
            
            normal = hit_info.world_normal
            face = -1
            
            if normal == Vec3(0, 1, 0): face = 1  # Y+
            elif normal == Vec3(0, -1, 0): face = 0 # Y-
            elif normal == Vec3(0, 0, 1): face = 3  # Z+
            elif normal == Vec3(0, 0, -1): face = 2 # Z-
            elif normal == Vec3(1, 0, 0): face = 5  # X+
            elif normal == Vec3(-1, 0, 0): face = 4 # X-

            if face != -1:
                self.hitResult = HitResult(x=x, y=y, z=z, face=face, entity=hit_info.entity)
                return
            
        self.hitResult = None
    

    def tick():
        
        if (held_keys['enter']):
            self.level.save()
        elif (held_keys['1']): self.current_block = TileType.STONE.id; setupHeldBlockDisplay()
        elif (held_keys['2']): self.current_block = TileType.DIRT.id; setupHeldBlockDisplay()
        elif (held_keys['3']): self.current_block = TileType.PLANKS.id; setupHeldBlockDisplay()
        elif (held_keys['4']): self.current_block = TileType.COBBLESTONE.id; setupHeldBlockDisplay()
        elif (held_keys['6']): self.current_block = TileType.BUSH.id; setupHeldBlockDisplay()
        
        self.level.onTick()
        
        for human in self.humans:
            human.tick()
        
        self.player.tick()
    
    def render(partialTicks):
        global self
        
        motionX = mouse.velocity.x * 18.55
        motionY = mouse.velocity.y * 18.55
        
        self.player.turn(motionX, motionY)
        
        pick()
        
        if (mouse.right and self.hitResult != None and self.is_mouse_right == False):
            self.is_mouse_right = True
            
            self.level.setTile(self.hitResult.x, self.hitResult.y, self.hitResult.z, 0)
            
        elif (not mouse.right):
            self.is_mouse_right = False
        
        if (mouse.left and self.hitResult != None and self.is_mouse_left == False):
            self.is_mouse_left = True
            x: int = self.hitResult.x
            y: int = self.hitResult.y
            z: int = self.hitResult.z
            
            if (self.hitResult.face == 0): y -= 1
            if (self.hitResult.face == 1): y += 1
            if (self.hitResult.face == 2): z -= 1
            if (self.hitResult.face == 3): z += 1
            if (self.hitResult.face == 4): x -= 1
            if (self.hitResult.face == 5): x += 1
            
            self.level.setTile(x, y, z, self.current_block)
        elif (not mouse.left):
            self.is_mouse_left = False
        
        moveCameraToPlayer(partialTicks)
        
        self.levelRenderer.render(0)
        
        for human in self.humans:
            human.render(partialTicks)
        
        self.levelRenderer.render(1)
        
        self.levelRenderer.renderHit(self.hitResult)
        
        drawGui()
        
    def updateHeldBlock():
        if self.held_block_entity:
            self.held_block_entity_rotation_y += time.dt * 20
            self.held_block_entity_rotation_x += time.dt * 20
            self.held_block_entity.rotation_y = self.held_block_entity_rotation_y
            self.held_block_entity.rotation_x = self.held_block_entity_rotation_x
            
    def setupHeldBlockDisplay():
        if self.held_block_entity: destroy(self.held_block_entity)
        
        self.tessellator.clear()
        tileToRender = Tile.TILES[self.current_block]
        
        for i in range(6):
            tileToRender.renderFace(self.tessellator, 0, 0, 0, i, centerToOrigin=True)
            
        self.held_block_entity = self.tessellator.flush()
        
        if self.held_block_entity:
            self.held_block_entity.parent = camera.ui
            self.held_block_entity.texture = load_texture('res/terrain.png')
            
            self.held_block_entity.position = (
                window.aspect_ratio * 0.5 - 0.1,
                0.5 - 0.1,
                -2
            )
            
            self.held_block_entity.scale = 0.1
            
            self.held_block_entity.rotation_x = self.held_block_entity_rotation_x
            self.held_block_entity.rotation_y = self.held_block_entity_rotation_y
    
    def drawGui():
        if self.crosshair_entity_1:
            destroy(self.crosshair_entity_1)
        if self.crosshair_entity_2:
            destroy(self.crosshair_entity_2)
        
        width, height = window.size
        
        screenWidth: int = int(width * 240 / height)
        screenHeight: int = int(height * 240 / height)
        
        x = int(screenWidth / 2)
        y = int(screenHeight / 2)
        
        # crosshair
        self.tessellator.clear()
        size = 0.01

        self.tessellator.vertex(0, size, 0)
        self.tessellator.vertex(0, -size, 0)
        self.crosshair_entity_1 = self.tessellator.flush_lines()
        
        if self.crosshair_entity_1:
            self.crosshair_entity_1.parent = camera.ui
            self.crosshair_entity_1.color = color.white
        
        self.tessellator.vertex(size, 0, 0)
        self.tessellator.vertex(-size, 0, 0)
        self.crosshair_entity_2 = self.tessellator.flush_lines()
        
        if self.crosshair_entity_2:
            self.crosshair_entity_2.parent = camera.ui
            self.crosshair_entity_2.color = color.white

    def update():
        global frames, lastTime
        
        if (held_keys['escape']):
            exit(0)
        
        self.timer.advanceTime()
        
        for i in range(self.timer.ticks):
            tick()
            
        render(self.timer.partialTicks)
        
        updateHeldBlock()
        
        frames += 1
        
        if (time.time() >= lastTime + 1.0):
            print(f"{frames} fps, {Chunk.UPDATES} chunk updates")
            
            Chunk.UPDATES = 0
            
            lastTime += 1.0
            frames = 0

    
    camera.fov = 90
    
    setupHeldBlockDisplay()
    app.run()