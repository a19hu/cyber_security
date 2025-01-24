import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

def load_key(file_path):
    with open(file_path, "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read())

def load_private_key(file_path):
    with open(file_path, "rb") as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=None)

client_socket = socket.socket()
server_port = 1672
server_ip = '127.0.0.1'
buffer_size = 1024

server_public_key = load_key("server_key.pub")
client_private_key = load_private_key("client_key")

print("[INFO] Connecting to the server...")
client_socket.connect((server_ip, server_port))
print("[INFO] Connected to server:", server_ip, "on port:", server_port)

message = input("Enter a message to send to the server: ")
encrypted_message = server_public_key.encrypt(
    message.encode('utf-8'),
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print("[INFO] Sending encrypted message to server...")
client_socket.send(encrypted_message)
print("[INFO] Encrypted message sent successfully.")

print("[INFO] Waiting for response from server...")
encrypted_response = client_socket.recv(buffer_size)
decrypted_response = client_private_key.decrypt(
    encrypted_response,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print("Decrypted Response from Server:", decrypted_response.decode('utf-8'))

print("[INFO] Closing connection to the server...")
client_socket.close()
print("[INFO] Connection closed successfully.")
