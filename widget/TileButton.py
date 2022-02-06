from PySide6.QtWidgets import QPushButton

from PySide6.QtGui import QMouseEvent, QDragEnterEvent, QDropEvent


class TileButton(QPushButton):
    def __init__(self, parent):
        super(TileButton, self).__init__(parent)

        self.setCheckable(True)
        self.setAcceptDrops(True)
        self.character = ' '

        self.x = 0
        self.y = 0

        # TODO: Show score for letter

    def set_char(self, char: str):
        # TODO: Handle other infos, score and bonus
        self.character = char
        self.setText(char)

    def set_ascii(self, ascii_: int):
        if ascii_ == 0:
            char = ' '
            self.setEnabled(False)
            self.setChecked(True)
            # self.setFlat(True)
        else:
            char = chr(ascii_)
            self.setEnabled(True)
            self.setChecked(False)
            # self.setFlat(False)
        self.set_char(char)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        print(e.pos())
        # print(self.text())
        self.parent().start_drag(self.x, self.y)

    def dragEnterEvent(self, event:QDragEnterEvent) -> None:
        if event.source() != self.parent():
            print("dragEnter_no: tile")
            event.ignore()
            return

        print("dragEnter: tile")
        self.parent().next_tile(self.x, self.y)
        event.accept()

    def dropEvent(self, event:QDropEvent) -> None:
        print("event drop: tile")
        self.parent().end_tile()
