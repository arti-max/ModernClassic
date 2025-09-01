from ursina import *
from src.render.Tessellator import Tessellator
from src.level.Level import Level
from src.level.LevelRenderer import LevelRenderer

if __name__ == "__main__":
    app = Ursina()
    
    level = Level(256, 256, 64)
    levelRenderer = LevelRenderer(level)
    
    def update():
        levelRenderer.render(0)
        levelRenderer.render(1)

    EditorCamera()
    

    app.run()