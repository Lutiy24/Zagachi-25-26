import socket
import json

# Клієнт
class QuizClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
    
    def start_quiz(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_host, self.server_port))
            questions = json.loads(s.recv(4096).decode())
            answers = []
            for question in questions:
                print(question["question"])
                for idx, option in enumerate(question["options"], 1):
                    print(f"{idx}. {option}")
                user_answer = input("Введіть номери правильних відповідей через кому: ")
                answers.append([int(i) - 1 for i in user_answer.split(",")])
            s.sendall(json.dumps(answers).encode())
            print(s.recv(1024).decode())

if __name__ == "__main__":
    client = QuizClient("127.0.0.1", 5000)
    client.start_quiz()
