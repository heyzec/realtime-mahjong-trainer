from email.mime import image
import os
from PIL import Image, UnidentifiedImageError
import base64
import io
import socket
import base64
from binascii import Error as BinasciiError

def read_base64_data(data: str):


    # Decode the Base64 string received over the network
    base64_string = data
    image_data = base64.b64decode(base64_string)

    print("imagedat length:", len(image_data))

    with open('test.jpg', 'wb') as f:
        f.write(image_data)

    # Convert the byte data to a PIL Image
    image = Image.open(io.BytesIO(image_data))

    image.save("myfile.png")

    # Now you can work with the PIL Image object as needed
    # Does not work on nixos
    image.show()
    # os.system("xdg-open myfile.png")

host = '0.0.0.0'  # Replace with your server's IP address
port = 12345  # Replace with your desired port number



from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

class Handler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):

        if "Content-Length" in self.headers:
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
        elif "chunked" in self.headers.get("Transfer-Encoding", ""):
            body = b""
            while True:
                line = self.rfile.readline().strip()
                if len(line) == 0:
                    break
                chunk_length = int(line, 16)

                if chunk_length != 0:
                    chunk = self.rfile.read(chunk_length)
                    body += chunk

                # Each chunk is followed by an additional empty newline
                # that we have to consume.
                self.rfile.readline()

                # Finally, a chunk size of 0 is an end indication
                if chunk_length == 0:
                    break
        print("actual", len(body))

        data = body.decode()[:-1]
        print("frist10: ", repr(data[:10]))
        print("last10: ", repr(data[-10:]))


        with open("base64.txt", 'w') as f:
            f.write(data)



        # print(data)
        read_base64_data(data)

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Handler, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)


def main():
    # Set up the server
    httpd = HTTPServer((host, port), Handler)
    print('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd...\n')
    return


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Client connected: {client_address}")
            try:
                # Read Base64 data from the client
                read_base64_data(client_socket)

            except (BinasciiError, UnidentifiedImageError) as e:
                print(e)
                client_socket.close()

    except KeyboardInterrupt:
        print(e)
        pass

    finally:
        server_socket.close()



if __name__ == '__main__':
    main()
