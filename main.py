import time
from ursina import *
from src.HitResult import HitResult
from src.render.Tessellator import Tessellator
from src.level.Level import Level
from src.level.LevelRenderer import LevelRenderer
from src.level.LevelLoaderListener import LevelLoaderListener
from src.level.generator.LevelGen import LevelGen
from src.Player import Player
from src.Timer import Timer
from src.level.Chunk import Chunk
from src.character.Human import Human
from src.level.tile.Tile import Tile
import src.level.TileType as TileType
from src.gui.Font import Font
from src.gui.Screen import Screen
from src.gui.PauseScreen import PauseScreen
from src.Utils import *

class ModernClassic(LevelLoaderListener):
    def __init__(self, app):
        self.width = 854
        self.height = 480
        self.app = app
        
        self.hitResult = None 
        self.tessellator = Tessellator()
        
        self.crosshair_entity_1 = None
        self.crosshair_entity_2 = None
        self.held_block_entity = None
        
        self.held_block_entity_rotation_x = 30
        self.held_block_entity_rotation_y = 45
        

        self.level: Level = Level(32, 32, 64)
        self.levelRenderer: LevelRenderer = None
        self.player: Player = Player(self.level)
        self.timer: Timer = Timer(20)
        self.screen: Screen = None
        self.levelGen: LevelGen = LevelGen(self)
        
        self.humans = []
        
        self.current_block = TileType.STONE.id
        
        self.is_mouse_right = False
        self.is_mouse_left = False
        
        self.font = Font('res/default.png')
        self.text_entities = []
        self.loading_entities = []
        
        self.loading = False
        self.loading_title = ""
        self.loading_status = ""
        self.world_loaded = False
        self.chunks_preloaded = False
        
        self.mouseGrabbed = False
        

        self.frames = 0
        self.lastTime = time.time()
        
        camera.fov = 90
        
        if not self._tryLoadLevel():
            self.generateNewLevel()
        
        # print(self._tryLoadLevel())
        
        # for i in range(1):
        #     self.humans.append(Human(self.level, 0.0, 0.0, 0.0))
        
    def setScreen(self, screen):
        self.screen = screen
        if (screen != None):
                screenWidth = self.width * 240 / self.height
                screenHeight = self.height * 240 / self.height
                screen.init(self, screenWidth, screenHeight)
                
    def grabMouse(self):
        if (not self.mouseGrabbed):
            self.mouseGrabbed = True
            mouse.locked = True
            self.setScreen(None)
            
    def releaseMouse(self):
        if (self.mouseGrabbed):
            self.mouseGrabbed = False
            mouse.locked = False
            self.setScreen(PauseScreen())
    
    def _tryLoadLevel(self):
        try:
            if os.path.exists("level.sav"):

                self.beginLevelLoading("Loading level")
                self.levelLoadUpdate("Reading save file...")
                self.app.step()
                
                self.level.load()
                self.levelLoadUpdate("Level loaded!")
                self.app.step()
                return True
        except Exception as e:
            print(f"Failed to load level: {e}")
        return False
        
    def generateNewLevel(self):
        print("Generating new level...")
        success = self.levelGen.generateLevel(self.level, "Player", self.level.width, self.level.height, self.level.depth)
        if success:
            print("Level generation complete!")
            
    def _create_renderer_and_preload(self):

        self.levelRenderer = LevelRenderer(self.level)
        self.levelLoadUpdate("Preloading chunks...")
        self.setupHeldBlockDisplay()

        self.chunks_preloaded = True
        self.levelLoadComplete()
            
    def beginLevelLoading(self, title: str):
        self.loading = True
        self.loading_title = title
        self.loading_status = ""
        
        for entity in self.loading_entities:
            destroy(entity)
        self.loading_entities.clear()
        
        background = Entity(
            model='cube',
            scale=(2, 2),
            position=(0, 0, 5),
            color=color.gray,
            parent=camera.ui,
            texture='res/dirt.png',
            texture_scale=(16, 16)
        )
        self.loading_entities.append(background)
        

        self.app.step()
    
    def levelLoadUpdate(self, status: str):
        self.loading_status = status
        # print(f"Loading: {status}")
        
        self._update_loading_screen()

        self.app.step()
        
    def levelLoadComplete(self):
        self.loading = False
        self.world_loaded = True
        
        for entity in self.loading_entities:
            destroy(entity)
        self.loading_entities.clear()
        
        if not self.levelRenderer:
            self._create_renderer_and_preload()
        
        self.grabMouse()
        self.setupHeldBlockDisplay()
        
    def _update_loading_screen(self):
        if not self.loading:
            return
        
        for entity in self.loading_entities[1:]:
            destroy(entity)
        self.loading_entities = self.loading_entities[:1]
        
        if self.loading_title:
            title_entities = self.font.draw_shadow(
                self.loading_title, 
                0.0, 
                0.3,
                size=0.8,
                text_origin=0.5
            )
            
            self.loading_entities.extend(title_entities)
        
        if self.loading_status:
            status_entities = self.font.draw_shadow(
                self.loading_status, 
                0, 
                0, 
                size=0.6,
                text_origin=0.5
            )
            self.loading_entities.extend(status_entities)
    

    def moveCameraToPlayer(self, partialTicks):
        player = self.player
        camera.rotation_x = player.xRotation
        camera.rotation_y = player.yRotation
        
        smooth_x = lerp(player.prevX, player.x, partialTicks)
        smooth_y = lerp(player.prevY, player.y, partialTicks)
        smooth_z = lerp(player.prevZ, player.z, partialTicks)
        
        camera.position = (smooth_x, smooth_y, smooth_z)
        
    def pick(self):
        self.hitResult = None
        
        origin = camera.world_position
        direction = camera.forward.normalized()
        max_distance = 6
        
        result = voxel_ray_cast(origin, direction, max_distance, 
                            lambda x, y, z: self.level.getTile(x, y, z))
        if result:
            x, y, z, face = result
            self.hitResult = HitResult(x=x, y=y, z=z, face=face, entity=None)
        else:
            self.hitResult = None

    def tick(self):
        if not self.world_loaded:
            return
        
        if held_keys['enter']: self.level.save()
        elif held_keys['1']: self.current_block = TileType.STONE.id; self.setupHeldBlockDisplay()
        elif held_keys['2']: self.current_block = TileType.DIRT.id; self.setupHeldBlockDisplay()
        elif held_keys['3']: self.current_block = TileType.PLANKS.id; self.setupHeldBlockDisplay()
        elif held_keys['4']: self.current_block = TileType.COBBLESTONE.id; self.setupHeldBlockDisplay()
        elif held_keys['6']: self.current_block = TileType.BUSH.id; self.setupHeldBlockDisplay()
        elif held_keys['escape']: self.releaseMouse()
        
        if (self.screen != None):
            self.screen.updateEvents()
            if (self.screen != None):
                self.screen.tick()
        
        self.level.onTick()
        
        for human in self.humans:
            human.tick()
        
        self.player.tick()
    
    def render(self, partialTicks):
        motionX = mouse.velocity.x * 18.55
        motionY = mouse.velocity.y * 18.55
        self.player.turn(motionX, motionY)
        
        self.pick()
        
        if mouse.right and self.hitResult != None and self.is_mouse_right == False:
            self.is_mouse_right = True
            self.level.setTile(self.hitResult.x, self.hitResult.y, self.hitResult.z, 0)
        elif not mouse.right:
            self.is_mouse_right = False
        
        if mouse.left and self.hitResult != None and self.is_mouse_left == False:
            self.is_mouse_left = True
            x: int = self.hitResult.x
            y: int = self.hitResult.y
            z: int = self.hitResult.z
            
            if self.hitResult.face == 0: y -= 1
            if self.hitResult.face == 1: y += 1
            if self.hitResult.face == 2: z -= 1
            if self.hitResult.face == 3: z += 1
            if self.hitResult.face == 4: x -= 1
            if self.hitResult.face == 5: x += 1
            
            self.level.setTile(x, y, z, self.current_block)
        elif not mouse.left:
            self.is_mouse_left = False
        
        self.moveCameraToPlayer(partialTicks)
        
        self.levelRenderer.render(0)
        
        for human in self.humans:
            human.render(partialTicks)
        
        self.levelRenderer.render(1)
        
        self.levelRenderer.renderHit(self.hitResult)
        
        self.drawGui()
        
    def updateHeldBlock(self):
        if self.held_block_entity:
            self.held_block_entity_rotation_y += time.dt * 20
            self.held_block_entity_rotation_x += time.dt * 20
            self.held_block_entity.rotation_y = self.held_block_entity_rotation_y
            self.held_block_entity.rotation_x = self.held_block_entity_rotation_x
            
    def setupHeldBlockDisplay(self):
        if self.held_block_entity: 
            destroy(self.held_block_entity)
        
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
    
    def drawGui(self):
        screenWidth = self.width * 240 / self.height
        screenHeight = self.height * 240 / self.height
        xMouse = mouse.x * screenWidth / self.height - 1
        yMouse = screenHeight - mouse.y * screenHeight / self.height - 1
        
        
        if self.crosshair_entity_1:
            destroy(self.crosshair_entity_1)
        if self.crosshair_entity_2:
            destroy(self.crosshair_entity_2)

        for entity in self.text_entities:
            destroy(entity)
        self.text_entities.clear()
        
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
            
        version_entities = self.font.draw_shadow("d0.0.2 &eunstable", -0.85, 0.45, size=0.6)
        self.text_entities.extend(version_entities)

        if held_keys['f3']:
            fps_text = f"FPS: {int(1.0/time.dt) if time.dt > 0 else 0}"
            chunk_text = f"Chunk updates: {Chunk.UPDATES}"
            pos_text = f"XYZ: {self.player.x:.1f} / {self.player.y:.1f} / {self.player.z:.1f}"
            
            fps_entities = self.font.draw(fps_text, -0.85, 0.35, size=0.6)
            self.text_entities.extend(fps_entities)
                
            chunk_entities = self.font.draw(chunk_text, -0.85, 0.30, size=0.6)
            self.text_entities.extend(chunk_entities)
                
            pos_entities = self.font.draw(pos_text, -0.85, 0.25, size=0.6)
            self.text_entities.extend(pos_entities)
            
        if (self.screen != None):
            self.screen.render(xMouse, yMouse)

    def update(self):
        
        if self.levelGen.is_generating:
            self.levelGen._continue_generation()
            return
        
        self.timer.advanceTime()
        
        for i in range(self.timer.ticks):
            self.tick()
            
        self.render(self.timer.partialTicks)
        self.updateHeldBlock()
        
        self.frames += 1
        
        if time.time() >= self.lastTime + 2.0:
            print(f"{self.frames} fps, {Chunk.UPDATES} chunk updates")
            
            Chunk.UPDATES = 0
            
            self.lastTime += 2.0
            self.frames = 0

    def shutdown(self):
        self.level.save()
        if self.held_block_entity:
            destroy(self.held_block_entity)
        if self.crosshair_entity_1:
            destroy(self.crosshair_entity_1)
        if self.crosshair_entity_2:
            destroy(self.crosshair_entity_2)

if __name__ == "__main__":
    app = Ursina(title='ModernClassic', development_mode=False, fullscreen=False, borderless=False, size=(854, 480))
    window.color = color.rgba(0.5, 0.8, 1.0, 1.0)
    
    game = ModernClassic(app)
    
    def update():
        game.update()
    
    app.run()
