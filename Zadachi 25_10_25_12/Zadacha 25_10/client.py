import socket
import os
import json

class BackupClient:
    def __init__(self, server_host, server_port, directories):
        self.server_host = server_host
        self.server_port = server_port
        self.directories = directories
    
    def collect_files(self):
        files_data = []
        for directory in self.directories:
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, "rb") as f:
                        content = f.read()
                    relative_path = os.path.relpath(file_path, directory)
                    files_data.append({"path": relative_path, "content": list(content)})
        return files_data
    
    def send_backup(self):
        files_data = self.collect_files()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_host, self.server_port))
            s.sendall(json.dumps(files_data).encode())
            response = s.recv(1024).decode()
            print(response)

if __name__ == "__main__":
    client = BackupClient("127.0.0.1", 5001, ["test_data"])
    client.send_backup()
