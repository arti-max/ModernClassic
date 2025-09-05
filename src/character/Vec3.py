


class Vec3:
    
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def interpolateTo(self, vector, partialTicks: float):
        interpolatedX: float = self.x + (vector.x - self.x) * partialTicks
        interpolatedY: float = self.y + (vector.y - self.y) * partialTicks
        interpolatedZ: float = self.z + (vector.z - self.z) * partialTicks

        return Vec3(interpolatedX, interpolatedY, interpolatedZ)
    
    def set(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z