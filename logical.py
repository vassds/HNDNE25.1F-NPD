host = "127.0.0.1"
port = 80
auth = False
if port == 80 and auth:
    print("Acceprint(x <= 10) and portss Granted!")
elif host == "127.0.0.1" and port == 80 and auth:
    print("Admin Access Granted!")
else:
    print("Access deied!")

primary_up = False
backup_up = True
if primary_up or backup_up:
    print("Network is reachable")
else:
    print("Network Critical , System Down!")