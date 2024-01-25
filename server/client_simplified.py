import bluetooth

def find_server():
    """ Scan for the Bluetooth server and return its address """
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True)
    print("Found {} devices.".format(len(nearby_devices)))

    for addr, name in nearby_devices:
        print("  {} - {}".format(addr, name))
        # If the device name matches your server's name, you can connect using its address
        # if name == 'My_Bluetooth_Server':  # Replace with the name of your server
        #     return addr

    # If no specific server is found, return the address of the first device
    return nearby_devices[0][0] if nearby_devices else None

def main():
    server_addr = find_server()
    
    if server_addr:
        # Create a Bluetooth socket using RFCOMM protocol
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        try:
            # Attempt to connect to the server
            sock.connect((server_addr, 1))  # Port number 1 should match your server's
            print("Connected to the server.")

            # Send data
            sock.send("Hello from Client!")

            # Optionally, receive data back
            # data = sock.recv(1024)
            # print(f"Received: {data}")

        except bluetooth.btcommon.BluetoothError as err:
            print(f"Bluetooth connection failed: {err}")
        finally:
            sock.close()
    else:
        print("Could not find the server.")

if __name__ == '__main__':
    main()
