from PySide6 import QtCore, QtWidgets, QtGui


class LevelSelectLabel(QtWidgets.QLabel):
    selection = QtCore.Signal(str)

    def mousePressEvent(self, ev) -> None:
        if ev.button() == QtCore.Qt.MouseButton.LeftButton:
            ev.accept()
            self.selection.emit(self.text()) # emit level name that the user clicked
            return
        ev.ignore()
