import bluetooth

def main():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    port = bluetooth.PORT_ANY
    server_sock.bind(("", port))
    server_sock.listen(1)

    bluetooth.advertise_service(server_sock, "SampleServer",
                                service_id=bluetooth.SERIAL_PORT_CLASS,
                                service_classes=[bluetooth.SERIAL_PORT_CLASS],
                                profiles=[bluetooth.SERIAL_PORT_PROFILE])

    print("Waiting for a connection on RFCOMM channel %d" % port)

    while True:  # Loop to allow for multiple connections
        client_sock, client_info = server_sock.accept()
        print("Accepted connection from ", client_info)

        try:
            while True:  # Loop to keep the connection open
                data = client_sock.recv(1024)
                if not data:
                    break
                print("Received [%s]" % data)
        except OSError:
            pass

        print("Disconnected from", client_info)

        client_sock.close()
        print("Waiting for a new connection...")

    server_sock.close()

if __name__ == "__main__":
    main()