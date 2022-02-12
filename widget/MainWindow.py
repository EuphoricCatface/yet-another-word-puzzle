from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QObject

from widget.ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent):
        super(MainWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(QObject.tr("Puzzle Test"))

        self.ui.frame_Top.ui.pushButton_start.clicked.connect(self.ui.frame_Board.game_init)
        self.ui.frame_Board.score_add.connect(self.ui.frame_Top.add_score)
        self.ui.frame_Board.char_list_update.connect(self.ui.frame_Top.word_display)
        self.ui.frame_Board.char_list_deactivate.connect(self.ui.frame_Top.word_deactivate)
