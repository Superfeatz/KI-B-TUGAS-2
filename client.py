import socket
import sys
from DES import *  # Import all functions from DES module

class DESClient:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = None
        self.key = None
        
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
        except Exception as e:
            print(f"Connection error: {e}")
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
        
    def send_message(self, message):
        if not self.key:
            print("Please set encryption key first!")
            return
            
        try:
            # Encrypt the message
            encrypted = self.encrypt_message(message)
            # Send the encrypted message
            self.socket.send(encrypted.encode())
        except Exception as e:
            print(f"Error sending message: {e}")
            
    def receive_message(self):
        try:
            # Receive encrypted message with larger buffer
            encrypted_msg = self.socket.recv(4096).decode()
            if not encrypted_msg:
                return None
                
            # Decrypt the message
            decrypted = self.decrypt_message(encrypted_msg)
            return decrypted
        except Exception as e:
            print(f"Error receiving message: {e}")
            return None
            
    def close(self):
        if self.socket:
            self.socket.close()

def main():
    client = DESClient()
    client.connect()
    

    # if used fix key
    key = "ADHD1234"
    # Set encryption key if manually
    # key = input("Enter encryption key (8 characters): ")
    # while len(key) != 8:
    #     print("Key must be exactly 8 characters!")
    #     key = input("Enter encryption key (8 characters): ")
    client.set_key(key)
    
    try:
        while True:
            message = input("Enter message (or 'quit' to exit): ")
            if message.lower() == 'quit':
                break
                
            # Send message
            client.send_message(message)
            print("Message sent (encrypted)")
            
            # Receive response
            response = client.receive_message()
            if response:
                print(f"Received (decrypted): {response}")
            else:
                print("No response received or decryption failed")
            
    except KeyboardInterrupt:
        print("\nClosing connection...")
    finally:
        client.close()

if __name__ == "__main__":
    main()
