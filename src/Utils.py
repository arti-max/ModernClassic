import numpy as np
from math import floor


# 3D DDA voxel ray casting function (no more colliders)
def voxel_ray_cast(origin, direction, max_distance, get_block_type, block_size=1):
    ox, oy, oz = origin
    dx, dy, dz = direction
    
    x = floor(ox)
    y = floor(oy) 
    z = floor(oz)
    
    step_x = 1 if dx > 0 else -1
    step_y = 1 if dy > 0 else -1
    step_z = 1 if dz > 0 else -1
    
    if dx == 0:
        t_max_x = float('inf')
        t_delta_x = float('inf')
    else:
        if dx > 0:
            t_max_x = (x + 1.0 - ox) / dx
        else:
            t_max_x = (ox - x) / (-dx)
        t_delta_x = abs(1.0 / dx)
    
    if dy == 0:
        t_max_y = float('inf')
        t_delta_y = float('inf')
    else:
        if dy > 0:
            t_max_y = (y + 1.0 - oy) / dy
        else:
            t_max_y = (oy - y) / (-dy)
        t_delta_y = abs(1.0 / dy)
    
    if dz == 0:
        t_max_z = float('inf')
        t_delta_z = float('inf')
    else:
        if dz > 0:
            t_max_z = (z + 1.0 - oz) / dz
        else:
            t_max_z = (oz - z) / (-dz)
        t_delta_z = abs(1.0 / dz)
    
    t = 0.0
    face = None
    
    while t <= max_distance:
        block_id = get_block_type(x, y, z)
        if block_id and block_id != 0:
            return (x, y, z, face)
        
        if t_max_x < t_max_y and t_max_x < t_max_z:
            t = t_max_x
            t_max_x += t_delta_x
            x += step_x
            face = 4 if step_x > 0 else 5  # X- or X+
        elif t_max_y < t_max_z:
            t = t_max_y
            t_max_y += t_delta_y
            y += step_y
            face = 0 if step_y > 0 else 1  # Y- or Y+
        else:
            t = t_max_z
            t_max_z += t_delta_z
            z += step_z
            face = 2 if step_z > 0 else 3  # Z- or Z+
    
    return None