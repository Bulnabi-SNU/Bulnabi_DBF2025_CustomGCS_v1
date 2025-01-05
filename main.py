from PyQt5.QtWidgets import QApplication
from core_controller import CoreController
from PyQt5.QtCore import Qt
from os import environ

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

if __name__ == "__main__":
    import sys
    suppress_qt_warnings()

    app = QApplication(sys.argv)
    controller = CoreController()
    controller.start()
    sys.exit(app.exec_())
