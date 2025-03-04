from PySide6 import QtCore, QtWidgets, QtGui


class IdleState:
    def __init__(self, window):
        # general variables reset
        window.file = ''
        window.save_location = ''
        window.room_data = None
        window.current_actor = -1
        window.next_actor = -1
        window.deleted = False
        window.actor_keys = []

        # clear actor info widgets
        window.ui.listWidget.clear()
        window.ui.listWidget.setEnabled(False)
        for i in range(8):
            window.ui.tableWidget.item(i, 0).setText('')
            window.ui.tableWidget.item(i, 1).setText('')
        window.ui.tableWidget.setEnabled(False)
        window.ui.dataType.clear()
        for c in window.ui.centralwidget.children():
            try:
                c.setEnabled(False)
            except AttributeError: # some objects won't have this attribute
                pass
        for field in window.ui.centralwidget.findChildren(QtWidgets.QLineEdit):
            field.setText('')

        # delete actor sprites
        for act in window.actor_sprites:
            act.deleteLater()
        window.actor_sprites = []

        # clear room layout tiles, do not delete because we want to keep these to draw future rooms
        for tile in window.tiles:
            tile.clear()

        window.setWindowTitle(window.app_name)
