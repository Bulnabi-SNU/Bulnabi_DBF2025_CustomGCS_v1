from PyQt5.QtSerialPort import QSerialPort
from PyQt5.QtCore import QIODevice
from PyQt5.QtWidgets import QMessageBox
import json
from datetime import datetime

class HandlerSerial:
    def __init__(self, controller):
        self.controller = controller
        self.serial_port = QSerialPort()
        self.serial_connected = False

    def connect_serial(self):
        selected_port = self.controller.ui.CB_SER_PORT.currentData()
        if not self.serial_connected:
            self.serial_port.setPortName(selected_port)
            self.serial_port.setBaudRate(int(self.controller.ui.LE_SER_BAUD.text()))
            self.serial_port.setDataBits(QSerialPort.Data8)
            self.serial_port.setParity(QSerialPort.NoParity)
            self.serial_port.setStopBits(QSerialPort.OneStop)
            self.serial_port.setFlowControl(QSerialPort.NoFlowControl)

            if self.serial_port.open(QIODevice.ReadWrite):
                self.serial_connected = True
                self.controller.ui.PB_SER_CONN.setText("Connected!")
                self.serial_port.readyRead.connect(self.handle_ready_read)
            else:
                QMessageBox.critical(self.controller.ui, "Error", "Failed to open serial port.")
        else:
            self.serial_connected = False
            self.serial_port.close()
            self.controller.ui.PB_SER_CONN.setText("Connect\nSerial")

    def handle_ready_read(self):
        while self.serial_port.canReadLine():
            line = self.serial_port.readLine().data().decode("utf-8").strip()
            if line[0] == '{':
                try:
                    data = json.loads(line)

                    curr_datetime = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    print(curr_datetime, ' | Packet Size : ', len(line))

                    recv_r  = data.get("r",  0.0)
                    recv_p  = data.get("p",  0.0)
                    recv_y  = data.get("y",  0.0)
                    recv_raw_acc_x = data.get("ax", 0.0)
                    recv_raw_acc_y = data.get("ay", 0.0)
                    recv_raw_acc_z = data.get("az", 0.0)
                    recv_lin_acc_x = data.get("lax", 0.0)
                    recv_lin_acc_y = data.get("lay", 0.0)
                    recv_lin_acc_z = data.get("laz", 0.0)
                    recv_raw_ang_x = data.get("gx", 0.0)
                    recv_raw_ang_y = data.get("gy", 0.0)
                    recv_raw_ang_z = data.get("gz", 0.0)
                    recv_raw_mag_x = data.get("mx", 0.0)
                    recv_raw_mag_y = data.get("my", 0.0)
                    recv_raw_mag_z = data.get("mz", 0.0)
                    
                    self.controller.plot_handler_cur_r.update_plot(recv_r)
                    self.controller.plot_handler_cur_p.update_plot(recv_p)
                    self.controller.plot_handler_cur_y.update_plot(recv_y)
                    self.controller.plot_handler_mag_xy.update_plot(recv_raw_mag_x)
                    self.controller.plot_handler_mag_yz.update_plot(recv_raw_mag_y)
                    self.controller.plot_handler_mag_zx.update_plot(recv_raw_mag_z)

                    # self.controller.ui.TE_RX_RAW.setText(line)
                    pretty_data = json.dumps(data, indent=4, ensure_ascii=False)  # 보기 좋게 포매팅
                    self.controller.ui.TE_RX_RAW.setText(pretty_data)

                except ValueError:
                    print(f"Invalid data: {line}")
            else:
                print("Debug Msg : ", line)

                # 기존 텍스트 가져오기
                text_edit = self.controller.ui.TE_RX_DEBUG
                existing_text = text_edit.toPlainText()

                # 줄 단위로 분리
                lines = existing_text.split('\n')

                # 100줄 초과 시 가장 오래된 줄 제거
                if len(lines) >= 100:
                    lines = lines[-99:]  # 최근 99줄만 유지

                # 새로운 줄 추가
                curr_datetime = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                lines.append(curr_datetime + " : " + line)

                # 텍스트 업데이트
                text_edit.setPlainText('\n'.join(lines).strip())
                text_edit.verticalScrollBar().setValue(text_edit.verticalScrollBar().maximum())  # 스크롤 아래로 이동
