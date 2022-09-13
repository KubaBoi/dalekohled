import time
import socket

from src.tools.arduinoControll import ArduinoController

class SocketServer:
    def __init__(self):
        pass

    def serve_forever(self):

        self.HOST = ""
        self.PORT = 55573

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                s.bind((self.HOST, self.PORT))
                s.listen(5)
                print(f"Running...")
                break
            except Exception as e:
                print(f"Connection is old. Turn of controll script.")
                time.sleep(2)


        conn, addr = s.accept()
        print(f"Connected by {addr}")

        while True:
            try:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break

                    request = data.decode("utf-8")
                    ArduinoController.write(request)

            except Exception as e:
                print(f"Disconnected by {addr}")
                print(f"{str(e)}")
                print(f"Waiting...")
                conn, addr = s.accept()
                print(f"Connected by {addr}")


