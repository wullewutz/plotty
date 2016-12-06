#!/usr/bin/env python

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from solarized import solarized as sol
from math import log10, pow
import sys


class UI():
    def __init__(self, chans):
        self.app  = QtGui.QApplication(sys.argv)
        self.win  = QtGui.QWidget()
        palette = self.win.palette()
        palette.setColor(self.win.backgroundRole(),
                         QtGui.QColor(sol['base03'][0],
                                      sol['base03'][1],
                                      sol['base03'][2]))
        palette.setColor(self.win.foregroundRole(),
                         QtGui.QColor(sol['base0'][0],
                                      sol['base0'][1],
                                      sol['base0'][2]))
        self.win.setPalette(palette)
        self.layout = QtGui.QGridLayout()
        self.plotter = Plotter(chans)
        self.ctrl  = Ctrl(self.plotter.p, len(chans[0]['data']), self.plotter.run, self.plotter.pause)
        self.layout.addWidget(self.ctrl , 2, 1)
        self.layout.addWidget(self.plotter, 1, 1)
        self.win.setLayout(self.layout)
        self.win.show()
        sys.exit(self.app.exec_())
        
class Plotter(pg.GraphicsWindow):
    def __init__(self, chans, parent = None):
        pg.setConfigOption('background', sol['base03'])
        pg.setConfigOption('foreground', sol['base01'])
        super(Plotter, self).__init__(parent)
        self.bufSize = len(chans[0]['data'])
        self.chans = chans
        self.p = self.addPlot()
        self.p.addLegend()
        self.p.showGrid(x=True, y=True)
        self.curves = list()
        for chan in chans:
            self.curves.append(self.p.plot(chan['data'], name=chan['legend'], pen=chan['color']))
        self.timer = self.startTimer(5)
    def timerEvent(self, event):
        for curve, chan in zip(self.curves, self.chans):
            curve.setData(chan['data'])
    def pause(self):
        self.killTimer(self.timer)
    def run(self):
        self.timer = self.startTimer(5)

class Ctrl(QtGui.QWidget):
    WHEEL_SNAP=20
    def __init__ (self, zoomablePlot, bufSize, runCallback, pauseCallback, parent = None):
        super(Ctrl, self).__init__(parent)
        self.bufSize = bufSize
        self.zoomablePlot = zoomablePlot
        self.runCallback = runCallback
        self.pauseCallback = pauseCallback
        layout = QtGui.QGridLayout()
        layout.setAlignment (QtCore.Qt.AlignCenter)
        self.pauseButton = PicButton(" ", QtGui.QPixmap("buttons/pause.png"), QtGui.QPixmap("buttons/play.png"))
        self.pauseButton.toggled.connect(self.onPauseButtonChanged)
        layout.addWidget(self.pauseButton, 2, 1)
        self.l1 = QtGui.QLabel("Zoom Level [Samples]")
        self.l1.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.l1, 1, 2)
        self.d1 = QtGui.QDial()
        self.d1.setMinimum(log10(10)*Ctrl.WHEEL_SNAP)
        self.d1.setMaximum(log10(self.bufSize)*Ctrl.WHEEL_SNAP)
        self.d1.setValue(log10(self.bufSize/20)*Ctrl.WHEEL_SNAP)
        layout.addWidget(self.d1, 2, 2)
        self.d1.valueChanged.connect(self.onZoomValuechange)
        self.l2 = QtGui.QLabel(str(self.d1.value()))
        self.l2.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.l2, 3, 2)
        self.setLayout(layout)
        self.onZoomValuechange()  #call this right at the beginning for accurate axis scaling
    def onZoomValuechange (self):
        zoomValue = int(round(pow(10, self.d1.value()/Ctrl.WHEEL_SNAP)))
        self.l2.setText(str(zoomValue))
        self.zoomablePlot.setXRange(self.bufSize - zoomValue, self.bufSize)
    def onPauseButtonChanged (self):
        if self.pauseButton.isChecked():
            self.pauseCallback()
        else:
            self.runCallback()
        
class PicButton(QtGui.QPushButton):
    def __init__(self, hotkey, pixmap, pixmap_pressed, parent=None):
        super(PicButton, self).__init__(hotkey, parent)
        self.setCheckable(True)
        self.pixmap = pixmap
        self.pixmap_pressed = pixmap_pressed
        self.pressed.connect(self.update)
        self.released.connect(self.update)
    def paintEvent(self, event):
        if self.isChecked():
            pix = self.pixmap_pressed
        else:
            pix = self.pixmap
        painter = QtGui.QPainter(self)
        painter.drawPixmap(event.rect(), pix)
    def enterEvent(self, event):
        self.update()
    def leaveEvent(self, event):
        self.update()
    def sizeHint(self):
        return QtCore.QSize(100, 100)
