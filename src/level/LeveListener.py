from abc import ABC, abstractmethod

class LevelListener(ABC):
    
    @abstractmethod
    def tileChanged(self, x, y, z):
        pass
    
    @abstractmethod
    def allChanged(self):
        pass
    
    @abstractmethod
    def lightColumnChanged(self, x, z, minY, maxY):
        pass