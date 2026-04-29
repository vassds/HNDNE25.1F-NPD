# Step 1: Create data (list of dictionaries)
devices = [
    {"name": "Router1", "ip": "192.168.1.1", "status": "active"},
    {"name": "Switch1", "ip": "192.168.1.2", "status": "down"},
    {"name": "Firewall1", "ip": "192.168.1.3", "status": "active"}
]

# Step 2 & 3: Loop + logic
for device in devices:
    if device["status"] == "active":
        print(f"Connecting to {device['name']} at {device['ip']}...")
    else:
        print(f"Cannot connect, {device['name']} is down.")