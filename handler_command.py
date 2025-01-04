class HandlerCommand:
    def __init__(self, serial_handler):
        """
        :param serial_handler: HandlerSerial 인스턴스
        """
        self.serial_handler = serial_handler

    def send_command(self, command):
        """
        명령어를 시리얼 포트를 통해 전송합니다.
        :param command: 전송할 문자열 명령어
        """
        if self.serial_handler.serial_connected:
            full_command = command + '\n'  # 명령어 끝에 줄 바꿈 추가
            self.serial_handler.serial_port.write(full_command.encode('utf-8'))
            print(f"Command sent: {command}")
        else:
            print("Error: Serial port not connected.")
