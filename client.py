import socket
import des
import sys
from time import sleep

def main():
    host = "127.0.0.1"
    port = 5002
    sock = socket.socket()
    sock.connect((host, port))

    while True:
        message = input("Enter the message to encrypt (or 'q' to quit): ")
        if message == 'q':
            break

        key = "0A1B2C3D4E5F6071"
        encrypted_message = des.bin2hex(des.encrypt(message, key))
        print(f"Encrypted message: {encrypted_message}")

        des.sending()
        sock.send(encrypted_message.encode())

        data = sock.recv(1024).decode()
        decrypted_message = des.decrypt(data, key)
        print(f"Decrypted message: {des.bin2text(decrypted_message)}")

    sock.close()

if __name__ == '__main__':
    main()