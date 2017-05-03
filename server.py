import ssl
import socket

host = 'localhost'
port = 8000


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_socket = ssl.wrap_socket(socket,
                    certfile='certificate.pem',
                    keyfile = 'key.pem',
                    cert_reqs=ssl.CERT_REQUIRED)

ssl_socket.connect((host,port))

print("ssl socket connected")
