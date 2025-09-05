# В файле NoiseFilter.py
import math

class NoiseFilter:
    
    def __init__(self, seed=0):
        self.seed = seed
        
    def _get_raw_noise(self, x, z):
        n = int(x) * 57 + int(z) * 131 + self.seed
        n = (n << 13) ^ n
        # Приводим к диапазону [-1, 1]
        return (1.0 - ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0)

    def _get_smooth_noise(self, x, z):
        floor_x = int(x)
        floor_z = int(z)
        
        frac_x = x - floor_x
        frac_z = z - floor_z

        v1 = self._get_raw_noise(floor_x,     floor_z)
        v2 = self._get_raw_noise(floor_x + 1, floor_z)
        v3 = self._get_raw_noise(floor_x,     floor_z + 1)
        v4 = self._get_raw_noise(floor_x + 1, floor_z + 1)

        i1 = self._interpolate(v1, v2, frac_x)
        i2 = self._interpolate(v3, v4, frac_x)
        
        return self._interpolate(i1, i2, frac_z)

    def _interpolate(self, a, b, blend):
        theta = blend * math.pi
        f = (1.0 - math.cos(theta)) * 0.5
        return a * (1.0 - f) + b * f

    def get_noise(self, x, z):
        total_noise = 0.0
        frequency = 0.01
        amplitude = 1.0
        
        for _ in range(4):
            total_noise += self._get_smooth_noise(x * frequency, z * frequency) * amplitude
            
            frequency *= 2
            amplitude /= 2
            
        return total_noise
