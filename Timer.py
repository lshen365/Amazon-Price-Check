import time

class TrackTime:
    def __init__(self,start,timeDelay):
        self.initialTime = start
        self.delay = timeDelay
    def waitSec(self):
        print(time.time())
        time.sleep(self.delay-((time.time()-self.initialTime)%self.delay))
