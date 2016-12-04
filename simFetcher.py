#!/usr/bin/env python

import threading
import sys
import time
from random import random
from math import sin

class SimFetcher(threading.Thread):

    def __init__(self, chans):
        threading.Thread.__init__(self)
        self.chans = chans
        self.setDaemon(True)
        self.start()
        self.x = 0.0;
    def run (self):
        while (True):
            time.sleep(0.001) #Simulation mode works at 1000Hz sample rate.
            self.x += 0.1
            for chan, offset in zip(self.chans, range(0, len(self.chans))):
                chan['data'].popleft()
                chan['data'].append(2*sin(self.x)+sin(self.x*3)+sin(self.x*10)+2*random()+10*offset)
