import socket
import argparse
import ipaddress
import concurrent.futures
import time
import json
import sys

def parse_ports(port_string):
    """
    Parses a port string (e.g., '80,443' or '20-100') into a list of integers.
    """
    ports = set()
    try:
        parts = port_string.split(',')
        for part in parts:
            if '-' in part:
                start, end = map(int, part.split('-'))
                ports.update(range(start, end + 1))
            else:
                ports.add(int(part))
        return sorted(list(ports))
    except ValueError:
        print("[-] Error: Invalid port format. Use '80,443' or '20-100'.")
        sys.exit(1)

def grab_banner(sock):
    """
    Attempts to grab the service banner from an open port.
    """
    try:
        # Lower timeout for banner grabbing to maintain high performance
        sock.settimeout(0.5) 
        # Send a generic payload in case the server waits for client input (like HTTP)
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        # Clean up the banner for display by replacing newlines
        return banner.replace('\r', '').replace('\n', ' ')[:50] 
    except (socket.timeout, ConnectionResetError, OSError):
        return ""

def scan_port(ip, port):
    """
    Attempts a TCP connection to a specific IP and port.
    Returns a tuple: (port, is_open, banner)
    """
    try:
        # Create a TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1.0) # 1 second timeout to prevent hanging on filtered ports
            # connect_ex returns 0 if successful, error code otherwise
            result = sock.connect_ex((str(ip), port))
            
            if result == 0:
                banner = grab_banner(sock)
                return port, True, banner
            return port, False, None
    except Exception as e:
        return port, False, None

def scan_target(ip, ports, num_threads):
    """
    Scans a list of ports for a single IP address using ThreadPoolExecutor.
    """
    open_ports = []
    print(f"\n[*] Scanning Target: {ip}")
    print("-" * 50)
    
    # Using ThreadPoolExecutor for concurrency
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit all port scanning tasks to the thread pool
        futures = {executor.submit(scan_port, ip, port): port for port in ports}
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(futures):
            port, is_open, banner = future.result()
            if is_open:
                open_ports.append({
                    "port": port,
                    "banner": banner
                })
                banner_display = f" [Banner: {banner}]" if banner else ""
                print(f"[+] Port {port}/TCP is OPEN{banner_display}")
                
    if not open_ports:
        print("[-] No open ports found on this host.")
        
    return open_ports

def main():
    # 1. Setup CLI Argument Parsing
    parser = argparse.ArgumentParser(description="High-Performance Multi-threaded Network Scanner")
    # Notice: required=True has been removed from the target argument so we can prompt for it
    parser.add_argument("-t", "--target", help="Target IP or CIDR Subnet (e.g., 192.168.1.0/24)")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range to scan (default: 1-1024, format: 20-100 or 80,443)")
    parser.add_argument("-T", "--threads", type=int, default=50, help="Number of concurrent threads (default: 50)")
    parser.add_argument("-o", "--output", help="Output file to save results in JSON format")
    
    args = parser.parse_args()

    # Print the banner first so it looks professional before the prompt
    print(r"""
     _   _      _   ____                                
    | \ | | ___| |_/ ___|  ___ __ _ _ __  _ __   ___ _ __ 
    |  \| |/ _ \ __\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
    | |\  |  __/ |_ ___) | (_| (_| | | | | | | |  __/ |   
    |_| \_|\___|\__|____/ \___\__,_|_| |_|_| |_|\___|_|   
    """)
    
    # 2. Interactive Prompt Logic
    # If the user didn't use the -t flag, ask them for the target interactively
    if not args.target:
        try:
            args.target = input("[?] Enter Target IP or CIDR Subnet (e.g., 192.168.1.0/24): ").strip()
            if not args.target:
                print("[-] Error: Target cannot be empty. Exiting.")
                sys.exit(1)
        except KeyboardInterrupt:
            print("\n[-] Scan cancelled by user. Exiting gracefully...")
            sys.exit(0)

    print("[*] Initializing Network Scanner...")
    
    # 3. Parse Inputs
    ports = parse_ports(args.ports)
    print(f"[*] Target(s): {args.target}")
    print(f"[*] Ports to scan: {len(ports)} (Threads: {args.threads})")
    
    try:
        # ipaddress module seamlessly handles both single IPs and CIDR blocks
        network = ipaddress.ip_network(args.target, strict=False)
        hosts = list(network.hosts())
        # If /32 or single IP provided, it acts as a single host
        if not hosts: 
            hosts = [ipaddress.ip_address(args.target)]
    except ValueError as e:
        print(f"[-] Invalid target network: {e}")
        sys.exit(1)

    scan_results = {}
    start_time = time.time()

    # 4. Execute Scan
    try:
        for host in hosts:
            open_ports = scan_target(host, ports, args.threads)
            if open_ports:
                scan_results[str(host)] = open_ports
                
    except KeyboardInterrupt:
        print("\n[-] Scan interrupted by user. Exiting gracefully...")
        sys.exit(0)

    # 5. Finalize & Output Results
    end_time = time.time()
    print("\n" + "=" * 50)
    print(f"[*] Scan completed in {round(end_time - start_time, 2)} seconds.")
    print(f"[*] Total active hosts with open ports: {len(scan_results)}")
    print("=" * 50)

    if args.output:
        try:
            with open(args.output, 'w') as f:
                json.dump(scan_results, f, indent=4)
            print(f"[+] Results successfully saved to {args.output}")
        except IOError as e:
            print(f"[-] Failed to save output file: {e}")

if __name__ == "__main__":
    main()
