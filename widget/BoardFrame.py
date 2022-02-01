from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QMouseEvent, QDrag, QDropEvent, QDragEnterEvent, QDragLeaveEvent
from PySide6.QtCore import Qt, QPoint
from PySide6.QtCore import QMimeData, QByteArray
from widget import TileButton

from backend import board

TILE_COLUMNS = 5
TILE_ROWS = 5


class BoardWidget(QFrame):
    def __init__(self, parent):
        super(BoardWidget, self).__init__(parent)

        self.setMinimumSize(200, 200)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)

        self.board = board.Board()
        self.board.fill_prepare()
        self.board.eliminate_empty()

        button_columns: [list[list[TileButton.TileButton]]] = [
            [TileButton.TileButton(self) for _ in range(5)]
            for _ in range(5)
        ]
        for x, column in enumerate(button_columns):
            for y, e in enumerate(column):
                e.move(x * 40, 200 - (y + 1) * 40)
                e.setFixedSize(40, 40)
                e.setText(chr(self.board.columns[x][y]))

    def start_drag(self, pos: QPoint) -> None:
        print(pos)
        print("Board")

        mime_data = QMimeData()
        item_data = QByteArray()
        mime_data.setData("application/x-puzzletile", item_data)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.exec(Qt.MoveAction)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.source() != self:
            print("dragEnter_no: board")
            event.ignore()
            return

        print("dragEnter: board")
        event.accept()

    def dragLeaveEvent(self, event: QDragLeaveEvent) -> None:
        print("dragLeave: board")
        super(BoardWidget, self).dragLeaveEvent(event)

    def dropEvent(self, event:QDropEvent) -> None:
        if event.source() != self:
            print("dragDrop_no: board")
            event.ignore()

        print("event drop: board")
        event.setDropAction(Qt.MoveAction)
        event.accept()
