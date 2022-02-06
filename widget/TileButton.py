from PySide6.QtWidgets import QPushButton, QLabel

from PySide6.QtGui import QMouseEvent, QDragEnterEvent, QDropEvent, QResizeEvent
from backend.board import LETTER_SCORE


class TileButton(QPushButton):
    def __init__(self, parent):
        super(TileButton, self).__init__(parent)

        self.setCheckable(True)
        self.setAcceptDrops(True)
        self.character = ' '

        self.x_board = 0
        self.y_board = 0

        # TODO: Show score for letter
        self.letter_label = QLabel(self)

    def resizeEvent(self, event:QResizeEvent) -> None:
        self.letter_label_resize()
        super(TileButton, self).resizeEvent(event)

    def letter_label_resize(self):
        sz = self.size()
        self.letter_label.setGeometry(
            0, 0,
            int(sz.width() / 2), int(sz.height() / 2)
        )
        self.letter_label.setStyleSheet("font-size: 8px; text-align: center;")

    def set_char(self, char: str):
        # TODO: Handle other infos, score and bonus
        self.character = char
        self.setText(char)
        if char != ' ':
            self.letter_label.setText(
                ' ' + str(LETTER_SCORE[ord(char) - ord('A')])
            )

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
        # print(e.pos())
        # print(self.text())
        self.parent().start_drag(self.x_board, self.y_board)

    def dragEnterEvent(self, event:QDragEnterEvent) -> None:
        if event.source() != self.parent():
            # print("dragEnter_no: tile")
            event.ignore()
            return

        # print("dragEnter: tile")
        self.parent().next_tile(self.x_board, self.y_board)
        event.accept()

    def dropEvent(self, event:QDropEvent) -> None:
        # print("event drop: tile")
        self.parent().end_tile()
