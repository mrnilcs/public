import socket
import ssl
import bluetooth

# Create a Bluetooth socket using RFCOMM protocol
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

# Set up SSL context for the server
# This will require a certificate and a private key
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")

# Server main loop
while True:
    # Accept a new connection
    client_sock, client_info = server_sock.accept()
    
    # Wrap the client socket with SSL for secure communication
    secure_sock = context.wrap_socket(client_sock, server_side=True)

    try:
        # Communication loop
        while True:
            data = secure_sock.recv(1024)
            if not data:
                break
            print("Received [%s]" % data)
    except OSError:
        # Handle exceptions (e.g., client disconnects)
        pass

    # Close the secure socket after communication is complete
    secure_sock.shutdown(socket.SHUT_RDWR)
    secure_sock.close()

# Close the server socket
server_sock.close()

