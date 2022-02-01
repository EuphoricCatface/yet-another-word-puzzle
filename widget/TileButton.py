from PySide6.QtWidgets import QPushButton

from PySide6.QtGui import QDrag
from PySide6.QtGui import QMouseEvent, QDragEnterEvent, QDragLeaveEvent, QDropEvent


class TileButton(QPushButton):
    def __init__(self, parent):
        super(TileButton, self).__init__(parent)

        self.setCheckable(True)
        self.setAcceptDrops(True)
        # self.character = char

        self.x = 0
        self.y = 0

    def mousePressEvent(self, e: QMouseEvent) -> None:
        print(e.pos())
        print(self.text())
        self.parent().start_drag(self.x, self.y)

    def dragEnterEvent(self, event:QDragEnterEvent) -> None:
        if event.source() != self.parent():
            print("dragEnter_no: tile")
            event.ignore()
            return

        print("dragEnter: tile")
        self.parent().next_tile(self.x, self.y)
        event.accept()

    # def dragLeaveEvent(self, event:QDragLeaveEvent) -> None:
    #     self.setChecked(False)
    #
    #     print("dragLeave: tile")
    #     super(TileButton, self).dragLeaveEvent(event)

    def dropEvent(self, event:QDropEvent) -> None:
        print("event drop: tile")
        self.parent().end_tile()
