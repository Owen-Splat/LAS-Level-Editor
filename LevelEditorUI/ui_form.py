# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_form.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpinBox, QTabWidget, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QSize(800, 600))
        MainWindow.setBaseSize(QSize(800, 600))
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSaveAs = QAction(MainWindow)
        self.actionSaveAs.setObjectName(u"actionSaveAs")
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.actionActors = QAction(MainWindow)
        self.actionActors.setObjectName(u"actionActors")
        self.actionPoints = QAction(MainWindow)
        self.actionPoints.setObjectName(u"actionPoints")
        self.actionRails = QAction(MainWindow)
        self.actionRails.setObjectName(u"actionRails")
        self.actionGrid = QAction(MainWindow)
        self.actionGrid.setObjectName(u"actionGrid")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 6, 251, 31))
        font = QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignBottom|Qt.AlignHCenter)
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setEnabled(False)
        self.listWidget.setGeometry(QRect(15, 41, 261, 491))
        self.addButton = QPushButton(self.centralwidget)
        self.addButton.setObjectName(u"addButton")
        self.addButton.setGeometry(QRect(14, 540, 121, 24))
        self.delButton = QPushButton(self.centralwidget)
        self.delButton.setObjectName(u"delButton")
        self.delButton.setGeometry(QRect(150, 540, 121, 24))
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QRect(286, 9, 511, 561))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(0, 0, 511, 541))
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet(u"QGroupBox#groupBox {border:0;}")
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.groupBox.setFlat(True)
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setEnabled(False)
        self.label_4.setGeometry(QRect(10, 50, 51, 22))
        font1 = QFont()
        font1.setPointSize(9)
        self.label_4.setFont(font1)
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.dataPos_X = QLineEdit(self.groupBox)
        self.dataPos_X.setObjectName(u"dataPos_X")
        self.dataPos_X.setEnabled(False)
        self.dataPos_X.setGeometry(QRect(70, 110, 131, 22))
        font2 = QFont()
        font2.setPointSize(10)
        self.dataPos_X.setFont(font2)
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setEnabled(False)
        self.label_6.setGeometry(QRect(10, 110, 51, 22))
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.dataPos_Y = QLineEdit(self.groupBox)
        self.dataPos_Y.setObjectName(u"dataPos_Y")
        self.dataPos_Y.setEnabled(False)
        self.dataPos_Y.setGeometry(QRect(210, 110, 131, 22))
        self.dataPos_Y.setFont(font2)
        self.dataPos_Z = QLineEdit(self.groupBox)
        self.dataPos_Z.setObjectName(u"dataPos_Z")
        self.dataPos_Z.setEnabled(False)
        self.dataPos_Z.setGeometry(QRect(350, 110, 131, 22))
        self.dataPos_Z.setFont(font2)
        self.dataRot_Y = QLineEdit(self.groupBox)
        self.dataRot_Y.setObjectName(u"dataRot_Y")
        self.dataRot_Y.setEnabled(False)
        self.dataRot_Y.setGeometry(QRect(210, 140, 131, 22))
        self.dataRot_Y.setFont(font2)
        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setEnabled(False)
        self.label_7.setGeometry(QRect(10, 140, 51, 22))
        self.label_7.setFont(font1)
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.dataRot_X = QLineEdit(self.groupBox)
        self.dataRot_X.setObjectName(u"dataRot_X")
        self.dataRot_X.setEnabled(False)
        self.dataRot_X.setGeometry(QRect(70, 140, 131, 22))
        self.dataRot_X.setFont(font2)
        self.dataRot_Z = QLineEdit(self.groupBox)
        self.dataRot_Z.setObjectName(u"dataRot_Z")
        self.dataRot_Z.setEnabled(False)
        self.dataRot_Z.setGeometry(QRect(350, 140, 131, 22))
        self.dataRot_Z.setFont(font2)
        self.dataScale_Y = QLineEdit(self.groupBox)
        self.dataScale_Y.setObjectName(u"dataScale_Y")
        self.dataScale_Y.setEnabled(False)
        self.dataScale_Y.setGeometry(QRect(210, 170, 131, 22))
        self.dataScale_Y.setFont(font2)
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setEnabled(False)
        self.label_8.setGeometry(QRect(10, 170, 51, 22))
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.dataScale_X = QLineEdit(self.groupBox)
        self.dataScale_X.setObjectName(u"dataScale_X")
        self.dataScale_X.setEnabled(False)
        self.dataScale_X.setGeometry(QRect(70, 170, 131, 22))
        self.dataScale_X.setFont(font2)
        self.dataScale_Z = QLineEdit(self.groupBox)
        self.dataScale_Z.setObjectName(u"dataScale_Z")
        self.dataScale_Z.setEnabled(False)
        self.dataScale_Z.setGeometry(QRect(350, 170, 131, 22))
        self.dataScale_Z.setFont(font2)
        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setEnabled(False)
        self.label_10.setGeometry(QRect(70, 90, 131, 20))
        self.label_10.setFont(font1)
        self.label_10.setAlignment(Qt.AlignCenter)
        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setEnabled(False)
        self.label_11.setGeometry(QRect(210, 90, 131, 20))
        self.label_11.setFont(font1)
        self.label_11.setAlignment(Qt.AlignCenter)
        self.label_12 = QLabel(self.groupBox)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setEnabled(False)
        self.label_12.setGeometry(QRect(350, 90, 131, 20))
        self.label_12.setFont(font1)
        self.label_12.setAlignment(Qt.AlignCenter)
        self.dataParameters_0 = QLineEdit(self.groupBox)
        self.dataParameters_0.setObjectName(u"dataParameters_0")
        self.dataParameters_0.setEnabled(False)
        self.dataParameters_0.setGeometry(QRect(40, 235, 201, 22))
        self.dataParameters_0.setFont(font1)
        self.dataParameters_1 = QLineEdit(self.groupBox)
        self.dataParameters_1.setObjectName(u"dataParameters_1")
        self.dataParameters_1.setEnabled(False)
        self.dataParameters_1.setGeometry(QRect(280, 235, 201, 22))
        self.dataParameters_1.setFont(font1)
        self.label_15 = QLabel(self.groupBox)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setEnabled(False)
        self.label_15.setGeometry(QRect(40, 210, 441, 21))
        self.label_15.setFont(font1)
        self.label_15.setAlignment(Qt.AlignCenter)
        self.dataParameters_2 = QLineEdit(self.groupBox)
        self.dataParameters_2.setObjectName(u"dataParameters_2")
        self.dataParameters_2.setEnabled(False)
        self.dataParameters_2.setGeometry(QRect(40, 265, 201, 22))
        self.dataParameters_2.setFont(font1)
        self.dataParameters_3 = QLineEdit(self.groupBox)
        self.dataParameters_3.setObjectName(u"dataParameters_3")
        self.dataParameters_3.setEnabled(False)
        self.dataParameters_3.setGeometry(QRect(280, 265, 201, 22))
        self.dataParameters_3.setFont(font1)
        self.dataParameters_6 = QLineEdit(self.groupBox)
        self.dataParameters_6.setObjectName(u"dataParameters_6")
        self.dataParameters_6.setEnabled(False)
        self.dataParameters_6.setGeometry(QRect(40, 325, 201, 22))
        self.dataParameters_6.setFont(font1)
        self.dataParameters_4 = QLineEdit(self.groupBox)
        self.dataParameters_4.setObjectName(u"dataParameters_4")
        self.dataParameters_4.setEnabled(False)
        self.dataParameters_4.setGeometry(QRect(40, 295, 201, 22))
        self.dataParameters_4.setFont(font1)
        self.dataParameters_7 = QLineEdit(self.groupBox)
        self.dataParameters_7.setObjectName(u"dataParameters_7")
        self.dataParameters_7.setEnabled(False)
        self.dataParameters_7.setGeometry(QRect(280, 325, 201, 22))
        self.dataParameters_7.setFont(font1)
        self.dataParameters_5 = QLineEdit(self.groupBox)
        self.dataParameters_5.setObjectName(u"dataParameters_5")
        self.dataParameters_5.setEnabled(False)
        self.dataParameters_5.setGeometry(QRect(280, 295, 201, 22))
        self.dataParameters_5.setFont(font1)
        self.label_16 = QLabel(self.groupBox)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setEnabled(False)
        self.label_16.setGeometry(QRect(40, 370, 441, 21))
        self.label_16.setFont(font1)
        self.label_16.setAlignment(Qt.AlignCenter)
        self.dataSwitches_0 = QLineEdit(self.groupBox)
        self.dataSwitches_0.setObjectName(u"dataSwitches_0")
        self.dataSwitches_0.setEnabled(False)
        self.dataSwitches_0.setGeometry(QRect(40, 395, 201, 22))
        self.dataSwitches_0.setFont(font2)
        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setEnabled(False)
        self.comboBox.setGeometry(QRect(280, 395, 201, 22))
        self.comboBox.setFont(font2)
        self.label_17 = QLabel(self.groupBox)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setEnabled(False)
        self.label_17.setGeometry(QRect(10, 265, 21, 22))
        self.label_17.setFont(font1)
        self.label_17.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_18 = QLabel(self.groupBox)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setEnabled(False)
        self.label_18.setGeometry(QRect(10, 295, 21, 22))
        self.label_18.setFont(font1)
        self.label_18.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_19 = QLabel(self.groupBox)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setEnabled(False)
        self.label_19.setGeometry(QRect(10, 325, 21, 22))
        self.label_19.setFont(font1)
        self.label_19.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_20 = QLabel(self.groupBox)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setEnabled(False)
        self.label_20.setGeometry(QRect(250, 265, 21, 22))
        self.label_20.setFont(font1)
        self.label_20.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_21 = QLabel(self.groupBox)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setEnabled(False)
        self.label_21.setGeometry(QRect(250, 295, 21, 22))
        self.label_21.setFont(font1)
        self.label_21.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_22 = QLabel(self.groupBox)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setEnabled(False)
        self.label_22.setGeometry(QRect(250, 325, 21, 22))
        self.label_22.setFont(font1)
        self.label_22.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_23 = QLabel(self.groupBox)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setEnabled(False)
        self.label_23.setGeometry(QRect(10, 235, 21, 22))
        self.label_23.setFont(font1)
        self.label_23.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_24 = QLabel(self.groupBox)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setEnabled(False)
        self.label_24.setGeometry(QRect(250, 235, 21, 22))
        self.label_24.setFont(font1)
        self.label_24.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_25 = QLabel(self.groupBox)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setEnabled(False)
        self.label_25.setGeometry(QRect(10, 395, 21, 22))
        self.label_25.setFont(font1)
        self.label_25.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_26 = QLabel(self.groupBox)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setEnabled(False)
        self.label_26.setGeometry(QRect(10, 425, 21, 22))
        self.label_26.setFont(font1)
        self.label_26.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.dataSwitches_1 = QLineEdit(self.groupBox)
        self.dataSwitches_1.setObjectName(u"dataSwitches_1")
        self.dataSwitches_1.setEnabled(False)
        self.dataSwitches_1.setGeometry(QRect(40, 425, 201, 22))
        self.dataSwitches_1.setFont(font2)
        self.comboBox_2 = QComboBox(self.groupBox)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setEnabled(False)
        self.comboBox_2.setGeometry(QRect(280, 425, 201, 22))
        self.comboBox_2.setFont(font2)
        self.dataSwitches_3 = QLineEdit(self.groupBox)
        self.dataSwitches_3.setObjectName(u"dataSwitches_3")
        self.dataSwitches_3.setEnabled(False)
        self.dataSwitches_3.setGeometry(QRect(40, 485, 201, 22))
        self.dataSwitches_3.setFont(font2)
        self.label_27 = QLabel(self.groupBox)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setEnabled(False)
        self.label_27.setGeometry(QRect(10, 455, 21, 22))
        self.label_27.setFont(font1)
        self.label_27.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_28 = QLabel(self.groupBox)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setEnabled(False)
        self.label_28.setGeometry(QRect(10, 485, 21, 22))
        self.label_28.setFont(font1)
        self.label_28.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.comboBox_4 = QComboBox(self.groupBox)
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.setObjectName(u"comboBox_4")
        self.comboBox_4.setEnabled(False)
        self.comboBox_4.setGeometry(QRect(280, 485, 201, 22))
        self.comboBox_4.setFont(font2)
        self.dataSwitches_2 = QLineEdit(self.groupBox)
        self.dataSwitches_2.setObjectName(u"dataSwitches_2")
        self.dataSwitches_2.setEnabled(False)
        self.dataSwitches_2.setGeometry(QRect(40, 455, 201, 22))
        self.dataSwitches_2.setFont(font2)
        self.comboBox_3 = QComboBox(self.groupBox)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setEnabled(False)
        self.comboBox_3.setGeometry(QRect(280, 455, 201, 22))
        self.comboBox_3.setFont(font2)
        self.dataType = QComboBox(self.groupBox)
        self.dataType.setObjectName(u"dataType")
        self.dataType.setEnabled(False)
        self.dataType.setGeometry(QRect(70, 50, 411, 22))
        self.dataType.setFont(font2)
        self.ID_lineEdit = QLineEdit(self.groupBox)
        self.ID_lineEdit.setObjectName(u"ID_lineEdit")
        self.ID_lineEdit.setEnabled(False)
        self.ID_lineEdit.setGeometry(QRect(70, 20, 411, 22))
        self.ID_lineEdit.setReadOnly(True)
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setEnabled(False)
        self.label_5.setGeometry(QRect(10, 20, 51, 22))
        self.label_5.setFont(font1)
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.comboBox_5 = QComboBox(self.tab_2)
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.setObjectName(u"comboBox_5")
        self.comboBox_5.setEnabled(False)
        self.comboBox_5.setGeometry(QRect(10, 20, 151, 22))
        self.comboBox_6 = QComboBox(self.tab_2)
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.setObjectName(u"comboBox_6")
        self.comboBox_6.setEnabled(False)
        self.comboBox_6.setGeometry(QRect(175, 20, 151, 22))
        self.comboBox_7 = QComboBox(self.tab_2)
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.setObjectName(u"comboBox_7")
        self.comboBox_7.setEnabled(False)
        self.comboBox_7.setGeometry(QRect(340, 20, 151, 22))
        self.tabWidget_2 = QTabWidget(self.tab_2)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setGeometry(QRect(10, 60, 481, 461))
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.label_14 = QLabel(self.tab_3)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setEnabled(False)
        self.label_14.setGeometry(QRect(10, 20, 81, 41))
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.groupBox_2 = QGroupBox(self.tab_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setEnabled(False)
        self.groupBox_2.setGeometry(QRect(10, 90, 451, 161))
        font3 = QFont()
        font3.setPointSize(12)
        self.groupBox_2.setFont(font3)
        self.groupBox_2.setAlignment(Qt.AlignCenter)
        self.groupBox_2.setFlat(False)
        self.dataEntryParameter = QLineEdit(self.groupBox_2)
        self.dataEntryParameter.setObjectName(u"dataEntryParameter")
        self.dataEntryParameter.setEnabled(False)
        self.dataEntryParameter.setGeometry(QRect(110, 80, 331, 22))
        self.dataEntryParameter.setFont(font2)
        self.label_30 = QLabel(self.groupBox_2)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setEnabled(False)
        self.label_30.setGeometry(QRect(10, 120, 71, 21))
        self.label_30.setFont(font1)
        self.label_30.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.dataEntryParameter_2 = QLineEdit(self.groupBox_2)
        self.dataEntryParameter_2.setObjectName(u"dataEntryParameter_2")
        self.dataEntryParameter_2.setEnabled(False)
        self.dataEntryParameter_2.setGeometry(QRect(110, 120, 331, 22))
        self.dataEntryParameter_2.setFont(font2)
        self.label_29 = QLabel(self.groupBox_2)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setEnabled(False)
        self.label_29.setGeometry(QRect(10, 80, 71, 21))
        self.label_29.setFont(font1)
        self.label_29.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_31 = QLabel(self.groupBox_2)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setEnabled(False)
        self.label_31.setGeometry(QRect(10, 40, 71, 21))
        self.label_31.setFont(font1)
        self.label_31.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.dataControlActorID = QLineEdit(self.groupBox_2)
        self.dataControlActorID.setObjectName(u"dataControlActorID")
        self.dataControlActorID.setEnabled(False)
        self.dataControlActorID.setGeometry(QRect(110, 40, 331, 22))
        self.dataControlActorID.setFont(font2)
        self.dataCurrentEntry = QSpinBox(self.tab_3)
        self.dataCurrentEntry.setObjectName(u"dataCurrentEntry")
        self.dataCurrentEntry.setEnabled(False)
        self.dataCurrentEntry.setGeometry(QRect(110, 20, 91, 41))
        self.dataCurrentEntry.setMinimum(0)
        self.dataCurrentEntry.setMaximum(99)
        self.dataCurrentEntry.setValue(0)
        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.dataCurrentEntry_2 = QSpinBox(self.tab_4)
        self.dataCurrentEntry_2.setObjectName(u"dataCurrentEntry_2")
        self.dataCurrentEntry_2.setEnabled(False)
        self.dataCurrentEntry_2.setGeometry(QRect(110, 20, 91, 41))
        self.dataCurrentEntry_2.setMinimum(0)
        self.dataCurrentEntry_2.setMaximum(99)
        self.dataCurrentEntry_2.setValue(0)
        self.label_38 = QLabel(self.tab_4)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setEnabled(False)
        self.label_38.setGeometry(QRect(10, 20, 81, 41))
        self.label_38.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.groupBox_3 = QGroupBox(self.tab_4)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setEnabled(False)
        self.groupBox_3.setGeometry(QRect(10, 90, 451, 241))
        self.groupBox_3.setFont(font3)
        self.groupBox_3.setAlignment(Qt.AlignCenter)
        self.groupBox_3.setFlat(False)
        self.dataEntryParameter_3 = QLineEdit(self.groupBox_3)
        self.dataEntryParameter_3.setObjectName(u"dataEntryParameter_3")
        self.dataEntryParameter_3.setEnabled(False)
        self.dataEntryParameter_3.setGeometry(QRect(110, 40, 331, 22))
        self.dataEntryParameter_3.setFont(font2)
        self.label_42 = QLabel(self.groupBox_3)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setEnabled(False)
        self.label_42.setGeometry(QRect(10, 120, 71, 41))
        self.label_42.setFont(font1)
        self.label_42.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_43 = QLabel(self.groupBox_3)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setEnabled(False)
        self.label_43.setGeometry(QRect(10, 80, 71, 21))
        self.label_43.setFont(font1)
        self.label_43.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.dataEntryParameter_4 = QLineEdit(self.groupBox_3)
        self.dataEntryParameter_4.setObjectName(u"dataEntryParameter_4")
        self.dataEntryParameter_4.setEnabled(False)
        self.dataEntryParameter_4.setGeometry(QRect(110, 80, 331, 22))
        self.dataEntryParameter_4.setFont(font2)
        self.label_44 = QLabel(self.groupBox_3)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setEnabled(False)
        self.label_44.setGeometry(QRect(10, 40, 71, 21))
        self.label_44.setFont(font1)
        self.label_44.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.dataEntryRail = QSpinBox(self.groupBox_3)
        self.dataEntryRail.setObjectName(u"dataEntryRail")
        self.dataEntryRail.setEnabled(False)
        self.dataEntryRail.setGeometry(QRect(110, 120, 91, 41))
        self.dataEntryRail.setMinimum(-1)
        self.dataEntryRail.setValue(-1)
        self.label_45 = QLabel(self.groupBox_3)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setEnabled(False)
        self.label_45.setGeometry(QRect(10, 180, 71, 41))
        self.label_45.setFont(font1)
        self.label_45.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.dataEntryPoint = QSpinBox(self.groupBox_3)
        self.dataEntryPoint.setObjectName(u"dataEntryPoint")
        self.dataEntryPoint.setEnabled(False)
        self.dataEntryPoint.setGeometry(QRect(110, 180, 91, 41))
        self.dataEntryPoint.setMinimum(-1)
        self.dataEntryPoint.setValue(-1)
        self.tabWidget_2.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.dataCurrentEntry_3 = QSpinBox(self.tab_5)
        self.dataCurrentEntry_3.setObjectName(u"dataCurrentEntry_3")
        self.dataCurrentEntry_3.setEnabled(False)
        self.dataCurrentEntry_3.setGeometry(QRect(110, 20, 91, 41))
        self.dataCurrentEntry_3.setMinimum(0)
        self.dataCurrentEntry_3.setMaximum(99)
        self.dataCurrentEntry_3.setValue(0)
        self.groupBox_4 = QGroupBox(self.tab_5)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setEnabled(False)
        self.groupBox_4.setGeometry(QRect(10, 90, 451, 81))
        self.groupBox_4.setFont(font3)
        self.groupBox_4.setAlignment(Qt.AlignCenter)
        self.groupBox_4.setFlat(False)
        self.label_32 = QLabel(self.groupBox_4)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setEnabled(False)
        self.label_32.setGeometry(QRect(10, 40, 71, 21))
        self.label_32.setFont(font1)
        self.label_32.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.dataHostActorID = QLineEdit(self.groupBox_4)
        self.dataHostActorID.setObjectName(u"dataHostActorID")
        self.dataHostActorID.setGeometry(QRect(110, 40, 331, 22))
        self.label_35 = QLabel(self.tab_5)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setEnabled(False)
        self.label_35.setGeometry(QRect(10, 20, 81, 41))
        self.label_35.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.tabWidget_2.addTab(self.tab_5, "")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.tabWidget.raise_()
        self.label_2.raise_()
        self.listWidget.raise_()
        self.addButton.raise_()
        self.delButton.raise_()
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 800, 22))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.comboBox.setCurrentIndex(4)
        self.comboBox_2.setCurrentIndex(4)
        self.comboBox_4.setCurrentIndex(4)
        self.comboBox_3.setCurrentIndex(4)
        self.comboBox_5.setCurrentIndex(0)
        self.comboBox_6.setCurrentIndex(0)
        self.comboBox_7.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"&Open", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"&Save", None))
        self.actionSaveAs.setText(QCoreApplication.translate("MainWindow", u"&Save As", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"&Close", None))
        self.actionActors.setText(QCoreApplication.translate("MainWindow", u"&Actors", None))
        self.actionPoints.setText(QCoreApplication.translate("MainWindow", u"&Points", None))
        self.actionRails.setText(QCoreApplication.translate("MainWindow", u"Rails", None))
        self.actionGrid.setText(QCoreApplication.translate("MainWindow", u"&Grid", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Actors", None))
        self.addButton.setText(QCoreApplication.translate("MainWindow", u"Add Actor", None))
        self.delButton.setText(QCoreApplication.translate("MainWindow", u"Delete Actor", None))
        self.groupBox.setTitle("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Type", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Position", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Rotation", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Scale", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Z", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Switches", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Local Flag", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Global Flag", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Hardcoded Value", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Panel Flag", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"Unused", None))

        self.label_17.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("MainWindow", u"Local Flag", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("MainWindow", u"Global Flag", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("MainWindow", u"Hardcoded Value", None))
        self.comboBox_2.setItemText(3, QCoreApplication.translate("MainWindow", u"Panel Flag", None))
        self.comboBox_2.setItemText(4, QCoreApplication.translate("MainWindow", u"Unused", None))

        self.label_27.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.comboBox_4.setItemText(0, QCoreApplication.translate("MainWindow", u"Local Flag", None))
        self.comboBox_4.setItemText(1, QCoreApplication.translate("MainWindow", u"Global Flag", None))
        self.comboBox_4.setItemText(2, QCoreApplication.translate("MainWindow", u"Hardcoded Value", None))
        self.comboBox_4.setItemText(3, QCoreApplication.translate("MainWindow", u"Panel Flag", None))
        self.comboBox_4.setItemText(4, QCoreApplication.translate("MainWindow", u"Unused", None))

        self.comboBox_3.setItemText(0, QCoreApplication.translate("MainWindow", u"Local Flag", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("MainWindow", u"Global Flag", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("MainWindow", u"Hardcoded Value", None))
        self.comboBox_3.setItemText(3, QCoreApplication.translate("MainWindow", u"Panel Flag", None))
        self.comboBox_3.setItemText(4, QCoreApplication.translate("MainWindow", u"Unused", None))

        self.label_5.setText(QCoreApplication.translate("MainWindow", u"ID", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Main Data", None))
        self.comboBox_5.setItemText(0, QCoreApplication.translate("MainWindow", u"Is Enemy Actor:  False", None))
        self.comboBox_5.setItemText(1, QCoreApplication.translate("MainWindow", u"Is Enemy Actor:  True", None))

        self.comboBox_5.setCurrentText(QCoreApplication.translate("MainWindow", u"Is Enemy Actor:  False", None))
        self.comboBox_6.setItemText(0, QCoreApplication.translate("MainWindow", u"Checks For Kills:  False", None))
        self.comboBox_6.setItemText(1, QCoreApplication.translate("MainWindow", u"Checks For Kills:  True", None))

        self.comboBox_7.setItemText(0, QCoreApplication.translate("MainWindow", u"+Enemies Tile:  False", None))
        self.comboBox_7.setItemText(1, QCoreApplication.translate("MainWindow", u"+Enemies Tile:  True", None))

        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Current Entry", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Entry Data", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Parameter 2", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Parameter 1", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Actor ID", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Actors To Control", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Current Entry", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Entry Data", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"Rail Index", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Parameter 2", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Parameter 1", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"Point Index", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Positions To Use", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Entry Data", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Actor ID", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Current Entry", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Actors That Use Me", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Relationships", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
    # retranslateUi

