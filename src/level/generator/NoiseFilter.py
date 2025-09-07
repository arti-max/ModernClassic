import math
import random

class NoiseFilter:
    
    def __init__(self, seed=0):
        self.seed = seed
        
    def _get_raw_noise(self, x, z):
        n = int(x) * 57 + int(z) * 131 + self.seed
        n = (n << 13) ^ n
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
    
    def get_ridged_noise(self, x, z):
        total_noise = 0.0
        frequency = 0.008
        amplitude = 1.0
        
        for i in range(5):
            noise_val = abs(self._get_smooth_noise(x * frequency, z * frequency))
            noise_val = 1.0 - noise_val
            noise_val = pow(noise_val, 2.0)
            
            total_noise += noise_val * amplitude
            frequency *= 2.0
            amplitude *= 0.4
            
        return total_noise
    
    def get_cliff_noise(self, x, z):
        frequency = 0.005
        noise_val = self._get_smooth_noise(x * frequency, z * frequency)
        
        steps = 6
        stepped = math.floor(noise_val * steps) / steps
        
        if abs(noise_val - stepped) > 0.1:
            stepped += 0.3 * (1 if noise_val > stepped else -1)
            
        return stepped
    
    def get_terrain_noise(self, x, z):
        base = self.get_noise(x, z) * 0.4
        
        ridged = self.get_ridged_noise(x, z) * 0.8
        
        cliffs = self.get_cliff_noise(x, z) * 0.6
        
        details = self._get_smooth_noise(x * 0.05, z * 0.05) * 0.2
        
        combined = base + ridged + cliffs + details
        
        if combined > 0.3:
            combined = combined + pow(combined - 0.3, 1.5) * 0.5
            
        return combined
