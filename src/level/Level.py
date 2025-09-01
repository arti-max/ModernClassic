

class Level:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        
        self.blocks = [0] * width * height * depth
        self.lightDepths = [0] * width * height
        
        for x in range(width):
            for z in range(height):
                for y in range(depth):
                   self.blocks[self.generate_index(x, y, z)] = 1 
                   
                   
        self.calcLightDepths(0, 0, width, height)
                    
    def generate_index(self, x, y, z):
        return (y * self.height + z) * self.width + x
    
    def calcLightDepths(self, minX, minZ, maxX, maxZ):
        for x in range(minX, maxX):
            for z in range(minZ, maxZ):
                prevData = self.lightDepths[z + z * self.width]
                
                depth = self.depth - 1
                while (depth > 0 and (not self.isLightBlocker(x, depth, z))):
                    depth -= 1
                    
                    
                self.lightDepths[x + z * self.width] = depth
            
    def isSolidTile(self, x, y, z):
        return self.isTile(x, y, z)
    
    def isTile(self, x, y, z):
        if (x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height):
            return False
        
        # print(x, y, z)
        
        return self.blocks[self.generate_index(x, y, z)] != 0
    
    def isLightBlocker(self, x, y, z):
        return self.isSolidTile(x, y, z)
    
    def getBrightness(self, x, y, z):
        dark = 0.8
        light = 1.0
        
        if (x < 0 or y < 0 or z < 0 or x >= self.width or y >= self.depth or z >= self.height):
            return light
        
        if (y < self.lightDepths[x + z * self.width]):
            return dark
        
        return light    # Unknown bright