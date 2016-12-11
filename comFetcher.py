#!/usr/bin/env python

import threading
import sys
from serial import Serial 

class ComFetcher(threading.Thread):

    def __init__(self, chans, comPort, baud):
        threading.Thread.__init__(self)
        self.chans = chans
        self.stream = Serial(comPort, baud, timeout=0)
        self.stream.readline() #read and forget to avoid data-glitches on first read.
        self.setDaemon(True)
        self.start()
        
    def run (self):
        while (True):
            while (self.stream.inWaiting() > 50):
                line = self.stream.readline()
                try:
                    data = [float(val) for val in line.split()]
                except ValueError:
                    print("ValueError " + str(line))
                    continue
                if len(data) > len(self.chans):
                    print ("Wrong length!!!: " + str(line))
                    continue
                for chan, dat in zip(self.chans, data):
                    chan['data'].popleft()
                    chan['data'].append(dat)
