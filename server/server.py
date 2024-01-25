import socket
import ssl
import bluetooth
import subprocess

def get_bluetooth_mac_address():
    # Retrieve and return the MAC address of the Bluetooth adapter
    try:
        output = subprocess.check_output("hcitool dev", shell=True).decode('utf-8')
        return output.split('\n')[1].split('\t')[2]
    except:
        return "MAC Address Not Found"

# Get and display the server's Bluetooth MAC address
mac_address = get_bluetooth_mac_address()
print("Server's Bluetooth MAC Address:", mac_address)

# Create a Bluetooth socket using RFCOMM protocol
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)
print("Bluetooth RFCOMM server socket created and listening")

# Set up SSL context for the server
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")
print("SSL context set up with server certificate and key")

# Server main loop
while True:
    print("Waiting for a client to connect...")
    client_sock, client_info = server_sock.accept()
    print(f"Accepted connection from {client_info}")

    # Wrap the client socket with SSL for secure communication
    secure_sock = context.wrap_socket(client_sock, server_side=True)
    print("Secure SSL socket established")

    try:
        # Communication loop
        while True:
            data = secure_sock.recv(1024)
            if not data:
                break
            print(f"Received data: {data}")
    except OSError as e:
        # Handle exceptions (e.g., client disconnects)
        print(f"Error: {e}")

    # Close the secure socket after communication is complete
    print("Client disconnected. Shutting down secure socket.")
    secure_sock.shutdown(socket.SHUT_RDWR)
    secure_sock.close()

# Close the server socket
print("Shutting down server socket.")
server_sock.close()
