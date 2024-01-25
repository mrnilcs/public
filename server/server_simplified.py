import bluetooth

# Create a Bluetooth socket using RFCOMM protocol
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

print("Bluetooth server started, waiting for clients to connect.")

# Server main loop
while True:
    # Accept a new connection
    client_sock, client_info = server_sock.accept()
    print(f"Accepted connection from {client_info}")

    try:
        # Communication loop
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            print(f"Received [{data}]")
    except OSError:
        # Handle exceptions (e.g., client disconnects)
        print("An error occurred with the client connection.")
        pass

    # Close the client socket after communication is complete
    client_sock.close()

# Close the server socket
server_sock.close()