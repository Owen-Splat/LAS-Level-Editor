from PySide6 import QtCore, QtWidgets
from LevelEditorUI.UI.ui_form import Ui_MainWindow
import LevelEditorCore.Tools.leb as leb
import copy, os, sys, yaml, random

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



class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super (MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)

        self.file = ''
        self.file_loaded = False
        self.save_location = ''

        self.data_viewed = False
        self.room_data = None
        self.current_actor = -1
        self.current_section = -1
        self.current_entry = -1
        self.deleted = False
        self.manual_editing = False
        self.keys = []

        self.ui.actionOpen.triggered.connect(self.fileOpen)
        self.ui.actionSave.triggered.connect(self.fileSave)
        self.ui.actionSaveAs.triggered.connect(self.fileSaveAs)
        self.ui.actionClose.triggered.connect(self.fileClose)
        self.ui.listWidget.currentItemChanged.connect(self.displayActorInfo)
        self.ui.dataType.currentIndexChanged.connect(self.updateActorType)
        self.ui.addButton.clicked.connect(self.addActor)
        self.ui.delButton.clicked.connect(self.deleteButton_Clicked)

        self.setFixedSize(800, 600)
        self.setWindowTitle('LAS Level Editor')
        self.show()


    def fileOpen(self, dragged_file=None):
        if dragged_file:
            path = dragged_file
        else:
            path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',
                os.path.dirname(self.file) if self.file_loaded else '', "Room files (*.leb)")[0]
            if not path.endswith(".leb"):
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
            self.ui.listWidget.setEnabled(True)
            self.ui.listWidget.clear()
            self.keys.clear()
            for act in self.room_data.actors:
                self.keys.append(act.key)
                self.ui.listWidget.addItem(f'{ACTOR_NAMES[ACTOR_IDS.index(hex(act.type))]}')
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
                    elif isinstance(act.parameters[i], float):
                        param = self.removeTrailingZeros(f'{act.parameters[i]:.8f}')
                    else:
                        param = str(act.parameters[i])
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
        relationship_info = {}

        relationship_info['Controlled_Actors'] = []
        for entry in act.relationships.section_1:
            params = []
            for param in entry[0]:
                params.append(str(param))
            relationship_info['Controlled_Actors'].append({
                self.room_data.actors[entry[1]].key: {
                    'Parameters': params
                }
            })
        
        relationship_info['Needed_Positions'] = []
        for entry in act.relationships.section_2:
            params = []
            for param in entry[0]:
                params.append(str(param))
            relationship_info['Needed_Positions'].append({
                'Rail_Index': entry[1],
                'Point_Index': entry[2],
                'Parameters': params
            })
        
        relationship_info['Actors_That_Use_Me'] = []
        for entry in act.relationships.section_3:
            relationship_info['Actors_That_Use_Me'].append(self.room_data.actors[entry].key)
        
        self.ui.textEdit.setText(yaml.dump(relationship_info, Dumper=MyDumper, sort_keys=False, default_flow_style=False, indent=4))
    

    def saveEntryData(self):
        pass


    def saveActor(self, previous=-1):
        if previous != -1:
            try:
                act = self.room_data.actors[previous]
                act.type = int(ACTORS[self.ui.dataType.currentText()], 16)
                act.posX = float(self.ui.dataPos_X.text())
                act.posY = float(self.ui.dataPos_Y.text())
                act.posZ = float(self.ui.dataPos_Z.text())
                act.rotX = float(self.ui.dataRot_X.text())
                act.rotY = float(self.ui.dataRot_Y.text())
                act.rotZ = float(self.ui.dataRot_Z.text())
                act.scaleX = float(self.ui.dataScale_X.text())
                act.scaleY = float(self.ui.dataScale_Y.text())
                act.scaleZ = float(self.ui.dataScale_Z.text())

                ldict = locals()
                for i in range(8):
                    exec(f"v = self.ui.dataParameters_{i}.text()")
                    if str(ldict['v']).isdigit():
                        act.parameters[i] = int(ldict['v'])
                    else:
                        try:
                            exec(f"act.parameters[i] = float(ldict['v'])")
                        except ValueError:
                            exec(f"act.parameters[i] = bytes(ldict['v'], 'utf-8')")
                
                act.switches[0] = (self.ui.comboBox.currentIndex(), int(self.ui.dataSwitches_0.text()))
                act.switches[1] = (self.ui.comboBox_2.currentIndex(), int(self.ui.dataSwitches_1.text()))
                act.switches[2] = (self.ui.comboBox_3.currentIndex(), int(self.ui.dataSwitches_2.text()))
                act.switches[3] = (self.ui.comboBox_4.currentIndex(), int(self.ui.dataSwitches_3.text()))

                self.saveEntryData()
            
            except ValueError as e:
                self.showError(e.args[0])
                self.ui.listWidget.setCurrentRow(previous)
            
            except IndexError:
                pass


    def addActor(self):
        if self.file_loaded:
            try:
                act = copy.deepcopy(self.room_data.actors[self.current_actor])
                while act.key in self.keys:
                    act.key = random.getrandbits(64)
                name_str = str(act.name, 'utf-8').split('-')[0]
                name_hex = hex(act.key).split('0x')[1].upper()
                act.name = bytes(f'{name_str}-{name_hex}', 'utf-8')
                self.room_data.actors.append(act)
                self.ui.listWidget.addItem(f'{ACTOR_NAMES[ACTOR_IDS.index(hex(act.type))]}')
                self.ui.listWidget.setCurrentRow(self.ui.listWidget.count() - 1)
            except ValueError as e:
                self.showError(e.args[0])
            except IndexError:
                pass


    def deleteButton_Clicked(self):
        if self.file_loaded:
            if self.room_data.actors[self.current_actor].type not in REQUIRED_ACTORS:
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
        
        self.keys.remove(self.room_data.actors[self.current_actor].key)
        del self.room_data.actors[self.current_actor]
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


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            links = [str(l.toLocalFile()) for l in event.mimeData().urls() if l.toLocalFile().endswith(".leb")]
            if links:
                event.accept()
                return
        event.ignore()


    def dropEvent(self, event):
        event.accept()
        link = [str(l.toLocalFile()) for l in event.mimeData().urls() if l.toLocalFile().endswith(".leb")][0]
        self.fileOpen(link)
