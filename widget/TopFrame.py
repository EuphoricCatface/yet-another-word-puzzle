from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Slot
from widget.ui_TopFrame import Ui_Frame


class TopFrame(QFrame):
    def __init__(self, parent):
        super(TopFrame, self).__init__(parent)
        self.ui = Ui_Frame()
        self.ui.setupUi(self)

        self.score = 0
        self.ui.label_score.setText(str(self.score))

        self.word_init()

    @Slot(int)
    def add_score(self, score: int):
        self.score += score
        self.ui.label_score.setText(str(self.score))

    @Slot(str, int)
    def word_display(self, word, score):
        self.word_activate(True)

        self.ui.label_word.setText(word)
        self.ui.label_wordscore.setText(str(score))

    @Slot()
    def word_init(self):
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
