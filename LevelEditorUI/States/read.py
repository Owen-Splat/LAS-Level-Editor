from LevelEditorCore.Tools.FixedHash import leb
from LevelEditorCore.Data.data import ACTORS
from PySide6 import QtWidgets
from pathlib import Path
import copy


class ReadState:
    def __init__(self, window, dragged_file=None) -> None:
        if dragged_file:
            path = dragged_file
        else:
            dir = window.rom_path / 'region_common/level'
            if window.file:
                dir = window.file.parent
            path = QtWidgets.QFileDialog.getOpenFileName(window, 'Open File', str(dir), "Room files (*.leb)")[0]
            if not path.endswith(".leb"):
                return

        # temp idle state to reset the editor
        # transitions to draw state once the file is parsed, stays in idle if it can't
        window.state.changeToIdle()

        # now we want to store the file location, but in the output dir rather than romfs dir
        path = Path(path)

        try:
            with open(path, 'rb') as f:
                window.room_data = leb.Room(f.read())
            # AttributeError if the room does not have grid info, these rooms are not yet supported by this editor
            # We might be able to just use the MapStatic actor position to get the topleft of the room
            # This will require testing first to see if it holds up
            window.topleft = [window.room_data.grid.info.x_coord, window.room_data.grid.info.z_coord]
        except (AttributeError, FileNotFoundError, ValueError) as e:
            window.showError(e.args[0])
        else:
            self.enableEditor(window)
            file_name = path.name
            level_name = file_name.split('_')[0]
            window.file = window.out_path / 'region_common/level' / level_name / file_name
            window.setWindowTitle(f"{window.app_name} - {path.stem}")
            window.next_actor = 0
            window.state.changeToDraw(toggle_hide=True)


    def enableEditor(self, window) -> None:
        """Changes all the editor elements to an interactive state"""

        fields = window.ui.centralwidget.children()
        for field in fields:
            try:
                field.setProperty('enabled', True)
            except AttributeError: # some objects won't have this attribute
                pass
        abc_actors = list(copy.deepcopy(ACTORS))
        abc_actors.sort()
        for actor in abc_actors:
            if not actor.startswith(('Player', 'null')):
                window.ui.dataType.addItem(actor)
