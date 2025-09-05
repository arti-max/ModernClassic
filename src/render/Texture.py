from ursina import load_texture

BINDED_TEXTURE = None

def bind_texture(texture):
    global BINDED_TEXTURE
    BINDED_TEXTURE = load_texture(texture)