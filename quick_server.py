from http.server import BaseHTTPRequestHandler, HTTPServer
from PIL import Image, UnidentifiedImageError
import base64
import io
import base64
from binascii import Error as BinasciiError

host = '0.0.0.0'  # Replace with your server's IP address
port = 12345  # Replace with your desired port number

def read_base64_data(data: str):
    base64_string = data
    image_data = base64.b64decode(base64_string)

    image = Image.open(io.BytesIO(image_data))

    image.save("image.jpg")






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

        data = body.decode()[:-1] # remove trailing \n


        read_base64_data(data)

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))



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


if __name__ == '__main__':
    main()
