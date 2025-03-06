from LevelEditorUI.States import draw, idle, read
from enum import Enum, auto


class EditorState(Enum):
    IDLE = auto()
    READ = auto()
    DRAW = auto()
    EDIT = auto()
    SAVE = auto()


class StateMachine:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.changeToIdle()


    def changeToIdle(self) -> None:
        self.state = EditorState.IDLE
        idle.IdleState(self.parent)


    def changeToRead(self, dragged_file=None) -> None:
        self.state = EditorState.READ
        read.ReadState(self.parent, dragged_file)


    def changeToDraw(self, toggle_hide=False, hide_empty_sprites=True) -> None:
        self.state = EditorState.DRAW
        draw.DrawState(self.parent, toggle_hide, hide_empty_sprites)
        self.changeToEdit() # automatically change to the edit state once the drawing is done


    def changeToEdit(self) -> None:
        self.state = EditorState.EDIT


    def isDrawMode(self) -> bool:
        return self.state == EditorState.DRAW


    def isEditMode(self) -> bool:
        return self.state == EditorState.EDIT
