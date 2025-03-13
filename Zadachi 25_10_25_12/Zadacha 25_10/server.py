import socket
import os
import threading
import json

BACKUP_DIR = "backup_storage"
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

class BackupServer:
    def __init__(self, host='0.0.0.0', port=5001):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Сервер працює на {self.host}:{self.port}")
    
    def handle_client(self, conn, addr):
        print(f"Підключився клієнт {addr}")
        data = json.loads(conn.recv(4096).decode())
        for file_info in data:
            file_path = os.path.join(BACKUP_DIR, file_info["path"])
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(bytes(file_info["content"]))
        print("Файли успішно збережені!")
        conn.sendall(b"exit")
        conn.close()
    
    def run(self):
        while True:
            conn, addr = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    server = BackupServer()
    server.run()
