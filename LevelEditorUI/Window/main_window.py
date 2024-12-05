################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
## This project can be used freely for all uses, as long as they maintain the
## respective credits only in the Python scripts, any information in the visual
## interface (GUI) can be modified without any implication.
##
## There are limitations on Qt licenses if you want to use your products
## commercially, I recommend reading them on the official website:
## https://doc.qt.io/qtforpython/licenses.html
##
################################################################################

# REGULAR IMPORTS
from PySide6 import QtCore, QtGui, QtWidgets
import os, string

# GUI FILE
from LevelEditorUI.Window.GUI_BASE import Ui_MainWindow

# IMPORT FUNCTIONS
from LevelEditorUI.Window.ui_functions import *

# IMPORT EXTRA DATA
from LevelEditorCore.Data.data import *

# IMPORT FILE PARSERS
import LevelEditorCore.Tools.FixedHash.leb as leb


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app_name):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## PRINT ==> SYSTEM
        # print('System: ' + platform.system())
        # print('Version: ' +platform.release())

        ########################################################################
        ## START - WINDOW VARIABLES
        ########################################################################
        self.app_name = app_name
        self.rom_path = ''
        self.out_path = ''
        self.manual_editing = True
        ## ==> END ##

        ########################################################################
        ## START - WINDOW ATTRIBUTES
        ########################################################################

        ## REMOVE ==> STANDARD TITLE BAR
        UIFunctions.removeTitleBar(True)
        ## ==> END ##

        ## SET ==> WINDOW TITLE
        self.setWindowTitle(app_name)
        UIFunctions.labelTitle(self, self.windowTitle())
        UIFunctions.labelDescription(self, '')
        ## ==> END ##

        ## WINDOW SIZE ==> DEFAULT SIZE
        startSize = QtCore.QSize(1000, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)
        # UIFunctions.enableMaximumSize(self, 500, 720)
        ## ==> END ##

        ## ==> SET DEFAULT ICONS
        self.ui.btn_toggle_menu.setIcon(QtGui.QIcon(MENU_ICON))
        self.ui.btn_toggle_menu.setIconSize(QtCore.QSize(24, 24))
        self.ui.btn_minimize.setIcon(QtGui.QIcon(MINIMIZE_ICON))
        self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(MAXIMIZE_ICON))
        self.ui.btn_close.setIcon(QtGui.QIcon(CLOSE_ICON))
        f_stylesheet = self.ui.frame_size_grip.styleSheet().replace('ICON_REPLACE', f'url({SIZE_ICON})')
        self.ui.frame_size_grip.setStyleSheet(f_stylesheet)
        f_stylesheet = self.ui.frame_icon_top_bar.styleSheet().replace('ICON_REPLACE', f'url({MAIN_ICON})')
        self.ui.frame_icon_top_bar.setStyleSheet(f_stylesheet)
        ## ==> END ##

        ## ==> CREATE MENUS
        ########################################################################

        ## ==> TOGGLE MENU SIZE
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))
        ## ==> END ##

        ## ==> ADD CUSTOM MENUS
        self.ui.stackedWidget.setMinimumWidth(20)
        UIFunctions.addNewMenu(self, "Project Manager", "btn_home", HOME_ICON, True)
        UIFunctions.addNewMenu(self, "Level Select", "btn_location", LOCATION_ICON, True)
        UIFunctions.addNewMenu(self, "Level Properties", "btn_properties", PROPERTIES_ICON, True)
        UIFunctions.addNewMenu(self, "Room Editor", "btn_room", ROOM_ICON, True)
        UIFunctions.addNewMenu(self, "Datasheets", "btn_sheets", DATASHEET_ICON, True)
        UIFunctions.addNewMenu(self, "Event Editor", "btn_events", EVENTS_ICON, True)
        UIFunctions.addNewMenu(self, "Assembly", "btn_code", CODE_ICON, True)
        # UIFunctions.addNewMenu(self, "Custom Widgets", "btn_widgets", "url(:/16x16/icons/16x16/cil-equalizer.png)", False)
        ## ==> END ##

        # START MENU => SELECTION
        UIFunctions.selectStandardMenu(self, "btn_home")
        UIFunctions.labelPage(self, "Project Manager")
        ## ==> END ##

        ## ==> START PAGE
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        ## ==> END ##

        ## USER ICON ==> SHOW HIDE
        # UIFunctions.userIcon(self, "WM", "", False)
        ## ==> END ##

        ## ==> SIGNALS
        self.ui.projectNameEdit.textEdited.connect(lambda x: \
            self.ui.projectNameLabel.setText(self.ui.projectNameEdit.text()))
        self.ui.romBrowseButton.clicked.connect(lambda x: self.selectFolder(self.ui.romEdit))
        self.ui.outBrowseButton.clicked.connect(lambda x: self.selectFolder(self.ui.outEdit))
        self.ui.levelList.currentRowChanged.connect(self.showLevelLayout)
        ## ==> END ##


        ## ==> MOVE WINDOW / MAXIMIZE / RESTORE
        ########################################################################
        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunctions.returnStatus() == 1:
                UIFunctions.maximize_restore(self)

            # MOVE WINDOW
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # WIDGET TO MOVE
        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow
        ## ==> END ##

        ## ==> LOAD DEFINITIONS
        ########################################################################
        UIFunctions.uiDefinitions(self)
        ## ==> END ##

        ########################################################################
        ## END - WINDOW ATTRIBUTES
        ############################## ---/--/--- ##############################

        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    ########################################################################
    ## MENUS ==> DYNAMIC MENUS FUNCTIONS
    ########################################################################
    def Button(self):
        # GET BT CLICKED
        btnWidget = self.sender()
        btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE HOME
        if btnWidget.objectName() == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, "btn_home")
            UIFunctions.labelPage(self, "Project Manager")

        # PAGE LOCATION
        if btnWidget.objectName() == "btn_location":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_location)
            UIFunctions.resetStyle(self, "btn_location")
            UIFunctions.labelPage(self, "Level Select")
            self.showLevelList()

        # PAGE PROPERTIES
        if btnWidget.objectName() == "btn_properties":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_properties)
            UIFunctions.resetStyle(self, "btn_properties")
            UIFunctions.labelPage(self, "Level Properties")

        # PAGE ROOM
        if btnWidget.objectName() == "btn_room":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_room)
            UIFunctions.resetStyle(self, "btn_room")
            UIFunctions.labelPage(self, "Room Editor")

        # PAGE DATASHEETS
        if btnWidget.objectName() == "btn_sheets":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_room)
            UIFunctions.resetStyle(self, "btn_room")
            UIFunctions.labelPage(self, "Datasheets")

        # PAGE EVENTS
        if btnWidget.objectName() == "btn_events":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_room)
            UIFunctions.resetStyle(self, "btn_room")
            UIFunctions.labelPage(self, "Event Editor")

        # PAGE ASSEMBLY
        if btnWidget.objectName() == "btn_code":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_room)
            UIFunctions.resetStyle(self, "btn_room")
            UIFunctions.labelPage(self, "Assembly")


    ## ==> END ##

    ########################################################################
    ## START ==> APP EVENTS
    ########################################################################

    ## EVENT ==> MOUSE DOUBLE CLICK
    ########################################################################
    def eventFilter(self, watched, event):
        pass
        # if watched == self.le and event.type() == QtCore.QEvent.Type.MouseButtonDblClick:
        #     print("pos: ", event.pos())
    ## ==> END ##

    ## EVENT ==> MOUSE CLICK
    ########################################################################
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        # if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
        #     print('Mouse click: LEFT CLICK')
        # if event.buttons() == QtCore.Qt.MouseButton.RightButton:
        #     print('Mouse click: RIGHT CLICK')
        # if event.buttons() == QtCore.Qt.MouseButton.MiddleButton:
        #     print('Mouse click: MIDDLE BUTTON')
    ## ==> END ##

    ## EVENT ==> RESIZE EVENT
    ########################################################################
    # def resizeEvent(self, event):
    #     self.resizeFunction()
    #     return super(MainWindow, self).resizeEvent(event)

    ## ==> END ##

    ## START ==> ERROR WINDOW

    def showError(self, error_message) -> None:
        """Opens a new QMessageBox with error_message as the text"""

        message = QtWidgets.QMessageBox()
        message.setWindowTitle(self.app_name)
        message.setText(error_message)
        message.exec()

    ## ==> END ##

    ########################################################################
    ## START ==> PROJECT TAB
    ########################################################################

    def selectFolder(self, line_edit):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open Level',
            self.rom_path if self.rom_path else '')
        if not path:
            return
        else:
            if line_edit == self.ui.romEdit:
                if os.path.exists(os.path.join(path, 'romfs')):
                    path = os.path.join(path, 'romfs')
                if not os.path.isfile(f'{path}/region_common/event/PlayerStart.bfevfl'):
                    self.showError('RomFS path is not valid!')
                    return
                self.rom_path = path
            if line_edit == self.ui.outEdit:
                self.out_path = path
            line_edit.setText(path)

    ## ==> END ##

    ########################################################################
    ## START ==> LOCATION TAB
    ########################################################################

    def showLevelList(self):
        """Puts all levels into a QListWidget for the user to choose from"""

        self.manual_editing = False

        if not self.rom_path or not self.out_path:
            return # return if paths are not set
        self.level_list = set([f for f in os.listdir(os.path.join(self.rom_path, 'region_common/level')) \
                if os.path.isdir(os.path.join(self.rom_path, 'region_common/level', f))])
        self.modded_level_list = set()
        try:
            self.modded_level_list.update([f for f in os.listdir(os.path.join(self.out_path, 'region_common/level')) \
                        if os.path.isdir(os.path.join(self.out_path, 'region_common/level', f))])
        except FileNotFoundError:
            pass # the user might not have saved anything yet, so ignore in such case
        total_levels = set(self.level_list)
        total_levels.update(self.modded_level_list)
        self.ui.levelList.clear()
        for lv in total_levels:
            self.ui.levelList.addItem(lv)
        self.ui.levelList.sortItems()

        self.manual_editing = True


    def showLevelLayout(self, current_row):
        """Displays the layout of all the rooms in the currently selected level"""

        if not self.manual_editing:
            return

        # clear the room grid
        while self.ui.levelGridLayout.count():
            room = self.ui.levelGridLayout.takeAt(0).widget()
            if room is not None:
                room.deleteLater()

        # get room list
        level_name = self.ui.levelList.item(current_row).text()
        room_files = [f for f in os.listdir(os.path.join(self.rom_path, f'region_common/level/{level_name}')) \
                      if f.endswith('.leb')]

        # put rooms on the grid
        for room in room_files:
            with open(os.path.join(self.rom_path, f'region_common/level/{level_name}', room), 'rb') as f:
                room_data = leb.Room(f.read())
            if room_data.grid.info.room_type == '2D':
                continue
            room_location = room.split("_")[1] # 1A, 3C, 7F, etc
            row = int(room_location[0] + room_location[1]) - 1
            column = string.ascii_uppercase.index(room_location[2])
            test_room_icon = QtWidgets.QFrame()
            test_room_icon.setStyleSheet("background-color: brown;")
            self.ui.levelGridLayout.addWidget(test_room_icon, row, column)
            # test_room_icon.setFixedWidth(int(round(test_room_icon.width() * 64) / 64))
            # test_room_icon.setFixedHeight(int(round(test_room_icon.height() * 64) / 64))
            # print(test_room_icon.width(), test_room_icon.height())

        # # add an empty space to the grid to make sure all rooms are the same size
        # blank = QtWidgets.QFrame()
        # blank.setStyleSheet("background-color: green")
        # self.ui.levelGrid.addWidget(blank, 16, 16)

    ## ==> END ##
