from src.render.Tessellator import Tessellator
from ursina import *
import ursina

class Screen:
    
    def __init__(self):
        pass
    
    def init(self, modernclassic, width, height):
        self.modernclassic = modernclassic
        self.width = width
        self.height = height
        
        self.ui_elements = []
    
    def render(self, x_mouse, y_mouse):
        pass
    
    def fill(self, minX, minY, maxX, maxY, col):
        a = (col >> 24 & 255) / 255.0
        r = (col >> 16 & 255) / 255.0
        g = (col >> 8 & 255) / 255.0
        b = (col & 255) / 255.0
        

        ui_minX = (minX / self.width) * 2 - 1
        ui_maxX = (maxX / self.width) * 2 - 1
        ui_minY = 1 - (maxY / self.height) * 2
        ui_maxY = 1 - (minY / self.height) * 2
        
        rect = Entity(
            model='cube',
            scale=(ui_maxX - ui_minX, ui_maxY - ui_minY, 0.001),
            position=((ui_minX + ui_maxX) / 2, (ui_minY + ui_maxY) / 2, -1),
            color=color.rgba(r, g, b, a),
            parent=camera.ui
        )
        
        self.ui_elements.append(rect)
        return rect
        
    def fillGradient(self, minX, minY, maxX, maxY, col1, col2):
        """Заполняет прямоугольную область градиентом"""
        a1 = (col1 >> 24 & 255) / 255.0
        r1 = (col1 >> 16 & 255) / 255.0
        g1 = (col1 >> 8 & 255) / 255.0
        b1 = (col1 & 255) / 255.0
        a2 = (col2 >> 24 & 255) / 255.0
        r2 = (col2 >> 16 & 255) / 255.0
        g2 = (col2 >> 8 & 255) / 255.0
        b2 = (col2 & 255) / 255.0
        
        ui_minX = (minX / self.width) * 2 - 1
        ui_maxX = (maxX / self.width) * 2 - 1
        ui_minY = 1 - (maxY / self.height) * 2
        ui_maxY = 1 - (minY / self.height) * 2
        
        vertices = [
            (ui_minX, ui_maxY, 0),
            (ui_maxX, ui_maxY, 0),
            (ui_maxX, ui_minY, 0),
            (ui_minX, ui_minY, 0)
        ]
        
        colors = [
            (r1, g1, b1, a1),
            (r1, g1, b1, a1),
            (r2, g2, b2, a2),
            (r2, g2, b2, a2)
        ]
        
        triangles = [0, 1, 2, 0, 2, 3]
        
        gradient_entity = Entity(
            model=Mesh(vertices=vertices, triangles=triangles, colors=colors, mode='triangle'),
            position=(0, 0, -1),
            parent=camera.ui
        )
        
        self.ui_elements.append(gradient_entity)
        return gradient_entity
    
    def drawCenteredString(self, text, x, y, color_val):
        font = self.modernclassic.font
        
        r = (color_val >> 16 & 255) / 255.0
        g = (color_val >> 8 & 255) / 255.0
        b = (color_val & 255) / 255.0
        text_color = ursina.color.rgb(r, g, b)
        
        ui_x = (x / self.width) * 2 - 1
        ui_y = 1 - (y / self.height) * 2
        
        text_entities = font.draw_shadow(
            text, 
            ui_x, 
            ui_y, 
            text_color=text_color,
            text_origin=0.5,
            size=0.6
        )
        
        self.ui_elements.extend(text_entities)
        return text_entities
    
    def drawString(self, text, x, y, color_val):
        font = self.modernclassic.font
        
        r = (color_val >> 16 & 255) / 255.0
        g = (color_val >> 8 & 255) / 255.0
        b = (color_val & 255) / 255.0
        text_color = ursina.color.rgb(r, g, b)
        
        ui_x = (x / self.width) * 2 - 1
        ui_y = 1 - (y / self.height) * 2
        
        text_entities = font.draw_shadow(
            text, 
            ui_x, 
            ui_y, 
            text_color=text_color,
            text_origin=0.0,
            size=0.6
        )
        
        self.ui_elements.extend(text_entities)
        return text_entities
    
    def updateEvents(self):
        if mouse.left:
            screen_x = int((mouse.position[0] + 1) * self.width / 2)
            screen_y = int((1 - mouse.position[1]) * self.height / 2)
            self.mouseClicked(screen_x, screen_y, 0)
        
        if mouse.right:
            screen_x = int((mouse.position[0] + 1) * self.width / 2)
            screen_y = int((1 - mouse.position[1]) * self.height / 2)
            self.mouseClicked(screen_x, screen_y, 1)
    
    def keyPressed(self, event_character, event_key):
        pass
    
    def mouseClicked(self, x, y, button):
        pass
    
    def tick(self):
        pass
    
    def cleanup(self):
        for element in self.ui_elements:
            if element and hasattr(element, '__iter__'):
                for sub_element in element:
                    if sub_element:
                        destroy(sub_element)
            elif element:
                destroy(element)
        
        self.ui_elements.clear()
    
    def onRemove(self):
        self.cleanup()
    
    @staticmethod
    def rgba(r, g, b, a=255):
        return (a << 24) | (r << 16) | (g << 8) | b
    
    @staticmethod
    def rgb(r, g, b):
        return Screen.rgba(r, g, b, 255)
