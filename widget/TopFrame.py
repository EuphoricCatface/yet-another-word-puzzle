from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Slot, Signal, QTimer
from widget.ui_TopFrame import Ui_Frame

import time


class TopFrame(QFrame):
    game_over = Signal()

    def __init__(self, parent):
        super(TopFrame, self).__init__(parent)
        self.ui = Ui_Frame()
        self.ui.setupUi(self)

        self.score = 0
        self.ui.pushButton_start.clicked.connect(self.init_game)

        self.game_start_time = 0
        self.game_found_words = 0

        self.init_game()

        self.game_timer = QTimer()
        self.game_timer.setInterval(100)
        self.game_timer.timeout.connect(self.game_over_check)

        self.ui.pushButton_start.clicked.connect(self.game_timer.start)
        self.game_over.connect(self.game_timer.stop)

        # TODO: Make game over rules
        #  Turns until score X
        #  Until X turns
        #  Until X seconds
        #  Score adds to the timer

        # TODO: Make game mechanic rules
        #  High risk high return (complementary random)
        #  Look before you leap (penalty on retreat)
        #  Leap of faith (Don't show if the word is valid)
        #  Allow undo
        #  Seeded random

    @Slot()
    def init_game(self):
        self.init_score()
        self.init_word()
        self.game_start_time = time.monotonic()
        self.game_found_words = 0

    @Slot(int)
    def add_score(self, score: int):
        self.score += score
        self.ui.label_score.setText(str(self.score))
        # counting a turn only when it's a valid word
        self.game_found_words += 1

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

    @Slot()
    def game_over_check(self):
        criteria = self.game_start_time
        remaining_rule = criteria + 90 - time.monotonic()

        self.ui.label_countdown.setText(str(int(remaining_rule)))
        if remaining_rule <= 0:
            self.game_over.emit()
