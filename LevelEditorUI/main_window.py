from PySide6 import QtCore, QtWidgets
from LevelEditorUI.UI.ui_form import Ui_MainWindow
from LevelEditorUI.States.states import *
from LevelEditorCore.Data.data import *
import LevelEditorCore.Tools.conversions as convert
from pathlib import Path
import copy, random


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app_name) -> None:
        super (MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.app_name = app_name

        # initialize the editor state machine
        self.state = StateMachine(self)
        self.state.changeToSetup()


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
        self.state.changeToDraw(toggle_hide=True, hide_empty_sprites=self.ui.hideUnimportantCheck.isChecked())


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
            self.state.changeToRead(dragged_file=link)


    def closeEvent(self, event) -> None:
        self.state.changeToClose(event)
