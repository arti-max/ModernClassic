# src/gui/Font.py
from ursina import Text, destroy, color, camera

class Font:
    def __init__(self, name='default'):
        self.name = name
        
    def draw(self, text, x, y, text_color):
        ui_x = (x / 400) - 1
        ui_y = 0.5 - (y / 300)
        
        text_entity = Text(
            text=text,
            position=(ui_x, ui_y, 0),
            scale=2,
            color=text_color,
            parent=camera.ui
        )
        return text_entity
        
    def draw_shadow(self, text, x, y, text_color):
        """Рисует текст с тенью"""
        entities = []
        
        shadow_entity = self.draw(text, x+2, y+2, color.dark_gray)
        entities.append(shadow_entity)
        
        text_entity = self.draw(text, x, y, text_color)
        entities.append(text_entity)
        
        return entities
