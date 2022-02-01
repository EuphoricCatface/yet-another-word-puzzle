from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QMouseEvent, QDrag, QDropEvent, QDragEnterEvent, QDragLeaveEvent
from PySide6.QtCore import Qt, QPoint
from PySide6.QtCore import QMimeData, QByteArray
from widget import TileButton

TILE_COLUMNS = 5
TILE_ROWS = 5


class BoardWidget(QFrame):
    def __init__(self, parent):
        super(BoardWidget, self).__init__(parent)

        self.setMinimumSize(200, 200)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)

        button1 = TileButton.TileButton(self)
        button1.setText('a')
        button1.move(10, 10)
        button1.show()
        button1.setAttribute(Qt.WA_DeleteOnClose)

        button2 = TileButton.TileButton(self)
        button2.setText('b')
        button2.move(100, 10)
        button2.show()
        button2.setAttribute(Qt.WA_DeleteOnClose)

        button3 = TileButton.TileButton(self)
        button3.setText('c')
        button3.move(10, 80)
        button3.show()
        button3.setAttribute(Qt.WA_DeleteOnClose)

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
