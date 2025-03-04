from LevelEditorUI.States import draw, idle
from enum import Enum


class EditorState(Enum):
    IDLE = 0
    DRAW = 1
    EDIT = 2


class StateMachine:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.changeToIdle()


    def changeToIdle(self) -> None:
        self.state = EditorState.IDLE
        idle.IdleState(self.parent)


    def changeToDraw(self) -> None:
        self.state = EditorState.DRAW
        draw.DrawState(self.parent)
        self.changeToEdit() # automatically change to the edit state once the drawing is done


    def changeToEdit(self) -> None:
        self.state = EditorState.EDIT


    def isDrawMode(self) -> bool:
        return self.state == EditorState.DRAW


    def isEditMode(self) -> bool:
        return self.state == EditorState.EDIT
