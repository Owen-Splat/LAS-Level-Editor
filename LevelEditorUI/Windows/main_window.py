from PySide6 import QtCore, QtWidgets, QtGui
from LevelEditorCore.Data.data import SIDEBAR_THEME, MAIN_THEME


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app_name) -> None:
        super (MainWindow, self).__init__()
        self.setupUi()
        self.setWindowTitle(app_name)
        self.show()


    def setupUi(self):
        self.setMinimumSize(640, 480)
        self.resize(self.minimumSize())
        self.setStyleSheet("background-color: #F5FAFE")

        self.sidebar = QtWidgets.QWidget(parent=self)
        self.sidebar.setGeometry(0, 0, 120, 480)
        self.sidebar.setStyleSheet(SIDEBAR_THEME)
        project_button = QtWidgets.QPushButton(text="Project Manager", parent=self.sidebar)
        project_button.setGeometry(5, 10, 130, 40)
        project_button.setCheckable(True)
        project_button.clicked.connect(lambda x: self.sidebarButtonClicked(project_button))
        level_button = QtWidgets.QPushButton(text="Level Properties", parent=self.sidebar)
        level_button.setGeometry(5, 60, 130, 40)
        level_button.setCheckable(True)
        level_button.clicked.connect(lambda x: self.sidebarButtonClicked(level_button))
        room_button = QtWidgets.QPushButton(text="Room Editor", parent=self.sidebar)
        room_button.setGeometry(5, 110, 130, 40)
        room_button.setCheckable(True)
        room_button.clicked.connect(lambda x: self.sidebarButtonClicked(room_button))
        datasheet_button = QtWidgets.QPushButton(text="Datasheets", parent=self.sidebar)
        datasheet_button.setGeometry(5, 160, 130, 40)
        datasheet_button.setCheckable(True)
        datasheet_button.clicked.connect(lambda x: self.sidebarButtonClicked(datasheet_button))
        event_button = QtWidgets.QPushButton(text="Event Editor", parent=self.sidebar)
        event_button.setGeometry(5, 210, 130, 40)
        event_button.setCheckable(True)
        event_button.clicked.connect(lambda x: self.sidebarButtonClicked(event_button))

        self.main_view = QtWidgets.QStackedWidget(parent=self)
        self.main_view.setGeometry(120, 0, 520, 480)
        self.main_view.setStyleSheet(MAIN_THEME)


    def sidebarButtonClicked(self, sender):
        for button in self.sidebar.findChildren(QtWidgets.QPushButton):
            check_state = False if button != sender else True
            button.setChecked(check_state)
