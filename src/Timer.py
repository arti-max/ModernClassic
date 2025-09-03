import time


class Timer:
    NS_PER_SECOND: int = 1000000000
    MAX_NS_PER_UPDATE: int = 1000000000
    MAX_TICKS_PER_UPDATE: int = 100
    
    def __init__(self, tps):
        self.lastTime: int = time.time_ns()
        self.timeScale: float = 1.0
        self.fps: float = 0.0
        self.passedTime: float = 0.0
        self.ticks: int = 0
        self.partialTicks: float = 0.0
        
        self.ticksPerSecond = tps
        
    def advanceTime(self):
        now: int = time.time_ns()
        passedNs: int = now - self.lastTime
        self.lastTime = now
        
        passedNs = max(0, passedNs)
        passedNs = min(Timer.MAX_NS_PER_UPDATE, passedNs)
        
        self.fps = float(Timer.NS_PER_SECOND / passedNs)
        
        self.passedTime += passedNs * self.timeScale * self.ticksPerSecond / Timer.NS_PER_SECOND
        self.ticks = int(self.passedTime)
        
        self.ticks = min(Timer.MAX_TICKS_PER_UPDATE, self.ticks)
        
        self.passedTime -= self.ticks
        self.partialTicks = self.passedTime