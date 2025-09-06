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
        

        self.level = Level(128, 128, 64)
        self.levelRenderer = LevelRenderer(self.level)
        self.player = Player(self.level)
        self.timer = Timer(20)
        self.levelGen = LevelGen(self)
        
        self.humans = []
        
        self.current_block = TileType.STONE.id
        
        self.is_mouse_right = False
        self.is_mouse_left = False
        
        self.font = Font('default')
        self.text_entities = []
        self.loading_entities = []
        
        # Состояние загрузки
        self.loading = False
        self.loading_title = ""
        self.loading_status = ""
        self.world_loaded = False
        self.chunks_preloaded = False
        

        self.frames = 0
        self.lastTime = time.time()
        
        mouse.locked = True
        camera.fov = 90
        
        if not self._tryLoadLevel():
            self.generateNewLevel()
        
        # print(self._tryLoadLevel())
        
        
        self.setupHeldBlockDisplay()
        
        # for i in range(1):
        #     self.humans.append(Human(self.level, 0.0, 0.0, 0.0))
        
    def _tryLoadLevel(self):
        try:
            if os.path.exists("level.sav"):
                # Показываем загрузку существующего мира
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
        """Создает renderer и запускает предзагрузку чанков"""
        self.levelRenderer = LevelRenderer(self.level)
        self.level_load_update("Preloading chunks...")
        self.setupHeldBlockDisplay()
        # Не генерируем чанки здесь - просто отмечаем что готовы
        self.chunks_preloaded = True
        self.level_load_complete()
            
    def beginLevelLoading(self, title: str):
        self.loading = True
        self.loading_title = title
        self.loading_status = ""
        
        # Очищаем старые loading entities
        for entity in self.loading_entities:
            destroy(entity)
        self.loading_entities.clear()
        
        # Создаем темный фон
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
        
        # Принудительно обновляем экран
        self.app.step()
    
    def levelLoadUpdate(self, status: str):
        self.loading_status = status
        print(f"Loading: {status}")
        
        self._update_loading_screen()
        # Принудительно обновляем экран
        self.app.step()
        
    def levelLoadComplete(self):
        self.loading = False
        self.world_loaded = True
        
        # Убираем экран загрузки
        for entity in self.loading_entities:
            destroy(entity)
        self.loading_entities.clear()
        
        # Создаем renderer если еще не создан
        if not self.levelRenderer:
            self._create_renderer_and_preload()
        
    def _update_loading_screen(self):
        """Обновляет экран загрузки"""
        if not self.loading:
            return
        
        # Очищаем старые текстовые entities (кроме фона)
        for entity in self.loading_entities[1:]:
            destroy(entity)
        self.loading_entities = self.loading_entities[:1]
        
        # Показываем заголовок
        if self.loading_title:
            title_entities = self.font.draw_shadow(
                self.loading_title, 
                self.width // 2 - 100, 
                self.height // 2 - 160, 
                color.white
            )
            self.loading_entities.extend(title_entities)
        
        # Показываем статус
        if self.loading_status:
            status_entities = self.font.draw_shadow(
                self.loading_status, 
                self.width // 2 - 90, 
                self.height // 2 - 80, 
                color.light_gray
            )
            self.loading_entities.extend(status_entities)
        
        # Простая полоска прогресса
        # if "%" in self.loading_status:
        #     try:
        #         percent_str = self.loading_status.split('%')[0].split()[-1]
        #         progress = float(percent_str) / 100.0
                
        #         # Фон полоски
        #         progress_bg = Entity(
        #             model='cube',
        #             scale=(6, 0.2, 0.01),
        #             position=(0, -0.2, -1),
        #             color=color.dark_gray,
        #             parent=camera.ui
        #         )
        #         self.loading_entities.append(progress_bg)
                
        #         # Заполненная часть
        #         if progress > 0:
        #             progress_fill = Entity(
        #                 model='cube',
        #                 scale=(6 * progress, 0.18, 0.01),
        #                 position=(-3 * (1 - progress), -0.2, -0.9),
        #                 color=color.green,
        #                 parent=camera.ui
        #             )
        #             self.loading_entities.append(progress_fill)
        #     except:
        #         pass

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
        
        hit_info = raycast(
            origin=camera.world_position, 
            direction=camera.forward, 
            distance=5,
            ignore=[self.levelRenderer.hit_entity]
        )

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

    def tick(self):
            
        if held_keys['enter']: self.level.save()
        elif held_keys['1']: self.current_block = TileType.STONE.id; self.setupHeldBlockDisplay()
        elif held_keys['2']: self.current_block = TileType.DIRT.id; self.setupHeldBlockDisplay()
        elif held_keys['3']: self.current_block = TileType.PLANKS.id; self.setupHeldBlockDisplay()
        elif held_keys['4']: self.current_block = TileType.COBBLESTONE.id; self.setupHeldBlockDisplay()
        elif held_keys['6']: self.current_block = TileType.BUSH.id; self.setupHeldBlockDisplay()
        
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
        """Отрисовка интерфейса"""
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
            
        version_entities = self.font.draw_shadow("d0.0.2", 10, 10, color.white)
        self.text_entities.extend(version_entities)
        
        # Рисуем отладочную информацию
        if held_keys['f3']:
            print(f"F3 pressed")
            fps_text = f"FPS: {int(1.0/time.dt) if time.dt > 0 else 0}"
            chunk_text = f"Chunk updates: {Chunk.UPDATES}"
            pos_text = f"XYZ: {self.player.x:.1f} / {self.player.y:.1f} / {self.player.z:.1f}"
            
            fps_entity = self.font.draw(fps_text, 10, 30, color.yellow)
            if fps_entity:
                self.text_entities.append(fps_entity)
                
            chunk_entity = self.font.draw(chunk_text, 10, 50, color.yellow)
            if chunk_entity:
                self.text_entities.append(chunk_entity)
                
            pos_entity = self.font.draw(pos_text, 10, 70, color.yellow)
            if pos_entity:
                self.text_entities.append(pos_entity)

    def update(self):
        if held_keys['escape']:
            exit(0)
        
        if self.levelGen.is_generating:
            self.levelGen._continue_generation()
            return
        
        self.timer.advanceTime()
        
        for i in range(self.timer.ticks):
            self.tick()
            
        self.render(self.timer.partialTicks)
        self.updateHeldBlock()
        
        self.frames += 1
        
        if time.time() >= self.lastTime + 1.0:
            print(f"{self.frames} fps, {Chunk.UPDATES} chunk updates")
            
            Chunk.UPDATES = 0
            
            self.lastTime += 1.0
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
