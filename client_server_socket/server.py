import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

def load_key(file_path):
    with open(file_path, "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read())

def load_private_key(file_path):
    with open(file_path, "rb") as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=None)

server_socket = socket.socket()
server_port = 1672
server_ip = '0.0.0.0'
buffer_size = 1024

server_private_key = load_private_key("server_key")
client_public_key = load_key("client_key.pub")

print("[INFO] Starting the server...")
server_socket.bind((server_ip, server_port))
print("[INFO] Server started successfully on port:", server_port)

print("[INFO] Waiting for a connection...")
server_socket.listen(5)
connection, address = server_socket.accept()
print("[INFO] Connection established with:", address)

print("[INFO] Receiving encrypted message from client...")
encrypted_message = connection.recv(buffer_size)
decrypted_message = server_private_key.decrypt(
    encrypted_message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print("Decrypted Message from Client:", decrypted_message.decode('utf-8'))

response_message = decrypted_message.decode('utf-8').upper()
encrypted_response = client_public_key.encrypt(
    response_message.encode('utf-8'),
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print("[INFO] Sending encrypted response to client...")
connection.send(encrypted_response)
print("[INFO] Encrypted response sent successfully.")

print("[INFO] Closing client connection...")
connection.close()
print("[INFO] Client connection closed.")

print("[INFO] Shutting down the server...")
server_socket.close()
print("[INFO] Server shut down successfully.")
