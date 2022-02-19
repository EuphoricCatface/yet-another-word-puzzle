from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QDrag, QDropEvent, QDragEnterEvent, QDragLeaveEvent
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtCore import QMimeData, QByteArray, QPoint
from PySide6.QtCore import QParallelAnimationGroup, QPropertyAnimation, QEasingCurve
from widget import TileButton

from backend import board
import time

TILE_COLUMNS = 5
TILE_ROWS = 5


class BoardWidget(QFrame):
    char_list_update = Signal(str, int)
    char_list_deactivate = Signal()
    score_add = Signal(int)
    score_undo = Signal(int)
    current_game_seed = Signal(str)

    def __init__(self, parent):
        super(BoardWidget, self).__init__(parent)

        self.setMinimumSize(200, 200)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)

        self.board = board.Board()
        self.drag_start_time = 0
        self.last_game_over_time = 0

        self.next_game_seed = None

        self.button_columns: [list[list[TileButton.TileButton]]] = [
            [TileButton.TileButton(self) for _ in range(5)]
            for _ in range(5)
        ]

        self.drop_animation_group = QParallelAnimationGroup()
        self.to_be_collected: list[TileButton.TileButton] = []

        self.board.empty()
        self.board_sync()

    @Slot()
    def game_init(self):
        seed = None
        self.setEnabled(True)
        if self.next_game_seed:
            seed = self.board.game_setup(self.next_game_seed)
            assert seed == self.next_game_seed
            self.next_game_seed = None
        else:
            seed = self.board.game_setup()
        self.board.fill_prepare()
        self.board_sync()
        self.drop_animation()

        self.current_game_seed.emit(seed)

    @Slot(str)
    def set_next_seed(self, seed: str):
        self.next_game_seed = None
        # If check fails, make the seed unset

        if not seed:
            # This is intended seed unset
            return False

        assert len(seed) == 32
        try:
            int(seed, 16)
        except ValueError:
            assert False

        self.next_game_seed = seed
        print("seed set")
        return True

    def board_sync(self):
        for x, column in enumerate(self.board.columns):
            for y, tile in enumerate(column):
                if len(self.button_columns[x]) == y:
                    self.button_columns[x].append(TileButton.TileButton(self))
                e = self.button_columns[x][y]
                e.move(x * 40 + 5, 200 - (y + 1) * 40 + 5)
                e.setFixedSize(30, 30)
                e.set_tile(tile)
                e.x_board = x
                e.y_board = y

    def drop_animation(self):
        def animate(pos: QPoint, dist: int, animation_: QPropertyAnimation):
            dummy_fall_unit = 40
            current_pos = pos
            new_pos = QPoint(
                current_pos.x(), current_pos.y() + dist * dummy_fall_unit,
            )
            animation_.setDuration(500)
            animation_.setStartValue(current_pos)
            animation_.setEndValue(new_pos)
            animation_.setEasingCurve(QEasingCurve.OutCubic)
            return animation_

        # Update the actual board before the animation,
        #  Collect UI elements after the animation
        self.board.eliminate_empty()
        self.drop_animation_group = QParallelAnimationGroup()
        self.drop_animation_group.finished.connect(self.collect_empty_button)

        animation_prepare = self.board.fall_distance

        for x, column in enumerate(animation_prepare):
            remove_later = []
            for y, distance in enumerate(column):
                if distance == 0:
                    continue

                target = self.button_columns[x][y]
                if distance == -1:
                    target.set_ascii(0)
                    self.to_be_collected.append(target)
                    remove_later.append(target)
                    continue

                target.y_board -= distance
                if target.y_board < TILE_ROWS:
                    target.show()
                animation = QPropertyAnimation(target, QByteArray('pos'), target)
                self.drop_animation_group.addAnimation(
                    animate(target.pos(), distance, animation)
                )

            for i in remove_later:
                self.button_columns[x].remove(i)

        self.drop_animation_group.start()

    def collect_empty_button(self):
        count = 0
        while self.to_be_collected:
            self.to_be_collected.pop().close()
            count += 1
        # print(f"closed {count} buttons")

    def start_drag(self, x, y) -> None:
        self.drag_start_time = time.monotonic()
        if self.board.is_selecting:
            print("Previous drag seem to have ended up elsewhere")
            print("-> Ignoring new drag")
            self.end_tile()
            return

        # print((x, y))
        # print("Board")
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
            # print("dragEnter_no: board")
            event.ignore()
            return

        # print("dragEnter: board")
        event.accept()

    def dragLeaveEvent(self, event: QDragLeaveEvent) -> None:
        # print("dragLeave: board")
        super(BoardWidget, self).dragLeaveEvent(event)

    def dropEvent(self, event:QDropEvent) -> None:
        if event.source() != self:
            # print("dragDrop_no: board")
            event.ignore()

        # print("event drop: board")
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

        score = self.board.eval_score()
        word = self.board.get_current_word()
        if not self.board.eval_word():
            score = -score
        self.char_list_update.emit(word, score)

    def end_tile(self):
        if self.drag_start_time < self.last_game_over_time:
            print("WORKAROUND: drag started before the last game ended")
            return

        word = self.board.end_select()
        for coord in self.board.current_coord_seq:
            x, y = coord
            self.button_columns[x][y].setChecked(False)
        print(self.board.get_current_word(), flush=True)
        self.char_list_deactivate.emit()

        score = self.board.eval_after_select()
        if score > 0:
            print(f"word {score=}")
            self.score_add.emit(score)
            self.board.fill_prepare()
            self.board_sync()
            self.drop_animation()

    @Slot()
    def game_over(self):
        self.last_game_over_time = time.monotonic()
        self.setEnabled(False)

    @Slot()
    def undo(self):
        _move, score = self.board.undo()
        # TODO: undo animation
        self.board_sync()
        self.score_undo.emit(score)

    @Slot()
    def redo(self):
        score = self.board.redo()
        self.score_add.emit(score)
        # TODO: redo animation
        self.board_sync()
        self.drop_animation()
