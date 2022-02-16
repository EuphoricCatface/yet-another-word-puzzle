from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QObject, QTimer

from widget.ui_MainWindow import Ui_MainWindow

from time import monotonic


class MainWindow(QMainWindow):
    def __init__(self, parent):
        super(MainWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(QObject.tr("Puzzle Test"))

        self.ui.frame_Board.score_add.connect(self.ui.frame_Top.add_score)
        self.ui.frame_Board.char_list_update.connect(self.ui.frame_Top.word_display)
        self.ui.frame_Board.char_list_deactivate.connect(self.ui.frame_Top.word_deactivate)
        self.ui.frame_Top.game_over.connect(self.ui.frame_Board.game_over)

        self.game_timer = QTimer()
        self.game_timer.setInterval(100)
        self.game_timer.timeout.connect(self.update_statusbar)

        # self.ui.frame_Top.ui.pushButton_start.clicked.connect(self.ui.frame_Board.game_init)
        # self.ui.frame_Top.ui.pushButton_start.clicked.connect(self.game_timer.start)
        self.ui.frame_Top.game_over.connect(self.update_statusbar)
        self.ui.frame_Top.game_over.connect(self.game_timer.stop)

        self.ui.actionNew.triggered.connect(self.ui.frame_Top.init_game)
        self.ui.actionNew.triggered.connect(self.ui.frame_Top.game_timer.start)
        self.ui.actionNew.triggered.connect(self.ui.frame_Board.game_init)
        self.ui.actionNew.triggered.connect(self.game_timer.start)
        # TODO: De-/activate undo/redo on condition
        self.ui.actionUndo.triggered.connect(self.ui.frame_Board.undo)
        self.ui.actionRedo.triggered.connect(self.ui.frame_Board.redo)

        self.adjustSize()

    def update_statusbar(self):
        timer = monotonic() - self.ui.frame_Top.game_start_time
        found = self.ui.frame_Top.game_found_words
        self.ui.statusbar.showMessage(f"Timer: {int(timer)}, Found {found} ")
