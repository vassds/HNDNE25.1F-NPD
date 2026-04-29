from ping3 import ping

target_ips = ("8.8.8.8", "10.0.0.99")

for ip in target_ips:
    response = ping(ip)

    if response is not None:
        print(f"[UP] {ip} responded.")
    else:
        print(f"[DOWN] {ip} timed out.")