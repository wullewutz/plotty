#!/usr/bin/env python

import threading
import sys
import time

class FileFetcher(threading.Thread):

    def __init__(self, chans, fil):
        threading.Thread.__init__(self)
        self.chans = chans
        self.stream = open(fil, 'r')
        #self.stream = open("/dev/ttyUSB0", 'r') #Linux style
        self.stream.readline() #read and forget to avoid data-glitches on first read.
        self.setDaemon(True)
        self.start()
        
    def run (self):
        while (True):
            time.sleep(0.01)
            for line in self.stream:
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
