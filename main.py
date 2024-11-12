#!/usr/bin/env python3

from PySide6 import QtCore, QtWidgets
import LevelEditorUI.main_window as window
import sys

def interruptHandler(sig, frame):
    sys.exit(0)

# Allow keyboard interrupts
import signal
signal.signal(signal.SIGINT, interruptHandler)

app = QtWidgets.QApplication([])
app.setStyle('windowsvista')

timer = QtCore.QTimer()
timer.start(100)
timer.timeout.connect(lambda: None)

m = window.MainWindow(app_name='LAS Level Editor')
sys.exit(app.exec())
