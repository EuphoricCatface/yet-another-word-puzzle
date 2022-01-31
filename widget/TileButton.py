from PySide6.QtWidgets import QPushButton


class TileButton(QPushButton):
    def __init__(self, parent):
        super(TileButton, self).__init__(parent)

        self.setAcceptDrops(True)
        # self.character = char
