from handler_ui import HandlerUI
from handler_serial import HandlerSerial
from handler_plot import HandlerPlot
from handler_command import HandlerCommand

class CoreController:
    def __init__(self):
        # UI 초기화
        self.ui = HandlerUI()
        
        # 핸들러 초기화
        self.serial_handler     = HandlerSerial(self)
        self.plot_handler_cur_r = HandlerPlot(self.ui.plot_cur_r, "Roll",  "deg")
        self.plot_handler_cur_p = HandlerPlot(self.ui.plot_cur_p, "Pitch", "deg")
        self.plot_handler_cur_y = HandlerPlot(self.ui.plot_cur_y, "Yaw",   "deg")
        self.plot_handler_mag_xy = HandlerPlot(self.ui.plot_mag_xy, "mag_xy", None, 200)
        self.plot_handler_mag_yz = HandlerPlot(self.ui.plot_mag_yz, "mag_yz", None, 200)
        self.plot_handler_mag_zx = HandlerPlot(self.ui.plot_mag_zx, "mag_zx", None, 200)
        self.command_handler    = HandlerCommand(self.serial_handler)

        # UI에 핸들러 연결
        self.ui.set_serial_handler(self.serial_handler)
        self.ui.set_plot_handler(self.plot_handler_cur_r)
        self.ui.set_command_handler(self.command_handler)

    def start(self):
        # UI 실행
        self.ui.show()
