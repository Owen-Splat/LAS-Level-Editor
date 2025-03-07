from PySide6 import QtCore, QtWidgets, QtGui
import LevelEditorCore.Tools.conversions as convert


class PosLineEdit(QtWidgets.QLineEdit):
    """Allows moving the actor by using the arrow keys

    These directions go from negative to positive:
        X-axis: West -> East
        Y-axis: Down -> Up
        Z-axis: North -> South"""

    DIRECTIONS = {
        'X': (QtCore.Qt.Key_Left, QtCore.Qt.Key_Right),
        'Y': (QtCore.Qt.Key_Down, QtCore.Qt.Key_Up),
        'Z': (QtCore.Qt.Key_Up, QtCore.Qt.Key_Down)
    }

    def keyPressEvent(self, arg__1) -> None:
        super().keyPressEvent(arg__1)
        self.moveTile(arg__1.key())

    def moveTile(self, key) -> None:
        try:
            pos = convert.strToFloat(self.text())
        except ValueError:
            return

        dirs = self.DIRECTIONS[self.objectName()[-1]]
        if key == dirs[0]:
            amount = -self.window().snap_margin
        elif key == dirs[1]:
            amount = self.window().snap_margin
        else:
            return

        self.setText(str(pos + amount))
        self.window().state.changeToDraw()


class RotLineEdit(QtWidgets.QLineEdit):
    """Allows rotating the actor by using the arrow keys

    Rotating on the Y-axis is what we want to use in 99% of situations. The direction should be self explanatory

    Some actors have natural rotations that differ from most, but this tool automatically adjusts for them"""

    def keyPressEvent(self, arg__1) -> None:
        super().keyPressEvent(arg__1)
        self.rotateTile(arg__1.key())

    def rotateTile(self, key) -> None:
        if key == QtCore.Qt.Key_Down:
            rot = 0.0
        elif key == QtCore.Qt.Key_Right:
            rot = 90.0
        elif key == QtCore.Qt.Key_Up:
            rot = 180.0
        elif key == QtCore.Qt.Key_Left:
            rot = -90.0
        else:
            return

        self.setText(str(rot))
        self.window().state.changeToDraw()


class ActorLabel(QtWidgets.QLabel):
    actor_index = -1
    clicked = False

    def mousePressEvent(self, ev) -> None:
        if ev.button() == QtCore.Qt.MouseButton.LeftButton:
            ev.accept()
            self.clicked = True
            return
        ev.ignore()

    def mouseReleaseEvent(self, ev) -> None:
        if ev.button() == QtCore.Qt.MouseButton.LeftButton and self.clicked:
            ev.accept()
            self.clicked = False
            release_pos = ev.position()
            x_in_bounds = True if release_pos.x() > 0 and release_pos.x() < self.width() else False
            y_in_bounds = True if release_pos.y() > 0 and release_pos.y() < self.height() else False
            if x_in_bounds and y_in_bounds:
                self.window().ui.listWidget.setCurrentRow(self.actor_index)
            return
        ev.ignore()


class SelectedLabel(QtWidgets.QLabel):
    """A custom QLabel that flashes its opacity to indicate focus on this object"""

    def __init__(self, parent=None) -> None:
        super().__init__()
        self.setParent(parent)

        effect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        self.anim_1 = QtCore.QPropertyAnimation(effect, b"opacity")
        self.anim_1.finished.connect(self.startAnimation)
        self.anim_1.setDuration(750)
        self.values = [0.65, 1.0]
        self.startAnimation()

    def startAnimation(self) -> None:
        """Reverses the animation start & end values each time before running"""

        self.anim_1.setStartValue(self.values[0])
        self.anim_1.setEndValue(self.values[1])
        self.values.reverse()
        self.anim_1.start()

    def mouseMoveEvent(self, ev) -> None:
        if ev.buttons() == QtCore.Qt.MouseButton.LeftButton:
            ev.accept()
            drag = QtGui.QDrag(self)
            mime = QtCore.QMimeData()
            drag.setMimeData(mime)
            drag.exec_(QtCore.Qt.DropAction.MoveAction)


class roomView(QtWidgets.QFrame):
    def dragEnterEvent(self, event) -> None:
        event.accept()

    def dragMoveEvent(self, event) -> None:
        event.accept()
        actor_obj: SelectedLabel = self.findChildren(SelectedLabel)[0]
        new_pos = event.pos()
        updated_pos = QtCore.QPoint(new_pos.x() - round(actor_obj.width() / 2), new_pos.y() - round(actor_obj.height() / 2))

        if (new_pos.x() < (self.x() + self.width())) and (new_pos.y() < (self.y() + self.height())):
            unit_pixel_ratio = self.window().tile_pixel_size / self.window().tile_unit_size
            new_x = (updated_pos.x() + (actor_obj.width() / 2)) / unit_pixel_ratio
            new_y = (updated_pos.y() + (actor_obj.height() / 2)) / unit_pixel_ratio

            new_x = self.window().topleft[0] + new_x
            new_x = round(new_x / self.window().snap_margin) * self.window().snap_margin
            self.window().ui.dataPos_X.setText(str(new_x))
            new_x = round(((new_x - self.window().topleft[0]) * unit_pixel_ratio) - (actor_obj.width() / 2))

            if self.window().room_data.grid.info.room_type == '3D':
                new_y = self.window().topleft[1] + new_y
                new_y = round(new_y / self.window().snap_margin) * self.window().snap_margin
                self.window().ui.dataPos_Z.setText(str(new_y))
                new_y = round(((new_y - self.window().topleft[1]) * unit_pixel_ratio) - (actor_obj.height() / 2))
            else:
                new_y = round(new_y / self.window().snap_margin) * self.window().snap_margin
                self.window().ui.dataPos_Y.setText(str(new_y))
                new_y = round((12 - new_y) * unit_pixel_ratio)

            # we move the sprite and manually edit the position fields, no need to call drawRoom
            actor_obj.setGeometry(new_x, new_y, actor_obj.width(), actor_obj.height())
