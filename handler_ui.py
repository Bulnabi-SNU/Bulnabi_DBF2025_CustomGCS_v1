from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5 import uic

form_class = uic.loadUiType("BulnabiCommandCenter.ui")[0]

class HandlerUI(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(1400, 900)

        self.serial_handler = None
        self.plot_handler = None
        self.command_handler = None

        # 버튼 이벤트 연결
        self.PB_SER_REFRESH.clicked.connect(self.refresh_ports)
        self.PB_SER_CONN.clicked.connect(self.connect_serial)
        self.PB_TX_CLEAR.clicked.connect(self.TE_TX_RAW.clear)
        self.PB_RX_CLEAR.clicked.connect(self.TE_RX_RAW.clear)
        self.PB_TX_CALI.clicked.connect(self.send_command)  # 명령 전송 버튼

    def set_serial_handler(self, serial_handler):
        self.serial_handler = serial_handler

    def set_plot_handler(self, plot_handler):
        self.plot_handler = plot_handler

    def set_command_handler(self, command_handler):
        self.command_handler = command_handler

    def refresh_ports(self):
        self.CB_SER_PORT.clear()
        available_ports = QSerialPortInfo.availablePorts()
        for port in available_ports:
            self.CB_SER_PORT.addItem(f"{port.portName()} - {port.description()}", port.portName())
        if not available_ports:
            self.CB_SER_PORT.addItem("No ports available")

    def connect_serial(self):
        if self.serial_handler:
            self.serial_handler.connect_serial()

    def send_command(self):
        """
        UI에서 명령어를 입력받아 CommandHandler를 통해 전송
        """
        if self.command_handler:
            command = "{\"cmd_cali\":1}"
            self.command_handler.send_command(command)
            self.TE_TX_RAW.append(f"Sent: {command}")  # 전송된 명령어를 텍스트 창에 추가
