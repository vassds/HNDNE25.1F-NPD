ips = ["192.168.10.1","192.068.10.2"]
source_ip = "192.168.10.5"

if source_ip in ips:
    print("Access granted")
else:
    print("Acces denied")

device_info = {
    "hostname": "cisco1",
    "model": 123,
    "uptime":"3 days"
}

model_num = 456
if model_num not in device_info:
    print("Access denied")
else:
    print("Access granted")

