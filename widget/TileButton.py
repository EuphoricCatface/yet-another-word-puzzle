from PySide6.QtWidgets import QPushButton

from PySide6.QtGui import QDrag
from PySide6.QtGui import QMouseEvent, QDragEnterEvent, QDragLeaveEvent, QDropEvent


class TileButton(QPushButton):
    def __init__(self, parent):
        super(TileButton, self).__init__(parent)

        self.setCheckable(True)
        self.setAcceptDrops(True)
        # self.character = char

    def mousePressEvent(self, e: QMouseEvent) -> None:
        print(e.pos())
        print(self.text())
        self.parent().start_drag(self.mapToParent(e.pos()))

    def dragEnterEvent(self, event:QDragEnterEvent) -> None:
        if event.source() != self.parent():
            print("dragEnter_no: tile")
            event.ignore()
            return

        print("dragEnter: tile")
        self.setChecked(True)
        event.accept()

    def dragLeaveEvent(self, event:QDragLeaveEvent) -> None:
        self.setChecked(False)

        print("dragLeave: tile")
        super(TileButton, self).dragLeaveEvent(event)

    def dropEvent(self, event:QDropEvent) -> None:
        print("event drop: tile")
