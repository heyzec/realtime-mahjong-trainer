from enum import Enum, auto
import base64
import io
import base64
from binascii import Error as BinasciiError
import socket
from typing import Callable
from engine import EngineResult
from recognition.utils import show

HOST = '0.0.0.0'
PORT = 55555

def read_base64_data(data: str):
    base64_string = data
    image_data = base64.b64decode(base64_string)

    image = Image.open(io.BytesIO(image_data))

    image.save("image.jpg")



class ServerState(Enum):
    empty = auto()
    partial = auto()


class Server:
    def __init__(self, callback, host: str, port: int):
        self.callback: Callable = callback
        self.host = host
        self.port = port
        self.buffer = bytearray()
        self.state = ServerState.empty
        self.remaining = 0

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.host, self.port))
            sock.listen()

            while True:

                conn, addr = sock.accept()
                print(f"Connected by f{addr}")
                with conn:
                    while True:
                        data = conn.recv(1024)
                        if (self.state == ServerState.empty):
                            try:
                                data_length = int(data[0:8].decode())
                            except Exception as e:
                                print(e)
                                raise


                            data = data[8:]
                            self.remaining = data_length

                        self.buffer.extend(data)
                        self.remaining -= len(data)

                        if self.remaining > 0:
                            self.state = ServerState.partial
                        else:
                            print("closing")
                            conn.close()
                            self.callback(bytes(self.buffer))
                            self.state = ServerState.empty
                            self.buffer = bytearray()
                            break

def callback(bytes):
    print(len(bytes))
    try:
        result = EngineResult.loads(bytes)
        stage = result.stage
        stage = stage.prev


        show(stage.display, block=False)

        print(result)
    except Exception as e:
        print(e)



def main():
    server = Server(callback, HOST, PORT)
    server.start()


if __name__ == '__main__':
    main()
