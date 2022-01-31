from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtCore import QObject

from widget import BoardWidget


def main():
    app = QApplication()

    main_widget = QWidget()
    horizontal_layout = QHBoxLayout(main_widget)
    horizontal_layout.addWidget(BoardWidget.BoardWidget(main_widget))
    horizontal_layout.addWidget(BoardWidget.BoardWidget(main_widget))

    main_widget.setWindowTitle(QObject.tr("Puzzle Test"))
    main_widget.show()

    return app.exec()


if __name__ == "__main__":
    main()
