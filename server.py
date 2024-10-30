import socket
import des

def main():
    host = "127.0.0.1"
    port = 5002
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(2)
    conn, addr = sock.accept()
    print(f"Connected to port: {addr}")

    while True:
        data = conn.recv(1024).decode()
        print(f"Received data from client: {data}")

        key = "0A1B2C3D4E5F6071"
        decrypted_message = des.decrypt(data, key)
        print(f"Decrypted message: {des.bin2text(decrypted_message)}")

        message = input("Enter the message to encrypt: ")
        encrypted_message = des.bin2hex(des.encrypt(message, key))
        print(f"Encrypted message: {encrypted_message}")

        des.sending()
        conn.send(encrypted_message.encode())

    conn.close()

if __name__ == '__main__':
    main()