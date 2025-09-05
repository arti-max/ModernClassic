from src.level.tile.Tile import Tile

class GrassTile(Tile):
    
    def __init__(self, id):
        super().__init__(id)
        
        self.textureID = 4
        
    def getTexture(self, face):
        return 0 if face == 1 else 3 if face == 0 else 4