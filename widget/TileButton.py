from PySide6.QtWidgets import QPushButton, QLabel

from PySide6.QtGui import QMouseEvent, QDragEnterEvent, QDropEvent, QResizeEvent
from PySide6.QtCore import Qt
from backend.board import LETTER_SCORE, Tile


class TileButton(QPushButton):
    def __init__(self, parent):
        super(TileButton, self).__init__(parent)

        self.setCheckable(True)
        self.setAcceptDrops(True)
        self.character = ' '

        self.x_board = 0
        self.y_board = 0

        self.score_label = QLabel(self)
        self.score_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.bonus_label = QLabel(self)
        self.bonus_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setStyleSheet("font: bold")
        self.is_word = False

    def resizeEvent(self, event:QResizeEvent) -> None:
        self.letter_label_resize()
        self.bonus_label_resize()
        super(TileButton, self).resizeEvent(event)

    def letter_label_resize(self):
        sz = self.size()
        self.score_label.setGeometry(
            0, 0,
            sz.width() // 3, sz.height() // 2
        )
        self.score_label.setStyleSheet("font-size: 8px")

    def bonus_label_resize(self):
        sz = self.size()
        self.bonus_label.setGeometry(
            sz.width() - sz.width() // 3, sz.height() // 2 if self.is_word else 0,
            sz.width() // 3, sz.height() // 2
        )

    def set_char(self, char: str):
        self.character = char
        if char == ' ':
            self.score_label.setText(' ')
        else:
            self.score_label.setText(
                ' ' + str(LETTER_SCORE[ord(char) - ord('A')])
            )

        if char == 'Q':
            char = 'Qu'
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

    def set_tile(self, tile: Tile):
        self.set_ascii(tile.letter_ord)

        if not tile.bonus:
            self.bonus_label.hide()
            return

        self.bonus_label.setText(tile.bonus)
        style_sheet = "font: 8px; color: white"
        if tile.bonus[0] == 'T':
            style_sheet = "background-color: red; " + style_sheet
        elif tile.bonus[0] == 'D':
            style_sheet = "background-color: blue; " + style_sheet
        self.is_word = tile.bonus[1] == 'W'
        self.bonus_label.setStyleSheet(style_sheet)
        self.bonus_label.show()

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
