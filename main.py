import sys
from os import environ

from PyQt5.QtWidgets import QApplication


def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


def main():
    # All files need to be imported after QApplication
    from ui_table import TableView

    _ = TableView()


if __name__ == "__main__":
    suppress_qt_warnings()

    app = QApplication([])
    main()
    sys.exit(app.exec())
