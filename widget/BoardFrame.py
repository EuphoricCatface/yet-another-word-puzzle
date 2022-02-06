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

        self.button_columns: [list[list[TileButton.TileButton]]] = [
            [TileButton.TileButton(self) for _ in range(5)]
            for _ in range(5)
        ]
        for x, column in enumerate(self.button_columns):
            for y, e in enumerate(column):
                e.move(x * 40 + 5, 200 - (y + 1) * 40 + 5)
                e.setFixedSize(30, 30)
                e.setText(chr(self.board.columns[x][y]))
                e.x = x
                e.y = y

    def start_drag(self, x, y) -> None:
        print((x, y))
        print("Board")
        self.board.start_select(x, y)

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
        self.end_tile()
        event.accept()

    def next_tile(self, x, y):
        if not self.board.next_select(x, y):
            return

        if self.board.deselect:
            x_, y_ = self.board.deselect
            self.button_columns[x_][y_].setChecked(False)

        x_, y_ = self.board.current_coord_seq[-1]
        self.button_columns[x_][y_].setChecked(True)

    def end_tile(self):
        word = self.board.end_select()
        for coord in self.board.current_coord_seq:
            x, y = coord
            self.button_columns[x][y].setChecked(False)
        print("".join(word), flush=True)
        self.board.selection_clear()
