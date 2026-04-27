import socket

# Change this to your server's IP address
SERVER_IP = '127.0.0.1'
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"[*] Attempting to connect to {SERVER_IP}:{PORT}...")
    s.connect((SERVER_IP, PORT))

    # send a hardcoded message
    s.sendall(b"Hello Server! This is a test message")

    # wait for the reply
    data = s.recv(1024)
    print(f"Reply from server: {data.decode('utf-8')}")