from PySide6.QtWidgets import QApplication
from widget.MainWindow import MainWindow


def main():
    app = QApplication()

    main_window = MainWindow(None)
    main_window.show()

    return app.exec()


if __name__ == "__main__":
    main()
