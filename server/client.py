import socket
import ssl
import bluetooth

# Server Bluetooth address and RFCOMM port
server_addr = 'SERVER_BLUETOOTH_ADDRESS'  # Replace with the server's address
port = 1

# Create a Bluetooth socket and connect to the server
client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client_sock.connect((server_addr, port))

# Set up SSL context for the client
# The client has its own certificate and key, and also needs the server's certificate
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="server_cert.pem")
context.load_cert_chain(certfile="client_cert.pem", keyfile="client_key.pem")

# Wrap the socket with SSL for a secure connection
secure_sock = context.wrap_socket(client_sock, server_hostname=server_addr)

try:
    # Send data to the server
    secure_sock.send(b"Hello, secure world!")

    # Receive and print data from the server
    data = secure_sock.recv(1024)
    print("Received:", data)
except Exception as e:
    # Handle exceptions (e.g., connection errors)
    print(e)
finally:
    # Close the secure socket properly
    secure_sock.shutdown(socket.SHUT_RDWR)
    secure_sock.close()

# Close the Bluetooth socket
client_sock.close()

