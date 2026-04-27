import socket
import threading

SERVER_IP = '172.20.10.7'   # <-- CHANGE to your friend's IP
PORT = 8070

def receive_messages(s):
    while True:
        try:
            data = s.recv(1024)
            if not data:
                break
            print(f"\nFriend: {data.decode()}")
        except:
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"[*] Connecting to {SERVER_IP}:{PORT}...")
    s.connect((SERVER_IP, PORT))

    # start receiving thread
    threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

    # sending loop
    while True:
        msg = input("You: ")
        s.sendall(msg.encode())