import socket
import ssl
import bluetooth
import subprocess

def get_bluetooth_mac_address():
    try:
        output = subprocess.check_output("hcitool dev", shell=True).decode('utf-8')
        return output.split('\n')[1].split('\t')[2]
    except:
        return "MAC Address Not Found"

mac_address = get_bluetooth_mac_address()
print("Server's Bluetooth MAC Address:", mac_address)

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)
print("Bluetooth RFCOMM server socket created and listening")

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")
print("SSL context set up with server certificate and key")

# Set a timeout for accept() method to handle unsuccessful attempts
server_sock.settimeout(10)  # Timeout of 10 seconds

while True:
    try:
        print("Waiting for a client to connect...")
        client_sock, client_info = server_sock.accept()
        print(f"Accepted connection from {client_info}")

        secure_sock = context.wrap_socket(client_sock, server_side=True)
        print("Secure SSL socket established with client")

        try:
            while True:
                data = secure_sock.recv(1024)
                if not data:
                    break
                print(f"Received data: {data}")
        except OSError as e:
            print(f"Error: {e}")

        print("Client disconnected. Shutting down secure socket.")
        secure_sock.shutdown(socket.SHUT_RDWR)
        secure_sock.close()

    except socket.timeout:
        # This block is executed if accept() times out waiting for a connection
        print("No connection attempts in the last 10 seconds.")

print("Shutting down server socket.")
server_sock.close()
