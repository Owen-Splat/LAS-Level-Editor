#!/usr/bin/env python3

from PySide6 import QtCore, QtWidgets, QtGui
from LevelEditorUI.Window.main_window import MainWindow
from LevelEditorCore.Data.data import RUNNING_FROM_SOURCE, ICONS_PATH
import sys, os

def interruptHandler(sig, frame):
    sys.exit(0)

# Allow keyboard interrupts
import signal
signal.signal(signal.SIGINT, interruptHandler)

# Set app id so the custom taskbar icon will show while running from source
if RUNNING_FROM_SOURCE:
    try:
        from ctypes import windll
        windll.shell32.SetCurrentProcessExplicitAppUserModelID("LANS_Level_Editor")
    except AttributeError:
        pass # Ignore for versions of Windows before Windows 7
    except ImportError:
        if sys.platform != 'linux': raise

build_icon = "icon.ico"
if sys.platform == "darwin": # mac
    build_icon = "icon.icns"

app = QtWidgets.QApplication([])
app.setWindowIcon(QtGui.QIcon(os.path.join(ICONS_PATH, build_icon)))

timer = QtCore.QTimer()
timer.start(100)
timer.timeout.connect(lambda: None)

window = MainWindow(app_name="Link's Awakening Remake Level Editor")
sys.exit(app.exec())
