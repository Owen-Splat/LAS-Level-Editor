from PySide6 import QtCore, QtWidgets, QtGui
from LevelEditorUI.UI.ui_form import Ui_MainWindow
from LevelEditorUI.path_window import PathsWindow
from LevelEditorUI.custom_widgets import *
from LevelEditorUI.States.states import *
from LevelEditorCore.Data.data import *
import LevelEditorCore.Tools.FixedHash.leb as leb
import LevelEditorCore.Tools.conversions as convert
from pathlib import Path
import copy, random


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app_name) -> None:
        super (MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.app_name = app_name

        self.rom_path = Path()
        self.out_path = Path()
        self.actor_sprites = []

        # by default, hide objects without sprites
        self.hideEmptySprites = True
        self.ui.hideUnimportantCheck.setChecked(True)

        # accept drop events so that files can be opened by dragging them into the editor
        self.setAcceptDrops(True)

        self.tile_unit_size = 1.5 # the tile size by in-game units
        self.tile_pixel_size = 45 # how many pixels make up a tile
        self.user_snap_margin = 2
        self.snap_margin = self.tile_unit_size / self.user_snap_margin  # grid snap margin, by default it snaps to 1/2 a tile

        # menu bar signals (signals connect events to functions)
        self.ui.actionOpen.triggered.connect(self.fileOpen)
        self.ui.actionSave.triggered.connect(self.fileSave)
        self.ui.actionSaveAs.triggered.connect(self.fileSaveAs)
        self.ui.actionClose.triggered.connect(self.fileClose)

        # widget signals
        self.ui.listWidget.currentRowChanged.connect(self.selectedActorChanged)
        self.ui.dataType.currentIndexChanged.connect(self.updateActorType)
        self.ui.addButton.clicked.connect(self.copyActor)
        self.ui.delButton.clicked.connect(self.deleteButton_Clicked)
        self.ui.showButton.clicked.connect(self.toggleActor)
        self.ui.hideUnimportantCheck.clicked.connect(self.toggleNoModelObjects)
        self.ui.gridCheck.clicked.connect(self.toggleGrid)

        # change position and rotation lineEdits to custom class for moving actors via arrow keys
        for line in self.findChildren(QtWidgets.QLineEdit):
            if line.objectName().startswith('dataPos'):
                line.__class__ = PosLineEdit
            elif line.objectName().startswith('dataRot'):
                line.__class__ = RotLineEdit

        # set up the roomView and tiles that will represent the room layout
        # we use a custom class and setAcceptDrops so that actor sprites can be dragged
        self.ui.roomFrame.__class__ = roomView
        self.ui.roomFrame.setAcceptDrops(True)

        # LAS rooms are defined by 10x8 tiles from a top-down view
        # Sidecroller rooms are 10x2 tiles, but will be drawn the same, represented as front-facing
        self.tiles = []
        for i in range(8):
            for b in range(10):
                tile = QtWidgets.QLabel(self.ui.roomFrame)
                tile.setGeometry((self.tile_pixel_size * b), (self.tile_pixel_size * i), self.tile_pixel_size, self.tile_pixel_size)
                self.tiles.append(tile)

        # raise the grid and make mouse events go through it, then hide it by default
        self.ui.gridWidget.raise_()
        self.ui.gridWidget.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.ui.gridWidget.hide()

        # make parameter names in the table unable to be edited
        for i in range(8):
            info_item = QtWidgets.QTableWidgetItem()
            info_item.setFlags(info_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.ui.tableWidget.setItem(i, 0, info_item)
            data_item = QtWidgets.QTableWidgetItem()
            self.ui.tableWidget.setItem(i, 1, data_item)

        # set stylesheet
        self.setStyleSheet(LIGHT_STYLE)

        # initialize the editor state machine
        self.state = StateMachine(self)

        # for now, the window is fixed size until all core features are working, then we can work more on UI
        self.setFixedSize(self.size())
        self.show()
        self.prepareSettings()


    def fileOpen(self, dragged_file=None) -> None:
        if dragged_file:
            path = dragged_file
        else:
            dir = self.rom_path / 'region_common/level'
            if self.file:
                dir = self.file.parent
            path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', str(dir), "Room files (*.leb)")[0]
            if not path.endswith(".leb"):
                return

        self.state.changeToIdle() # temp idle state to reset everything

        # now we want to store the file location, but in the output dir rather than romfs dir
        path = Path(path)
        file_name = path.name
        level_name = file_name.split('_')[0]
        self.file = self.out_path / 'region_common/level' / level_name / file_name

        try:
            with open(path, 'rb') as f:
                self.room_data = leb.Room(f.read())
        except (FileNotFoundError, ValueError) as e:
            self.showError(e.args[0])
        else:
            self.enableEditor()
            self.setWindowTitle(f"{self.app_name} - {path.stem}")
            self.topleft = [self.room_data.grid.info.x_coord, self.room_data.grid.info.z_coord]
            self.ui.listWidget.setEnabled(True)
            self.next_actor = 0
            self.toggle_hide = True
            self.state.changeToDraw()


    def fileSave(self) -> None:
        if not self.state.isEditMode():
            return

        path = self.file.parent
        path.mkdir(parents=True, exist_ok=True)

        self.saveActor(self.ui.listWidget.currentRow())

        try:
            with open(self.file, 'wb') as f:
                f.write(self.room_data.repack())
        except (ValueError, OverflowError) as e:
            self.showError(e.args[0])
        else:
            message = QtWidgets.QMessageBox()
            message.setWindowTitle(self.app_name)
            message.setText('File saved successfully')
            message.exec()


    def fileSaveAs(self) -> None:
        if not self.state.isEditMode():
            return

        path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File As',
            self.file.parent / self.file.stem, "Room files (*.leb)")[0]
        
        if path:
            self.saveActor(self.ui.listWidget.currentRow())
            try:
                actor_keys = []
                for act in self.room_data.actors:
                    if act.key not in actor_keys:
                        actor_keys.append(act.key)
                    else:
                        raise ValueError('Actors cannot share the same Hex!')
                with open(path, 'wb') as f:
                    f.write(self.room_data.repack())
            except (ValueError, OverflowError) as e:
                self.showError(e.args[0])
            else:
                self.file = Path(path)
                message = QtWidgets.QMessageBox()
                message.setWindowTitle(self.app_name)
                message.setText('File saved successfully')
                message.exec()


    def fileClose(self):
        self.state.changeToIdle()


    def prepareSettings(self) -> None:
        self.paths_valid = False
        open_paths = False

        if SETTINGS['romfs_path']:
            rom_path = Path(SETTINGS['romfs_path'])
            if rom_path != Path() and rom_path.exists():
                self.rom_path = rom_path
            else:
                open_paths = True
        else:
            open_paths = True

        if SETTINGS['output_path']:
            out_path = Path(SETTINGS['output_path'])
            if out_path != Path() and out_path.exists():
                self.out_path = out_path
            else:
                open_paths = True
        else:
            open_paths = True

        if open_paths:
            self.showPathsWindow()
        else:
            self.paths_valid = True


    def selectedActorChanged(self, current_row) -> None:
        if not self.state.isEditMode() or self.deleted:
            return

        if (current_row != -1) and (current_row != self.current_actor):
            self.next_actor = current_row
            self.state.changeToDraw()


    def saveEntryData(self) -> None:
        pass


    def saveActor(self, previous=-1) -> None:
        if previous != -1:
            try:
                act = self.room_data.actors[previous]
                act.type = int(ACTORS[self.ui.dataType.currentText()], 16)
                act.position.x = convert.strToFloat(self.ui.dataPos_X.text())
                act.position.y = convert.strToFloat(self.ui.dataPos_Y.text())
                act.position.z = convert.strToFloat(self.ui.dataPos_Z.text())
                act.rotation.x = convert.strToFloat(self.ui.dataRot_X.text())
                act.rotation.y = convert.strToFloat(self.ui.dataRot_Y.text())
                act.rotation.z = convert.strToFloat(self.ui.dataRot_Z.text())
                act.scale.x = convert.strToFloat(self.ui.dataScale_X.text())
                act.scale.y = convert.strToFloat(self.ui.dataScale_Y.text())
                act.scale.z = convert.strToFloat(self.ui.dataScale_Z.text())

                for i in range(8):
                    v = self.ui.tableWidget.item(i, 1).text()
                    if v.isdigit():
                        act.parameters[i] = int(v)
                    else:
                        try:
                            exec(f"act.parameters[i] = convert.strToFloat(v)")
                        except ValueError:
                            exec(f"act.parameters[i] = bytes(v, 'utf-8')")
                
                act.switches[0] = (self.ui.comboBox.currentIndex(), int(self.ui.dataSwitches_0.text()))
                act.switches[1] = (self.ui.comboBox_2.currentIndex(), int(self.ui.dataSwitches_1.text()))
                act.switches[2] = (self.ui.comboBox_3.currentIndex(), int(self.ui.dataSwitches_2.text()))
                act.switches[3] = (self.ui.comboBox_4.currentIndex(), int(self.ui.dataSwitches_3.text()))

                self.saveEntryData()
            
            except ValueError as e:
                print('error at saveActor', f"current actor: {self.current_actor}")
                self.showError(e.args[0])
                self.ui.listWidget.setCurrentRow(previous)
            
            except IndexError:
                pass


    def copyActor(self) -> None:
        """Makes a copy of the currently selected actor. The new actor is then given a unique ID"""

        if not self.state.isEditMode():
            return

        try:
            self.saveActor(self.current_actor)
            act = copy.deepcopy(self.room_data.actors[self.current_actor])
            while act.key in self.actor_keys:
                act.key = random.getrandbits(64)
            self.room_data.actors.append(act)
            self.next_actor = self.ui.listWidget.count()
            self.state.changeToDraw()
        except ValueError as e:
            self.showError(e.args[0])
        except IndexError:
            pass


    def deleteButton_Clicked(self) -> None:
        if not self.state.isEditMode():
            return

        if self.room_data.actors[self.current_actor].type not in REQUIRED_ACTORS:
            self.deleteActor()
        else:
            if len([act for act in self.room_data.actors if act.type == self.room_data.actors[self.current_actor].type]) > 1:
                self.deleteActor()
            else:
                self.showError('Levels require at least 1 actor of this type')


    def deleteActor(self) -> None:
        if not self.state.isEditMode():
            return

        # before deleting the actor, we need to adjust actor references
        for act in self.room_data.actors:
            i = 0
            while i < len(act.relationships.section_1):
                try:
                    index = act.relationships.section_1[i][1]
                    if index > self.current_actor:
                        act.relationships.section_1[i][1] -=1
                    elif index == self.current_actor:
                        act.relationships.section_1.pop(i)
                        act.relationships.num_entries_1 -= 1
                        continue
                    i += 1
                except IndexError:
                    print('section 1:' + i)

            i = 0
            while i < len(act.relationships.section_3):
                try:
                    index = act.relationships.section_3[i]
                    if index > self.current_actor:
                        act.relationships.section_3[i] -= 1
                    elif index == self.current_actor:
                        act.relationships.section_3.pop(i)
                        act.relationships.num_entries_3 -= 1
                        continue
                    i += 1
                except IndexError:
                    print('section 3:' + i)

        self.actor_keys.remove(self.room_data.actors[self.current_actor].key)
        del self.room_data.actors[self.current_actor]
        if self.current_actor == self.ui.listWidget.count() - 1:
            self.next_actor = self.current_actor - 1
        self.deleted = True
        self.state.changeToDraw()


    def toggleActor(self) -> None:
        if not self.state.isEditMode():
            return

        act = self.room_data.actors[self.current_actor]
        act.visible = not act.visible
        self.state.changeToDraw()


    def toggleShowButton(self) -> None:
        if not self.state.isDrawMode():
            return

        if self.room_data.actors[self.current_actor].visible:
            self.ui.showButton.setText("Hide")
        else:
            self.ui.showButton.setText("Show")


    def toggleNoModelObjects(self) -> None:
        if not self.state.isEditMode():
            return

        self.hideEmptySprites = self.ui.hideUnimportantCheck.isChecked()
        self.toggle_hide = True
        self.state.changeToDraw()


    def toggleGrid(self) -> None:
        if self.ui.gridCheck.isChecked():
            self.ui.gridWidget.show()
        else:
            self.ui.gridWidget.hide()


    def updateActorType(self) -> None:
        """Runs when the type field is edited and updates the actor"""

        if not self.state.isEditMode():
            return

        act = self.room_data.actors[self.current_actor]
        new_type = ACTOR_NAMES.index(self.ui.dataType.currentText())

        if new_type == act.type: # do not do anything if the type is not being changed
            return

        if not self.room_data.actors[self.current_actor].type in REQUIRED_ACTORS:
            act.type = new_type
        else:
            if len([act for act in self.room_data.actors if act.type == self.room_data.actors[self.current_actor].type]) > 1:
                act.type = new_type
            else:
                self.showError('Levels require at least 1 actor of this type')
                self.ui.dataType.setCurrentIndex(
                    self.ui.dataType.findText(ACTOR_NAMES[ACTOR_IDS.index(hex(act.type))], QtCore.Qt.MatchExactly))

        self.state.changeToDraw()


    def enableEditor(self) -> None:
        fields = self.ui.centralwidget.children()
        for field in fields:
            try:
                field.setProperty('enabled', True)
            except AttributeError: # some objects won't have this attribute
                pass
        abc_actors = list(copy.deepcopy(ACTORS))
        abc_actors.sort()
        for actor in abc_actors:
            if not actor.startswith(('Player', 'null')):
                self.ui.dataType.addItem(actor)


    def showError(self, error_message) -> None:
        """Opens a new QMessageBox with error_message as the text"""

        message = QtWidgets.QMessageBox()
        message.setWindowTitle(self.app_name)
        message.setText(error_message)
        message.exec()


    def dragEnterEvent(self, event) -> None:
        """Allows dragging level files into this tool. Dropping the file is handled in dropEvent()"""

        if event.mimeData().hasUrls():
            links = [str(l.toLocalFile()) for l in event.mimeData().urls() if l.toLocalFile().endswith(".leb")]
            if links:
                event.accept()
                return
        event.ignore()


    def dropEvent(self, event) -> None:
        """Allows dropping level files into this tool. Dragging the file is handed in dragEnterEvent()"""

        event.accept()
        if event.mimeData().hasUrls():
            link = [str(l.toLocalFile()) for l in event.mimeData().urls() if l.toLocalFile().endswith(".leb")][0]
            self.fileOpen(link)
            return


    def closeEvent(self, event) -> None:
        QtWidgets.QApplication.instance().processEvents()
        settings = {
            'romfs_path': str(self.rom_path),
            'output_path': str(self.out_path)
        }
        with open(SETTINGS_PATH, 'w') as f:
            yaml.dump(settings, f, sort_keys=False)
        event.accept()


    def showPathsWindow(self) -> None:
        p_window = PathsWindow(self)
        p_window.setWindowTitle(self.app_name)
        p_window.setStyleSheet(LIGHT_STYLE)
        p_window.give_settings.connect(self.obtainSettings)
        p_window.exec()


    def obtainSettings(self, settings) -> None:
        self.paths_valid = settings[0]
        if self.paths_valid:
            self.rom_path = settings[1]
            self.out_path = settings[2]
        else:
            self.deleteLater()
