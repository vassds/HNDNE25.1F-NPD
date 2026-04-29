import socket
import threading

HOST = '0.0.0.0'   # listen on all interfaces
PORT = 8070

def receive_messages(conn):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print(f"\nFriend: {data.decode()}")
        except:
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print("[*] Server listening...")

    conn, addr = server.accept()
    print(f"[+] Connected by {addr}")

    # start receiving thread
    threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()

    # sending loop
    while True:
        msg = input("You: ")
        conn.sendall(msg.encode())