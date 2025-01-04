from PyQt5.QtWidgets import QApplication
from core_controller import CoreController

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    controller = CoreController()
    controller.start()
    sys.exit(app.exec_())
