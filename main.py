import time
from ursina import *
from src.render.Tessellator import Tessellator
from src.level.Level import Level
from src.level.LevelRenderer import LevelRenderer
from src.Player import Player
from src.Timer import Timer
from src.level.Chunk import Chunk

if __name__ == "__main__":
    app = Ursina()
    
    level = Level(32, 32, 64)
    levelRenderer = LevelRenderer(level)
    player = Player(level)
    timer = Timer(20)
    # destroy(camera.ui.parent)
    mouse.locked = True
    
    frames = 0
    lastTime = time.time()
    
    
    def moveCameraToPlayer(partialTicks):

        camera.rotation_x = player.xRotation
        camera.rotation_y = player.yRotation
        
        smooth_x = lerp(player.prevX, player.x, partialTicks)
        smooth_y = lerp(player.prevY, player.y, partialTicks)
        smooth_z = lerp(player.prevZ, player.z, partialTicks)
        

        camera.position = (smooth_x, smooth_y + 0.3, smooth_z)
        
        
    

    def tick():
        player.tick()
    
    def render(partialTicks):
        motionX = mouse.velocity.x * 6.55
        motionY = mouse.velocity.y * 6.55
        
        player.turn(motionX, motionY)
        
        moveCameraToPlayer(partialTicks)
        
        levelRenderer.render(0)
        levelRenderer.render(1)

    def update():
        global frames, lastTime
        
        timer.advanceTime()
        
        for i in range(timer.ticks):
            tick()
            
        render(timer.partialTicks)
        
        frames += 1
        
        if (time.time() >= lastTime + 1.0): # Уменьшил интервал до 1 секунды для удобства
            print(f"{frames} fps, {Chunk.UPDATES} chunk updates")
            
            Chunk.UPDATES = 0
            
            lastTime += 1.0
            frames = 0

    
    scene.fog_mode = 'linear'
    scene.fog_color = color.rgb(100, 100, 120)
    scene.fog_start = 0   # Начало тумана у камеры
    scene.fog_end = 30    # Полная плотность тумана на расстоянии 30 единиц
    
    camera.fov = 75
    app.run()