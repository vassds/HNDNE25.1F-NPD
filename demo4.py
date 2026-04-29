port_num = input("Enter the port number: ")

if port_num.isdigit():
    port_num = int(port_num)   # convert to integer
    
    if port_num == 80:
        print("HTTP")
    elif port_num == 443:
        print("HTTPS")
    else:
        print("Unknown port")
else:
    print("Invalid input (not an integer)")

    