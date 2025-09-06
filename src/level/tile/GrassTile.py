from src.level.tile.Tile import Tile
from src.level.Util import nextInt
import src.level.TileType as TileType

class GrassTile(Tile):
    
    def __init__(self, id):
        super().__init__(id)
        
        self.textureID = 4
        
    def getTexture(self, face):
        return 0 if face == 1 else 3 if face == 0 else 4
    
    def onTick(self, level, x, y, z):
        if (level.isLit(x, y, z)):
            
            for i in range(4):
                targetX = x + nextInt(3) - 1
                targetY = y + nextInt(5) - 3
                targetZ = z + nextInt(3) - 1
                
                
                if (level.getTile(targetX, targetY, targetZ) == TileType.DIRT.id and level.isLit(targetX, targetY, targetZ)):
                    level.setTile(targetX, targetY, targetZ, TileType.GRASS.id)
        else:
            level.setTile(x, y, z, TileType.DIRT.id)