from LevelEditorCore.Data.data import SETTINGS_PATH
from PySide6 import QtWidgets
import yaml


class CloseState:
    def __init__(self, window, event):
        QtWidgets.QApplication.instance().processEvents()
        settings = {
            'romfs_path': str(window.rom_path),
            'output_path': str(window.out_path)
        }
        with open(SETTINGS_PATH, 'w') as f:
            yaml.dump(settings, f, sort_keys=False)
        event.accept()
