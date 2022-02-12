from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Slot
from widget.ui_TopFrame import Ui_Frame


class TopFrame(QFrame):
    def __init__(self, parent):
        super(TopFrame, self).__init__(parent)
        self.ui = Ui_Frame()
        self.ui.setupUi(self)

        self.score = 0
        self.ui.pushButton_start.clicked.connect(self.init_game)

        self.init_game()

        # TODO: Make game over rules
        #  Turns until score X
        #  Until X turns
        #  Until X seconds
        #  Score adds to the timer

        # TODO: Make game mechanic rules
        #  More high value tiles (complementary random)
        #  See before you go (penalty on retreat)

    @Slot()
    def init_game(self):
        self.init_score()
        self.init_word()

    @Slot(int)
    def add_score(self, score: int):
        self.score += score
        self.ui.label_score.setText(str(self.score))

    @Slot()
    def init_score(self):
        self.score = 0
        self.add_score(0)

    @Slot(str, int)
    def word_display(self, word, score):
        self.word_activate(True)

        if score < 0:
            self.ui.label_word.setStyleSheet("")
            score = -score
        else:
            self.ui.label_word.setStyleSheet("font: bold")

        self.ui.label_word.setText(word)
        self.ui.label_wordscore.setText(str(score))

    @Slot()
    def init_word(self):
        self.ui.label_word.setText("")
        self.ui.label_wordscore.setText("0")
        self.word_activate(False)

    @Slot()
    def word_activate(self, _bool: bool = True):
        self.ui.label_word.setEnabled(_bool)
        self.ui.label_wordscore.setEnabled(_bool)

    @Slot()
    def word_deactivate(self):
        self.word_activate(False)
