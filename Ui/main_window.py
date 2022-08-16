from PySide6 import QtWidgets
from Ui.ui_form import Ui_MainWindow
import leb

import copy
import os



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
        self.current_actor = -1
        self.deleted = -1

        self.ui.actionOpen.triggered.connect(self.fileOpen)
        self.ui.actionSave.triggered.connect(self.fileSave)
        self.ui.actionSaveAs.triggered.connect(self.fileSaveAs)
        self.ui.actionClose.triggered.connect(self.fileClose)
        self.ui.listWidget.currentItemChanged.connect(self.displayActorInfo)
        self.ui.dataHex.editingFinished.connect(self.updateActorKey)
        self.ui.addButton.clicked.connect(self.addActor)
        self.ui.delButton.clicked.connect(self.delActor)

        self.setFixedSize(800, 600)
        self.setWindowTitle('Level Editor')
        self.show()
    


    def fileOpen(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',
            os.path.dirname(self.file) if self.file_loaded else '', "Level files (*.leb)")[0]
        if not path:
            return
        
        self.fileClose()
        self.file = path

        try:
            with open(path, 'rb') as f:
                self.room_data = leb.Room(f.read())
        except (FileNotFoundError, ValueError) as e:
            message = QtWidgets.QMessageBox()
            message.setText(e.args[0])
            message.exec()
        else:
            self.file_loaded = True

            self.setWindowTitle(os.path.basename(path))

            self.ui.listWidget.setEnabled(True)
            self.ui.listWidget.clear()
            for act in self.room_data.actors:
                self.ui.listWidget.addItem(str(act.name, 'utf-8'))
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
                message = QtWidgets.QMessageBox()
                message.setText(e.args[0])
                message.exec()
            else:
                message = QtWidgets.QMessageBox()
                message.setText('File saved successfully')
                message.exec()



    def fileSaveAs(self):
        if self.file_loaded:
            path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File As',
                os.path.join(self.save_location, os.path.basename(self.file)), "Level files (*.leb)")[0]
            
            if path:
                self.save_location = os.path.dirname(path)
                self.saveActor(self.ui.listWidget.currentRow())
                try:
                    with open(path, 'wb') as f:
                        f.write(self.room_data.repack())
                except (ValueError, OverflowError) as e:
                    message = QtWidgets.QMessageBox()
                    message.setText(e.args[0])
                    message.exec()
                else:
                    message = QtWidgets.QMessageBox()
                    message.setText('File saved successfully')
                    message.exec()
    


    def fileClose(self):
        self.file = ''
        self.file_loaded = False
        self.save_location = ''
        self.current_actor = -1
        self.room_data = None
        self.ui.listWidget.clear()
        self.ui.listWidget.setEnabled(False)
        self.data_viewed = False
        for c in self.ui.groupBox.children():
            c.setEnabled(False)
        for field in self.ui.groupBox.findChildren(QtWidgets.QLineEdit):
            field.setText('')
        self.setWindowTitle('Level Editor')



    def displayActorInfo(self):
        if not self.file_loaded:
            return
        
        if not self.data_viewed:
            self.enableEditor()
        
        self.saveActor(self.current_actor)
        self.current_actor = self.ui.listWidget.currentRow() if self.deleted == -1 else self.current_actor

        if self.current_actor != -1:
            try:
                act = self.room_data.actors[self.current_actor]
            except IndexError:
                return
            else:
                self.ui.dataKey.setText(str(act.key))
                self.ui.dataName.setText(str(act.name, 'utf-8').split('-')[0])
                self.ui.dataHex.setText(str(act.name, 'utf-8').split('-')[1])
                self.ui.dataType.setText(str(hex(act.type)))
                self.ui.dataRoomID.setText(str(act.roomID))
                self.ui.dataPos_X.setText(str(act.posX))
                self.ui.dataPos_Y.setText(str(act.posY))
                self.ui.dataPos_Z.setText(str(act.posZ))
                self.ui.dataRot_X.setText(str(act.rotX))
                self.ui.dataRot_Y.setText(str(act.rotY))
                self.ui.dataRot_Z.setText(str(act.rotZ))
                self.ui.dataScale_X.setText(str(act.scaleX))
                self.ui.dataScale_Y.setText(str(act.scaleY))
                self.ui.dataScale_Z.setText(str(act.scaleZ))

                for i in range(8):
                    if type(act.parameters[i]) == bytes:
                        param = str(act.parameters[i], 'utf-8')
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
    


    def saveActor(self, previous=-1):
        if previous != -1:
            try:
                act = self.room_data.actors[previous]
                act.key = int(self.ui.dataKey.text())
                act.name = bytes(f'{self.ui.dataName.text()}-{self.ui.dataHex.text()}', 'utf-8')
                act.type = int(self.ui.dataType.text(), 16)
                act.roomID = int(self.ui.dataRoomID.text())
                act.posX = int(self.ui.dataPos_X.text())
                act.posY = int(self.ui.dataPos_Y.text())
                act.posZ = int(self.ui.dataPos_Z.text())
                act.rotX = int(self.ui.dataRot_X.text())
                act.rotY = int(self.ui.dataRot_Y.text())
                act.rotZ = int(self.ui.dataRot_Z.text())
                act.scaleX = int(self.ui.dataScale_X.text())
                act.scaleY = int(self.ui.dataScale_Y.text())
                act.scaleZ = int(self.ui.dataScale_Z.text())

                for i in range(8):
                    try:
                        exec(f'act.parameters[i] = int(self.ui.dataParameters_{i}.text())')
                    except ValueError:
                        exec(f'act.parameters[i] = bytes(self.ui.dataParameters_{i}.text(), "utf-8")')
                
                act.switches[0] = (self.ui.comboBox.currentIndex(), int(self.ui.dataSwitches_0.text()))
                act.switches[1] = (self.ui.comboBox_2.currentIndex(), int(self.ui.dataSwitches_1.text()))
                act.switches[2] = (self.ui.comboBox_3.currentIndex(), int(self.ui.dataSwitches_2.text()))
                act.switches[3] = (self.ui.comboBox_4.currentIndex(), int(self.ui.dataSwitches_3.text()))
            
            except ValueError as e:
                message = QtWidgets.QMessageBox()
                message.setText(e.args[0])
                message.exec()
                self.ui.listWidget.setCurrentRow(previous)
            
            except IndexError:
                pass
    


    def addActor(self):
        if self.file_loaded:
            try:
                act = copy.deepcopy(self.room_data.actors[self.current_actor])
                self.room_data.actors.append(act)
                self.ui.listWidget.addItem(str(act.name, 'utf-8'))
                self.ui.listWidget.setCurrentRow(self.ui.listWidget.count() - 1)
            except ValueError as e:
                message = QtWidgets.QMessageBox()
                message.setText(e.args[0])
                message.exec()
            except IndexError:
                pass



    def delActor(self):
        if self.file_loaded:
            try:
                self.deleted = self.current_actor
                if self.deleted > 0:
                    self.room_data.actors.pop(self.current_actor)
                    self.ui.listWidget.takeItem(self.current_actor)
                    self.ui.listWidget.setCurrentRow(self.deleted)
                    self.deleted = -1
                    if self.ui.listWidget.count() == 0:
                        self.fileClose()
                        return
            except IndexError:
                pass
    


    def updateActorKey(self):
        try:
            key = int(self.ui.dataHex.text(), 16)
        except ValueError as e:
            message = QtWidgets.QMessageBox()
            message.setText(e.args[0])
            message.exec()
        else:
            self.ui.dataKey.setText(str(key))
    


    def enableEditor(self):
        fields = [f for f in self.ui.groupBox.children() if f.objectName() not in ['label', 'dataKey']]
        for field in fields:
            field.setProperty('enabled', True)
        self.data_viewed = True
