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

    @Slot(int)
    def add_score(self, score: int):
        self.score += score
        self.ui.label_score.setText(str(self.score))
