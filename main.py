#!/usr/bin/env python3

from PySide6 import QtWidgets
import Ui.main_window as window
import sys

app = QtWidgets.QApplication([])
app.setStyle('Fusion')

m = window.MainWindow()
sys.exit(app.exec())
