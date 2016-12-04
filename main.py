#!/usr/bin/env python

import os
import sys
from pyqtgraph.Qt import QtCore, QtGui
from ui import UI
from solarized import solarized as sol
from collections import deque
import json

with open('config.json', 'r') as f:
    config = json.load(f)

channels = list()
for chan in config['channels']:
    channels.append(dict(legend=chan['legend'],
                         color=sol[chan['color']],
                         data=deque([0.0] * config['bufferSize'])))

if (config['inputStream'] == "simulation"):
    # just a simulation mode showing white noise on every channel.
    from simFetcher import SimFetcher
    fetcher = SimFetcher(channels)
elif (os.name == "posix"):
    # on Un*x systems, reading is very easy since ttys are simple files.
    from fileFetcher import FileFetcher
    fetcher = FileFetcher(channels, config['inputStream'])
elif (os.name == "nt"):
    # Windows still uses it's ugly COM port system.
    # So ComFetcher has to use the pyserial library to open serial ports.
    # pyserial expects a port like 'COM3' and a baudrate e.g. 921600
    from comFetcher import ComFetcher
    fetcher = ComFetcher(channels, config['inputStream'], config['baud'])
else:
    sys.exit("OS \"{}\" not supported (yet)!".format(os.name))

userInterface = UI(channels)

if __name__ == '__main__':
    if(sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
