from PySide6 import QtCore, QtWidgets, QtGui
from LevelEditorCore.Data.data import ACTOR_ICONS_PATH
from LevelEditorUI.Windows.LevelWindow.level_widgets import LevelSelectLabel
import os


class LevelSelectionWindow(QtWidgets.QDialog):
    selection = QtCore.Signal(str)

    def __init__(self, parent=None, rom_path=str, out_path=str):
        super().__init__(parent)
        self.setFixedSize(500, 400)

        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setGeometry(0, 0, self.width(), self.height())
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()

        level_list = set([f for f in os.listdir(os.path.join(rom_path, 'region_common/level')) \
                        if os.path.isdir(os.path.join(rom_path, 'region_common/level', f))])
        try:
            level_list.update([f for f in os.listdir(os.path.join(out_path, 'region_common/level')) \
                        if os.path.isdir(os.path.join(out_path, 'region_common/level', f))])
        except FileNotFoundError:
            pass # the user might not have saved any files yet
        finally:
            level_list = list(level_list)
            level_list.sort()

        r = 0
        c = 0
        for level in level_list: # work on level text later
            level_view = QtWidgets.QLabel(parent=scroll_area)
            level_view.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            level_view.resize(120, 80)
            level_view.setStyleSheet("background-color: blue") # placeholder for level icons/previews
            pix = QtGui.QPixmap(os.path.join(ACTOR_ICONS_PATH, "NoSprite.png"))
            pix = pix.scaled(level_view.width(), level_view.height(), 
                QtCore.Qt.AspectRatioMode.IgnoreAspectRatio, QtCore.Qt.TransformationMode.FastTransformation)
            level_view.setPixmap(pix)
            layout.addWidget(level_view, r, c)
            level_text = LevelSelectLabel(text=level, parent=scroll_area)
            level_text.selection.connect(self.levelPicked)
            level_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            level_text.resize(level_view.size())
            level_text.setStyleSheet("""background-color: transparent;
                                        color: white;""")
            # level_text.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            layout.addWidget(level_text, r, c)
            c += 1
            if c > 2: # limit horizontal column count to 3
                c = 0
                r += 1

        widget.setLayout(layout)
        scroll_area.setWidgetResizable(False)
        scroll_area.setWidget(widget)


    def levelPicked(self, level=str) -> None:
        self.selection.emit(level) # pass level selection to the main window
