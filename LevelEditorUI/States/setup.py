from LevelEditorUI.path_window import PathsWindow
from LevelEditorUI.custom_widgets import *
from LevelEditorCore.Data.data import *
from PySide6 import QtWidgets
from pathlib import Path


class SetupState:
    def __init__(self, window) -> None:
        window.rom_path = Path()
        window.out_path = Path()
        window.actor_sprites = []

        window.tile_unit_size = 1.5 # the tile size by in-game units
        window.tile_pixel_size = 45 # how many pixels make up a tile
        window.user_snap_margin = 2
        window.snap_margin = window.tile_unit_size / window.user_snap_margin  # grid snap margin, by default it snaps to 1/2 a tile

        # by default, hide objects without sprites
        window.ui.hideUnimportantCheck.setChecked(True)

        # accept drop events so that files can be opened by dragging them into the editor
        window.setAcceptDrops(True)

        # change position and rotation lineEdits to custom class for moving actors via arrow keys
        for line in window.findChildren(QtWidgets.QLineEdit):
            if line.objectName().startswith('dataPos'):
                line.__class__ = PosLineEdit
            elif line.objectName().startswith('dataRot'):
                line.__class__ = RotLineEdit

        # set up the roomView and tiles that will represent the room layout
        # we use a custom class and setAcceptDrops so that actor sprites can be dragged
        window.ui.roomFrame.__class__ = roomView
        window.ui.roomFrame.setAcceptDrops(True)

        # LAS rooms are defined by 10x8 tiles from a top-down view
        # Sidecroller rooms are 10x2 tiles, but will be drawn the same, represented as front-facing
        window.tiles = []
        for i in range(8):
            for b in range(10):
                tile = QtWidgets.QLabel(window.ui.roomFrame)
                tile.setGeometry((window.tile_pixel_size * b), (window.tile_pixel_size * i), window.tile_pixel_size, window.tile_pixel_size)
                window.tiles.append(tile)

        # raise the grid and make mouse events go through it, then hide it by default
        window.ui.gridWidget.raise_()
        window.ui.gridWidget.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        window.ui.gridWidget.hide()

        # make parameter names in the table unable to be edited
        for i in range(8):
            info_item = QtWidgets.QTableWidgetItem()
            info_item.setFlags(info_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            window.ui.tableWidget.setItem(i, 0, info_item)
            data_item = QtWidgets.QTableWidgetItem()
            window.ui.tableWidget.setItem(i, 1, data_item)

        # menu bar signals (signals connect events to functions)
        window.ui.actionOpen.triggered.connect(lambda x: window.state.changeToRead())
        window.ui.actionSave.triggered.connect(lambda x: window.state.changeToSave())
        window.ui.actionClose.triggered.connect(lambda x: window.state.changeToIdle())

        # widget signals
        window.ui.listWidget.currentRowChanged.connect(window.selectedActorChanged)
        window.ui.dataType.currentIndexChanged.connect(window.updateActorType)
        window.ui.addButton.clicked.connect(window.copyActor)
        window.ui.delButton.clicked.connect(window.deleteButton_Clicked)
        window.ui.showButton.clicked.connect(window.toggleActor)
        window.ui.hideUnimportantCheck.clicked.connect(window.toggleNoModelObjects)
        window.ui.gridCheck.clicked.connect(window.toggleGrid)

        # set stylesheet
        window.setStyleSheet(LIGHT_STYLE)

        # for now, the window is fixed size until all core features are working, then we can work more on UI
        window.setFixedSize(window.size())
        window.show()
        self.window = window
        self.prepareSettings()


    def prepareSettings(self) -> None:
        self.window.paths_valid = False
        open_paths = False

        if SETTINGS['romfs_path']:
            rom_path = Path(SETTINGS['romfs_path'])
            if rom_path != Path() and rom_path.exists():
                self.window.rom_path = rom_path
            else:
                open_paths = True
        else:
            open_paths = True

        if SETTINGS['output_path']:
            out_path = Path(SETTINGS['output_path'])
            if out_path != Path() and out_path.exists():
                self.window.out_path = out_path
            else:
                open_paths = True
        else:
            open_paths = True

        if open_paths:
            self.showPathsWindow()
        else:
            self.window.paths_valid = True


    def showPathsWindow(self) -> None:
        p_window = PathsWindow(self.window)
        p_window.setWindowTitle(self.window.app_name)
        p_window.setStyleSheet(LIGHT_STYLE)
        p_window.give_settings.connect(self.obtainSettings)
        p_window.exec()


    def obtainSettings(self, settings) -> None:
        self.window.paths_valid = settings[0]
        if self.window.paths_valid:
            self.window.rom_path = settings[1]
            self.window.out_path = settings[2]
        else:
            self.window.deleteLater()
