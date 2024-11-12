from PySide6 import QtCore, QtWidgets, QtGui
import os


class PathsWindow(QtWidgets.QDialog):
    give_settings = QtCore.Signal(tuple)
    paths_valid = False

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 200)
        main_text = QtWidgets.QLabel('Please select your paths', parent=self)
        main_text.setGeometry(10, 0, self.width(), 30)
        main_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        rom_text = QtWidgets.QLabel('RomFS Path', parent=self)
        rom_text.setGeometry(10, 35, 100, 20)
        self.rom_line = QtWidgets.QLineEdit(parent=self)
        self.rom_line.setGeometry(10, 55, 300, 30)
        rom_button = QtWidgets.QPushButton(text='Browse', parent=self)
        rom_button.setGeometry(320, 55, 70, 30)
        rom_button.clicked.connect(self.romBrowse)
        out_text = QtWidgets.QLabel('Output Path', parent=self)
        out_text.setGeometry(10, 95, 100, 20)
        self.out_line = QtWidgets.QLineEdit(parent=self)
        self.out_line.setGeometry(10, 115, 300, 30)
        out_button = QtWidgets.QPushButton(text='Browse', parent=self)
        out_button.setGeometry(320, 115, 70, 30)
        out_button.clicked.connect(self.outBrowse)
        confirm_button = QtWidgets.QPushButton(text='Confirm', parent=self)
        confirm_button.setGeometry(165, 160, 70, 30)
        confirm_button.clicked.connect(self.confirmButtonPressed)


    def romBrowse(self) -> None:
        path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select RomFS Path')
        if path:
            self.rom_line.setText(path)
            self.validatePaths(rom=True, out=False)


    def outBrowse(self) -> None:
        path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Output Path')
        if path:
            self.out_line.setText(path)
            self.validatePaths(rom=False, out=True)


    def confirmButtonPressed(self) -> None:
        self.validatePaths(rom=True, out=True)
        if self.paths_valid:
            self.accept()


    def validatePaths(self, rom=True, out=True) -> None:
        if not rom and not out:
            return

        rom_valid = False
        if rom:
            rom_path = self.rom_line.text()
            if os.path.exists(os.path.join(rom_path, 'romfs')):
                rom_path = os.path.join(rom_path, 'romfs')
            self.rom_line.setText(rom_path)
            if os.path.isfile(os.path.join(rom_path, 'region_common/level/MarinTarinHouse/MarinTarinHouse_01A.leb')):
                self.rom_line.setStyleSheet('background-color: green')
                rom_valid = True
            else:
                self.rom_line.setStyleSheet('background-color: red')

        out_valid = False
        if out:
            out_path = self.out_line.text()
            color = 'green' if os.path.exists(out_path) else 'red'
            self.out_line.setStyleSheet(f'background-color: {color}')
            out_valid = True

        if rom_valid and out_valid:
            self.paths_valid = True


    # def closeEvent(self, event):
    #     event.accept()


    def done(self, result):
        print('done()')
        self.give_settings.emit((self.paths_valid, {
            'romfs_path': self.rom_line.text(),
            'output_path': self.out_line.text()}))
        super().done(result)
