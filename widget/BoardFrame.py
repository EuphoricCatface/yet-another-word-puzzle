from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QDrag, QDropEvent, QDragEnterEvent, QDragLeaveEvent
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtCore import QMimeData, QByteArray, QTimer, QPoint
from PySide6.QtCore import QParallelAnimationGroup, QPropertyAnimation, QEasingCurve
from widget import TileButton

from backend import board

TILE_COLUMNS = 5
TILE_ROWS = 5


class BoardWidget(QFrame):
    char_list_update = Signal(str)
    # FIXME: sync() logic is not ideal

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

        self.game_init()

        self.drop_animation_group = QParallelAnimationGroup()

    @Slot()
    def game_init(self):
        self.board.fill_prepare()
        self.board_sync()
        self.drop_animation()
        self.board.eliminate_empty()
        self.board_sync()

    def board_sync(self):
        for x, column in enumerate(self.board.columns):
            for y, ascii_ in enumerate(column):
                if len(self.button_columns[x]) == y:
                    self.button_columns[x].append(TileButton.TileButton(self))
                e = self.button_columns[x][y]
                e.move(x * 40 + 5, 200 - (y + 1) * 40 + 5)
                e.setFixedSize(30, 30)
                e.set_ascii(ascii_)
                e.x_board = x
                e.y_board = y
                # e.show()

    def drop_animation(self):
        def animate(pos: QPoint, animation_: QPropertyAnimation):
            current_pos = pos
            new_pos = QPoint(
                current_pos.x(), current_pos.y() + distance * dummy_fall_unit,
            )
            animation_.setDuration(200)
            animation_.setStartValue(current_pos)
            animation_.setEndValue(new_pos)
            animation_.setEasingCurve(QEasingCurve.InQuad)
            return animation_

        self.drop_animation_group = QParallelAnimationGroup()
        # self.drop_animation_group.finished.connect(self.board_sync)
        animation_prepare = self.board.fall_distance
        dummy_fall_unit = 40

        for x, column in enumerate(animation_prepare):
            remove_later = []
            # TODO: make remove_later into member variable, and then destroy in collect_empty_button
            #  Make fancy animation before elimination
            for y, distance in enumerate(column):
                if distance == 0:
                    continue

                target = self.button_columns[x][y]
                if distance == -1:
                    target.setText(' ')
                    target.close()
                    remove_later.append(target)
                    continue

                target.show()
                target.y_board -= distance
                animation = QPropertyAnimation(target, QByteArray('pos'), target)
                self.drop_animation_group.addAnimation(
                    animate(target.pos(), animation)
                )

            for i in remove_later:
                self.button_columns[x].remove(i)

        self.drop_animation_group.start()

    def collect_empty_button(self):
        pass

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

        if self.board.selection_eval():
            self.board.fill_prepare()
            self.board_sync()
            self.drop_animation()
            self.board.eliminate_empty()
            self.collect_empty_button()
