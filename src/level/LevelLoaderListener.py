from abc import ABC, abstractmethod

class LevelLoaderListener(ABC):
    
    @abstractmethod
    def beginLevelLoading(self, title: str):
        pass
    
    @abstractmethod
    def levelLoadUpdate(self, status: str):
        pass
    
    @abstractmethod
    def levelLoadComplete(self):
        pass
