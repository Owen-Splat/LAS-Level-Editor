from PySide6 import QtWidgets


class SaveState:
    def __init__(self, window):
        if not window.state.isEditMode():
            return

        path = window.file.parent
        path.mkdir(parents=True, exist_ok=True)

        window.saveActor(window.ui.listWidget.currentRow())

        try:
            with open(window.file, 'wb') as f:
                f.write(window.room_data.repack())
        except (ValueError, OverflowError) as e:
            window.showError(e.args[0])
        else:
            message = QtWidgets.QMessageBox()
            message.setWindowTitle(window.app_name)
            message.setText('File saved successfully')
            message.exec()
