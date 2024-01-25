server_addr = find_server()
    
if server_addr:
    # Create a Bluetooth socket using RFCOMM protocol
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    try:
        # Attempt to connect to the server using its address
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
