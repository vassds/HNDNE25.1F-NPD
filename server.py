import socket

HOST = '127.0.0.1'
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()

    print("[*] Server listening...")

    conn, addr = server.accept()
    with conn:
        print(f"[+] Connected by {addr}")
        data = conn.recv(1024)
        print(data.decode())

        conn.sendall(b"Hello from server")