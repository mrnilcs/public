import bluetooth
import uuid

def main():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    # Bind to any available port
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)

    # Get the port the server socket is listening
    port = server_sock.getsockname()[1]

    # Generate a new UUID or use a predefined one
    service_uuid = str(uuid.uuid4())

    # Advertise the service
    bluetooth.advertise_service(server_sock, "PyBluezServer", service_id=service_uuid,
                                service_classes=[service_uuid, bluetooth.SERIAL_PORT_CLASS],
                                profiles=[bluetooth.SERIAL_PORT_PROFILE])

    print(f"Waiting for connection on RFCOMM channel {port}")

    # Accept incoming connections
    client_sock, client_info = server_sock.accept()
    print(f"Accepted connection from {client_info}")

    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode('utf-8')}")
    except OSError:
        pass

    print("Disconnected.")

    # Close sockets
    client_sock.close()
    server_sock.close()
    print("Server down.")

if __name__ == '__main__':
    main()
