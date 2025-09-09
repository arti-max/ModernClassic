from src.gui.Screen import Screen
from src.gui.Button import Button
from ursina import mouse

class PauseScreen(Screen):
    def __init__(self): pass
        
    def init(self, mc, w, h):
        super().init(mc, w, h)
        self.buttons = []
        
        self.buttons.append(Button(0, self.width  / 2 - 100, self.height / 3 + 0, 200, 20, "Generate new level"))
        self.buttons.append(Button(1, self.width  / 2 - 100, self.height / 3 + 0, 200, 20, "Save level..."))
        self.buttons.append(Button(2, self.width  / 2 - 100, self.height / 3 + 0, 200, 20, "Load level..."))
        self.buttons.append(Button(3, self.width  / 2 - 100, self.height / 3 + 0, 200, 20, "Back to game"))
        
        
    def mouseClicked(self, x, y, button):
        if (button == 0):
            for i in range(0, len(self.buttons)):
                button = self.buttons[i]
                if (x >= button.x and y >= button.y and x < button.x + button.w and y < button.y + button.h):
                    self.buttonClicked(button)
                    
    
    def buttonClicked(self, button: Button):
        if (button.id == 0):
            self.modernclassic.generateNewLevel()
            self.modernclassic.setScreen(None)
            self.modernclassic.grabMouse()
            
        if (button.id == 3):
            self.modernclassic.setScreen(None)
            self.modernclassic.grabMouse()
            
    def render(self, xMouse, yMouse):
        self.fillGradient(0, 0, self.width, self.height, 537199872, -1607454624)
        
        for i in range(0, len(self.buttons)):
            button = self.buttons[i]
            self.fill(button.x - 1, button.y - 1, button.x + button.w + 1, button.y + button.h + 1, -16777216)
            if (xMouse >= button.x and yMouse >= button.y and xMouse < button.x + button.w and yMouse < button.y + button.h):
                self.fill(button.x - 1, button.y - 1, button.x + button.w + 1, button.y + button.h + 1, -6250336)
                self.fill(button.x, button.y, button.x + button.w, button.y + button.h, -8355680)
                self.drawCenteredString(button.msg, button.x + button.w / 2, button.y + (button.h - 8) / 2, 16777120)
            else:
                self.fill(button.x, button.y, button.x + button.w, button.y + button.h, -9408400)
                self.drawCenteredString(button.msg, button.x + button.w / 2, button.y + (button.h - 8) / 2, 14737632)