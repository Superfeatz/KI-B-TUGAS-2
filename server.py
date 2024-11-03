import socket
import sys
from DES import *  # Import all functions from DES module

class DESServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = None
        self.client_socket = None
        self.client_address = None
        self.key = None
        
    def start(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Add socket reuse option
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            print(f"Server listening on {self.host}:{self.port}")
        except Exception as e:
            print(f"Server startup error: {e}")
            sys.exit(1)
            
    def accept_connection(self):
        try:
            self.client_socket, self.client_address = self.socket.accept()
            print(f"Connection accepted from {self.client_address}")
        except Exception as e:
            print(f"Connection acceptance error: {e}")
            sys.exit(1)
            
    def set_key(self, key):
        self.key = key
        # Initialize DES keys using the global keys list from DES.py
        global keys
        keys = [''] * 16
        generate_keys(key)
            
    def encrypt_message(self, message):
        # Pad message if needed
        while len(message) % 8 != 0:
            message += ' '
            
        encrypted_result = ''
        for i in range(0, len(message), 8):
            block = message[i:i+8]
            encrypted_result += des_encrypt_block(block)
            
        return bin_to_hex(encrypted_result)
        
    def decrypt_message(self, ciphertext_hex):
        try:
            ciphertext_bin = hex_to_bin(ciphertext_hex)
            decrypted_result = ''
            
            for i in range(0, len(ciphertext_bin), 64):
                block = ciphertext_bin[i:i+64]
                decrypted_result += des_decrypt(block)
                
            return decrypted_result.strip()
        except Exception as e:
            print(f"Decryption error: {e}")
            return None
        
    def receive_message(self):
        try:
            # Receive encrypted message with larger buffer
            encrypted_msg = self.client_socket.recv(4096).decode()
            if not encrypted_msg:
                return None
                
            # Decrypt the message
            decrypted = self.decrypt_message(encrypted_msg)
            return decrypted
        except Exception as e:
            print(f"Error receiving message: {e}")
            return None
            
    def send_message(self, message):
        if not self.key:
            print("Please set encryption key first!")
            return
            
        try:
            # Encrypt the message
            encrypted = self.encrypt_message(message)
            # Send the encrypted message
            self.client_socket.send(encrypted.encode())
        except Exception as e:
            print(f"Error sending message: {e}")
            
    def close(self):
        if self.client_socket:
            self.client_socket.close()
        if self.socket:
            self.socket.close()

def main():
    server = DESServer()
    server.start()
    
    # if used fix key
    key = "ADHD1234"
    # Set encryption key if manually
    # key = input("Enter encryption key (8 characters): ")
    # while len(key) != 8:
    #     print("Key must be exactly 8 characters!")
    #     key = input("Enter encryption key (8 characters): ")
    server.set_key(key)
    
    # Accept client connection
    server.accept_connection()
    
    try:
        while True:
            # Receive message
            message = server.receive_message()
            if not message:
                print("Client disconnected")
                break
                
            print(f"Received (decrypted): {message}")
            
            # Send response
            response = input("Enter response: ")
            server.send_message(response)
            print("Response sent (encrypted)")
            
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server.close()

if __name__ == "__main__":
    main()
