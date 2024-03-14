from PySide6 import QtCore, QtWidgets
from LevelEditorUI.ui_form import Ui_MainWindow
import LevelEditorCore.Tools.leb as leb
import numpy as np
import copy, os, sys, yaml

if getattr(sys, "frozen", False):
    root_path = os.path.dirname(sys.executable)
else:
    root_path = os.path.dirname(os.path.dirname(__file__))

DATA_PATH = os.path.join(root_path, 'LevelEditorCore/Data')
with open(os.path.join(DATA_PATH, 'actors.yml'), 'r') as f:
    actor_list = yaml.safe_load(f)

ACTORS = {}
for i, actor in enumerate(actor_list):
    ACTORS[actor['name']] = hex(i)

ACTOR_IDS = list(ACTORS.values())
ACTOR_NAMES = list(ACTORS.keys())
REQUIRED_ACTORS = [0x185]
# MapStatic



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super (MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.file = ''
        self.file_loaded = False
        self.save_location = ''

        self.data_viewed = False
        self.room_data = None
        self.new_key = -1
        self.current_actor = -1
        self.current_section = -1
        self.current_entry = -1
        self.deleted = False
        self.manual_editing = False
        
        self.ui.actionOpen.triggered.connect(self.fileOpen)
        self.ui.actionSave.triggered.connect(self.fileSave)
        self.ui.actionSaveAs.triggered.connect(self.fileSaveAs)
        self.ui.actionClose.triggered.connect(self.fileClose)
        self.ui.listWidget.currentItemChanged.connect(self.displayActorInfo)
        self.ui.dataType.currentIndexChanged.connect(self.updateActorType)
        self.ui.addButton.clicked.connect(self.addActor)
        self.ui.delButton.clicked.connect(self.deleteButton_Clicked)
        self.ui.tabWidget_2.currentChanged.connect(self.saveEntryData)
        self.ui.dataCurrentEntry.valueChanged.connect(self.displayEntryInfo)
        # self.ui.dataEntryActor.valueChanged.connect(self.updateSect1CurrentEntry)
        self.ui.dataCurrentEntry_2.valueChanged.connect(self.displayEntryInfo)
        # self.ui.dataEntryRail.valueChanged.connect(self.updateSect2CurrentEntry)
        # self.ui.dataEntryPoint.valueChanged.connect(self.updateSect2CurrentEntry)
        self.ui.dataCurrentEntry_3.valueChanged.connect(self.displayEntryInfo)
        # self.ui.dataEntryActor_2.valueChanged.connect(self.updateSect3CurrentEntry)
        
        self.setFixedSize(800, 600)
        self.setWindowTitle('LAS Level Editor')
        self.show()
    


    def fileOpen(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',
            os.path.dirname(self.file) if self.file_loaded else '', "Room files (*.leb)")[0]
        if not path:
            return
        
        self.fileClose()
        self.file = path
        self.manual_editing = False

        try:
            with open(path, 'rb') as f:
                self.room_data = leb.Room(f.read())
        except (FileNotFoundError, ValueError) as e:
            self.showError(e.args[0])
        else:
            self.file_loaded = True
            self.setWindowTitle(os.path.basename(path))
            # self.ui.dataEntryActor.setMaximum(len(self.room_data.actors))
            # self.ui.dataEntryActor_2.setMaximum(len(self.room_data.actors))
            self.ui.listWidget.setEnabled(True)
            self.ui.listWidget.clear()
            keys = []
            for i,act in enumerate(self.room_data.actors):
                keys.append(act.key)
                self.ui.listWidget.addItem(f'{ACTOR_NAMES[ACTOR_IDS.index(hex(act.type))]} ({i})')
            self.new_key = max(keys) + 1
            self.ui.listWidget.setCurrentRow(0)
    


    def fileSave(self):
        if self.file_loaded:
            path = os.path.dirname(self.file)
            if not os.path.exists(path):
                os.makedirs(path)
            
            self.saveActor(self.ui.listWidget.currentRow())

            try:
                with open(self.file, 'wb') as f:
                    f.write(self.room_data.repack())
            except (ValueError, OverflowError) as e:
                self.showError(e.args[0])
            else:
                message = QtWidgets.QMessageBox()
                message.setWindowTitle('LAS Level Editor')
                message.setText('File saved successfully')
                message.exec()



    def fileSaveAs(self):
        if self.file_loaded:
            path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File As',
                os.path.join(self.save_location, os.path.basename(self.file)), "Room files (*.leb)")[0]
            
            if path:
                self.save_location = os.path.dirname(path)
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
                    message = QtWidgets.QMessageBox()
                    message.setWindowTitle('LAS Level Editor')
                    message.setText('File saved successfully')
                    message.exec()
    


    def fileClose(self):
        self.file = ''
        self.file_loaded = False
        self.save_location = ''
        self.manual_editing = False
        self.current_actor = -1
        self.current_section = -1
        self.current_entry = -1
        self.room_data = None
        self.ui.listWidget.clear()
        self.ui.listWidget.setEnabled(False)
        self.ui.dataType.clear()
        self.data_viewed = False
        for c in self.ui.groupBox.children():
            c.setEnabled(False)
        for field in self.ui.groupBox.findChildren(QtWidgets.QLineEdit):
            field.setText('')
        self.setWindowTitle('Level Editor')



    def displayActorInfo(self):
        if not self.file_loaded:
            return
        
        self.manual_editing = False

        if not self.data_viewed:
            self.enableEditor()
        
        if not self.deleted:
            self.saveActor(self.current_actor)
        else:
            self.deleted = False
        
        self.current_actor = self.ui.listWidget.currentRow() if self.room_data.actors else -1

        if self.current_actor != -1:
            try:
                act = self.room_data.actors[self.current_actor]
            except IndexError:
                return
            else:
                self.ui.ID_lineEdit.setText(str(act.key))
                self.ui.dataType.setCurrentIndex(
                    self.ui.dataType.findText(ACTOR_NAMES[ACTOR_IDS.index(hex(act.type))], QtCore.Qt.MatchExactly))
                # self.ui.dataRoomID.setText(str(act.roomID))
                self.ui.dataPos_X.setText(self.removeTrailingZeros(f'{act.posX:.8f}'))
                self.ui.dataPos_Y.setText(self.removeTrailingZeros(f'{act.posY:.8f}'))
                self.ui.dataPos_Z.setText(self.removeTrailingZeros(f'{act.posZ:.8f}'))
                self.ui.dataRot_X.setText(self.removeTrailingZeros(f'{act.rotX:.8f}'))
                self.ui.dataRot_Y.setText(self.removeTrailingZeros(f'{act.rotY:.8f}'))
                self.ui.dataRot_Z.setText(self.removeTrailingZeros(f'{act.rotZ:.8f}'))
                self.ui.dataScale_X.setText(self.removeTrailingZeros(f'{act.scaleX:.8f}'))
                self.ui.dataScale_Y.setText(self.removeTrailingZeros(f'{act.scaleY:.8f}'))
                self.ui.dataScale_Z.setText(self.removeTrailingZeros(f'{act.scaleZ:.8f}'))

                for i in range(8):
                    if isinstance(act.parameters[i], bytes):
                        param = str(act.parameters[i], 'utf-8')
                    elif isinstance(act.parameters[i], np.float32):
                        param = self.removeTrailingZeros(f'{act.parameters[i]:.8f}')
                    else:
                        param = act.parameters[i]
                    exec(f'self.ui.dataParameters_{i}.setText(str(param))')
                
                self.ui.dataSwitches_0.setText(str(act.switches[0][1]))
                self.ui.comboBox.setCurrentIndex(act.switches[0][0])
                self.ui.dataSwitches_1.setText(str(act.switches[1][1]))
                self.ui.comboBox_2.setCurrentIndex(act.switches[1][0])
                self.ui.dataSwitches_2.setText(str(act.switches[2][1]))
                self.ui.comboBox_3.setCurrentIndex(act.switches[2][0])
                self.ui.dataSwitches_3.setText(str(act.switches[3][1]))
                self.ui.comboBox_4.setCurrentIndex(act.switches[3][0])

                # relationships
                self.ui.comboBox_5.setCurrentIndex(act.relationships.is_enemy)
                self.ui.comboBox_6.setCurrentIndex(act.relationships.check_kills)
                self.ui.comboBox_7.setCurrentIndex(act.relationships.is_chamber_enemy)
                self.displayEntryInfo()
        
        for field in self.ui.groupBox.findChildren(QtWidgets.QLineEdit): # forces QLineEdit to display from leftmost character
            field.home(False)
        
        # let the GUI know that any further changes are from the user and now should update
        self.manual_editing = True
    


    def displayEntryInfo(self):
        act = self.room_data.actors[self.current_actor]
        sect = act.relationships.section_1
        # self.saveEntryData(section=1, entry=self.ui.dataCurrentEntry)
        if act.relationships.num_entries_1 > 0:
            self.ui.dataEntryParameter.setText(str(sect[self.ui.dataCurrentEntry.value()][0][0], 'utf-8'))
            self.ui.dataEntryParameter_2.setText(str(sect[self.ui.dataCurrentEntry.value()][0][1], 'utf-8'))
            self.ui.dataControlActorID.setText(self.room_data.actors[sect[self.ui.dataCurrentEntry.value()-1][1]].key)
        else:
            self.ui.dataEntryParameter.setText("")
            self.ui.dataEntryParameter.setEnabled(False)
            self.ui.dataEntryParameter_2.setText("")
            self.ui.dataEntryParameter_2.setEnabled(False)
            self.ui.dataControlActorID.setText("")
            self.ui.dataCurrentEntry.setMaximum(self.ui.dataCurrentEntry.value())
        
        act = self.room_data.actors[self.current_actor]
        sect = act.relationships.section_2
        if act.relationships.num_entries_2 > 0:
            self.ui.dataEntryParameter_3.setText(str(sect[self.ui.dataCurrentEntry_2.value()][0][0], 'utf-8'))
            self.ui.dataEntryParameter_4.setText(str(sect[self.ui.dataCurrentEntry_2.value()][0][1], 'utf-8'))
            self.ui.dataEntryRail.setValue(sect[self.ui.dataCurrentEntry_2.value()-1][1])
            self.ui.dataEntryPoint.setValue(sect[self.ui.dataCurrentEntry_2.value()-1][2])
        else:
            self.ui.dataEntryParameter_3.setText("")
            self.ui.dataEntryParameter_3.setEnabled(False)
            self.ui.dataEntryParameter_4.setText("")
            self.ui.dataEntryParameter_4.setEnabled(False)
            self.ui.dataEntryRail.setValue(-1)
            self.ui.dataEntryPoint.setValue(-1)
            self.ui.dataCurrentEntry_2.setMaximum(self.ui.dataCurrentEntry_2.value())
        
        act = self.room_data.actors[self.current_actor]
        sect = act.relationships.section_3
        if act.relationships.num_entries_3 > 0:
            self.ui.dataHostActorID.setText(self.room_data.actors[sect[self.ui.dataCurrentEntry_3.value()]].key)
        else:
            self.ui.dataHostActorID.setText("")
            self.ui.dataCurrentEntry_3.setMaximum(self.ui.dataCurrentEntry_3.value())
    


    def saveEntryData(self):
        pass



    def saveActor(self, previous=-1):
        if previous != -1:
            try:
                act = self.room_data.actors[previous]
                # act.key = int(self.ui.dataKey.text())
                # act.name = bytes(f'{self.ui.dataName.text()}-{self.ui.dataHex.text()}', 'utf-8')
                act.type = int(ACTORS[self.ui.dataType.currentText()], 16)
                # act.roomID = int(self.ui.dataRoomID.text())
                act.posX = float(self.ui.dataPos_X.text())
                act.posY = float(self.ui.dataPos_Y.text())
                act.posZ = float(self.ui.dataPos_Z.text())
                act.rotX = float(self.ui.dataRot_X.text())
                act.rotY = float(self.ui.dataRot_Y.text())
                act.rotZ = float(self.ui.dataRot_Z.text())
                act.scaleX = float(self.ui.dataScale_X.text())
                act.scaleY = float(self.ui.dataScale_Y.text())
                act.scaleZ = float(self.ui.dataScale_Z.text())

                for i in range(8):
                    try:
                        exec(f'act.parameters[i] = bytes(self.ui.dataParameters_{i}.text(), "utf-8")')
                    except TypeError:
                        exec(f'act.parameters[i] = int(self.ui.dataParameters_{i}.text())')
                
                act.switches[0] = (self.ui.comboBox.currentIndex(), int(self.ui.dataSwitches_0.text()))
                act.switches[1] = (self.ui.comboBox_2.currentIndex(), int(self.ui.dataSwitches_1.text()))
                act.switches[2] = (self.ui.comboBox_3.currentIndex(), int(self.ui.dataSwitches_2.text()))
                act.switches[3] = (self.ui.comboBox_4.currentIndex(), int(self.ui.dataSwitches_3.text()))
            
            except ValueError as e:
                self.showError(e.args[0])
                self.ui.listWidget.setCurrentRow(previous)
            
            except IndexError:
                pass
    


    def addActor(self):
        if self.file_loaded:
            try:
                act = copy.deepcopy(self.room_data.actors[self.current_actor])
                act.key = self.new_key
                self.new_key += 1
                name_str = str(act.name, 'utf-8').split('-')[0]
                name_hex = hex(act.key).split('0x')[1].upper()
                act.name = bytes(f'{name_str}-{name_hex}', 'utf-8')
                self.room_data.actors.append(act)
                # self.ui.dataEntryActor.setMaximum(len(self.room_data.actors))
                # self.ui.dataEntryActor_2.setMaximum(len(self.room_data.actors))
                self.ui.listWidget.addItem(f'{ACTOR_NAMES[ACTOR_IDS.index(hex(act.type))]} ({len(self.room_data.actors)})')
                self.ui.listWidget.setCurrentRow(self.ui.listWidget.count() - 1)
            except ValueError as e:
                self.showError(e.args[0])
            except IndexError:
                pass



    def deleteButton_Clicked(self):
        if self.file_loaded:
            if not self.room_data.actors[self.current_actor].type in REQUIRED_ACTORS:
                self.deleteActor()
            else:
                if len([act for act in self.room_data.actors if act.type == self.room_data.actors[self.current_actor].type]) > 1:
                    self.deleteActor()
                else:
                    self.showError('Levels require at least 1 actor of this type')
            self.displayActorInfo()
    


    def deleteActor(self):
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
        
        del self.room_data.actors[self.current_actor]
        # self.ui.dataEntryActor.setMaximum(len(self.room_data.actors))
        # self.ui.dataEntryActor_2.setMaximum(len(self.room_data.actors))
        self.deleted = True
        self.ui.listWidget.takeItem(self.current_actor)
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            act_name = item.text().split('(')
            item.setText(f'{act_name[0]}({i})')
    


    def updateActorType(self): # executed when the type field is edited and updates both the actor and the list
        
        if not self.manual_editing: # only change actor type when the user actually manually edits
            return
        
        act = self.room_data.actors[self.current_actor]
        new_type = ACTOR_NAMES.index(self.ui.dataType.currentText())

        if new_type == act.type: # do not do anything if the type is not being changed
            return
        
        if not self.room_data.actors[self.current_actor].type in REQUIRED_ACTORS:
            act.type = new_type
            self.ui.listWidget.currentItem().setText(self.ui.dataType.currentText())
        else:
            if len([act for act in self.room_data.actors if act.type == self.room_data.actors[self.current_actor].type]) > 1:
                act.type = new_type
                self.ui.listWidget.currentItem().setText(self.ui.dataType.currentText())
            else:
                self.showError('Levels require at least 1 actor of this type')
                self.ui.dataType.setCurrentIndex(
                    self.ui.dataType.findText(ACTOR_NAMES[ACTOR_IDS.index(hex(act.type))], QtCore.Qt.MatchExactly))



    def enableEditor(self):
        fields = [f for f in self.ui.tab.children()]
        fields += [f for f in self.ui.groupBox.children()]
        fields += [f for f in self.ui.tab_2.children()]
        fields += [f for f in self.ui.tab_3.children()]
        fields += [f for f in self.ui.groupBox_2.children()]
        fields += [f for f in self.ui.tab_4.children()]
        fields += [f for f in self.ui.groupBox_3.children()]
        fields += [f for f in self.ui.tab_5.children()]
        fields += [f for f in self.ui.groupBox_4.children()]
        for field in fields:
            field.setProperty('enabled', True)
        abc_actors = list(copy.deepcopy(ACTORS))
        abc_actors.sort()
        for actor in abc_actors:
            if not actor.startswith(('Player', 'null')):
                self.ui.dataType.addItem(actor)
        self.data_viewed = True
    


    def capCurrentEntries(self):
        return
        # self.room_data.actors[self.current_actor].relationships.num_entries_1 = self.ui.dataNumEntries.value()
        # self.ui.dataCurrentEntry.setMaximum(
        #     (self.ui.dataNumEntries.value() - 1) if (self.ui.dataNumEntries.value() - 1) > 0 else -1)
        if self.ui.dataNumEntries.value() > 0:
            self.ui.dataCurrentEntry.setMinimum(0)
            self.ui.dataEntryParameter.setEnabled(True)
            self.ui.dataEntryParameter_2.setEnabled(True)
            self.ui.dataEntryActor.setEnabled(True)
        else:
            self.ui.dataEntryParameter.setEnabled(False)
            self.ui.dataEntryParameter_2.setEnabled(False)
            self.ui.dataEntryActor.setEnabled(False)
        
        # self.room_data.actors[self.current_actor].relationships.num_entries_2 = self.ui.dataNumEntries_2.value()
        # self.ui.dataCurrentEntry_2.setMaximum(
        #     (self.ui.dataNumEntries_2.value() - 1) if (self.ui.dataNumEntries_2.value() - 1) > 0 else -1)
        if self.ui.dataNumEntries_2.value() > 0:
            self.ui.dataCurrentEntry_2.setMinimum(0)
            self.ui.dataEntryParameter_3.setEnabled(True)
            self.ui.dataEntryParameter_4.setEnabled(True)
            self.ui.dataEntryRail.setEnabled(True)
            self.ui.dataEntryPoint.setEnabled(True)
        else:
            self.ui.dataEntryParameter_3.setEnabled(False)
            self.ui.dataEntryParameter_4.setEnabled(False)
            self.ui.dataEntryRail.setEnabled(False)
            self.ui.dataEntryPoint.setEnabled(False)
        
        # self.room_data.actors[self.current_actor].relationships.num_entries_3 = self.ui.dataNumEntries_3.value()
        # self.ui.dataCurrentEntry_3.setMaximum(
        #     (self.ui.dataNumEntries_3.value() - 1) if (self.ui.dataNumEntries_3.value() - 1) > 0 else -1)
        if self.ui.dataNumEntries_3.value() > 0:
            self.ui.dataCurrentEntry_3.setMinimum(0)
            self.ui.dataEntryActor_2.setEnabled(True)
        else:
            self.ui.dataEntryActor_2.setEnabled(False)



    # def updateSect1CurrentEntry(self):
    #     if self.ui.dataEntryActor.value() < 0:
    #         self.ui.dataCurrentEntry.setMaximum(self.ui.dataCurrentEntry.value())
    #     else:
    #         self.ui.dataCurrentEntry.setMaximum(99)



    # def updateSect2CurrentEntry(self):
    #     if self.ui.dataEntryActor.value() < 0:
    #         self.ui.dataCurrentEntry.setMaximum(self.ui.dataCurrentEntry.value())
    #     else:
    #         self.ui.dataCurrentEntry.setMaximum(99)



    # def updateSect3CurrentEntry(self):
    #     if self.ui.dataEntryActor.value() < 0:
    #         self.ui.dataCurrentEntry.setMaximum(self.ui.dataCurrentEntry.value())
    #     else:
    #         self.ui.dataCurrentEntry.setMaximum(99)



    def removeTrailingZeros(self, dec: str):
        dec_list = [c for c in dec]
        dec_list.reverse()
        dec_list_2 = dec_list.copy()
        
        for d in dec_list_2:
            if d == '0':
                dec_list.remove(d)
            else:
                break
        
        dec_str = ''
        dec_list.reverse()
        for d in dec_list:
            dec_str += d
        
        if dec_str.endswith('.'):
            dec_str += '0'
        
        return dec_str



    def showError(self, error_message):
        message = QtWidgets.QMessageBox()
        message.setWindowTitle('LAS Level Editor')
        message.setText(error_message)
        message.exec()
