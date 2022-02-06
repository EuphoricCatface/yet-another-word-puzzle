from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QDrag, QDropEvent, QDragEnterEvent, QDragLeaveEvent
from PySide6.QtCore import Qt, Signal
from PySide6.QtCore import QMimeData, QByteArray, QTimer, QPoint
from PySide6.QtCore import QParallelAnimationGroup, QPropertyAnimation, QEasingCurve
from widget import TileButton

from backend import board

TILE_COLUMNS = 5
TILE_ROWS = 5


class BoardWidget(QFrame):
    char_list_update = Signal(str)

    def __init__(self, parent):
        super(BoardWidget, self).__init__(parent)

        self.setMinimumSize(200, 200)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)

        self.board = board.Board()

        self.button_columns: [list[list[TileButton.TileButton]]] = [
            [TileButton.TileButton(self) for _ in range(5)]
            for _ in range(5)
        ]

        self.board.fill_prepare()
        self.board.eliminate_empty()
        self.board_update()

        self.animation_group = QParallelAnimationGroup()

    def board_update(self):
        # TODO: falling animation

        for x, column in enumerate(self.button_columns):
            for y, e in enumerate(column):
                e.move(x * 40 + 5, 200 - (y + 1) * 40 + 5)
                e.setFixedSize(30, 30)
                e.set_ascii(self.board.columns[x][y])
                e.x_board = x
                e.y_board = y
                e.show()

    def board_fill_prepare(self):
        self.board.fill_prepare()
        self.animation_group = QParallelAnimationGroup()
        animation_prepare = self.board.fall_distance
        dummy_fall_unit = 40

        for x, column in enumerate(animation_prepare):
            remove_later = []
            for y, distance in enumerate(column):
                if y >= TILE_ROWS:
                    continue
                if distance == 0:
                    continue

                target = self.button_columns[x][y]
                if distance == -1:
                    target.setText(' ')
                    target.close()
                    self.button_columns[x].append(TileButton.TileButton(self))
                    remove_later.append(target)
                    continue

                current_geo = target.pos()
                new_geo = QPoint(
                    current_geo.x(), current_geo.y() + distance * dummy_fall_unit,
                )
                animation = QPropertyAnimation(target, QByteArray('pos'), target)
                animation.setDuration(200)
                animation.setStartValue(current_geo)
                animation.setEndValue(new_geo)
                animation.setEasingCurve(QEasingCurve.InQuad)
                self.animation_group.addAnimation(animation)
            for i in remove_later:
                self.button_columns[x].remove(i)

        self.animation_group.start()
        print("animation group started")
        QTimer.singleShot(250, self.board_eliminate_empty)
        print("non block")

    def board_eliminate_empty(self):
        self.board.eliminate_empty()
        self.board_update()

    def start_drag(self, x, y) -> None:
        if self.board.is_selecting:
            print("Previous drag seem to have ended up elsewhere")
            print("-> Ignoring new drag")
            self.end_tile()
            return

        print((x, y))
        print("Board")
        self.board.start_select(x, y)
        self.button_columns[x][y].setChecked(True)

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
        update, char_list = self.board.next_select(x, y)
        if not update:
            return

        if self.board.deselect:
            x_, y_ = self.board.deselect
            self.button_columns[x_][y_].setChecked(False)
        else:
            self.button_columns[x][y].setChecked(True)

        self.char_list_update.emit("".join(char_list))

    def end_tile(self):
        word = self.board.end_select()
        for coord in self.board.current_coord_seq:
            x, y = coord
            self.button_columns[x][y].setChecked(False)
        print("".join(word), flush=True)

        self.board.selection_eval()
        self.board_fill_prepare()
