from LevelEditorUI.States import close, draw, idle, read, save, setup
from enum import Enum, auto


class EditorState(Enum):
    SETUP = auto()
    IDLE = auto()
    READ = auto()
    DRAW = auto()
    EDIT = auto()
    SAVE = auto()
    CLOSE = auto()


class StateMachine:
    def __init__(self, window) -> None:
        self.window = window


    def changeToSetup(self) -> None:
        self.state = EditorState.SETUP
        setup.SetupState(self.window)
        self.changeToIdle()


    def changeToIdle(self) -> None:
        self.state = EditorState.IDLE
        idle.IdleState(self.window)


    def changeToRead(self, dragged_file=None) -> None:
        self.state = EditorState.READ
        read.ReadState(self.window, dragged_file)


    def changeToDraw(self, toggle_hide=False, hide_empty_sprites=True) -> None:
        self.state = EditorState.DRAW
        draw.DrawState(self.window, toggle_hide, hide_empty_sprites)
        self.changeToEdit()


    def changeToEdit(self) -> None:
        self.state = EditorState.EDIT


    def changeToSave(self) -> None:
        self.state = EditorState.SAVE
        save.SaveState(self.window)


    def changeToClose(self, event) -> None:
        self.state = EditorState.CLOSE
        close.CloseState(self.window, event)


    def isDrawMode(self) -> bool:
        return self.state == EditorState.DRAW


    def isEditMode(self) -> bool:
        return self.state == EditorState.EDIT
