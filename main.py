from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QObject

from widget.ui_MainWindow import Ui_MainWindow


def main():
    app = QApplication()

    main_window = QMainWindow()
    main_window.ui = Ui_MainWindow()
    main_window.ui.setupUi(main_window)

    main_window.setWindowTitle(QObject.tr("Puzzle Test"))
    main_window.show()

    main_window.ui.frame_Top.ui.pushButton_start.clicked.connect(main_window.ui.frame_Board.game_init)
    main_window.ui.frame_Board.score_add.connect(main_window.ui.frame_Top.add_score)

    return app.exec()


if __name__ == "__main__":
    main()
