import socket
import json
import threading

# Файл із питаннями
QUESTIONS_FILE = "questions.json"

# Сервер
class QuizServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Сервер працює на {self.host}:{self.port}")
        self.load_questions()
    
    def load_questions(self):
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            self.questions = json.load(f)
    
    def handle_client(self, conn, addr):
        print(f"Підключився клієнт {addr}")
        score = 0
        conn.sendall(json.dumps(self.questions).encode())
        answers = json.loads(conn.recv(1024).decode())
        for i, question in enumerate(self.questions):
            correct_answers = set(question["correct"])
            if set(answers[i]) == correct_answers:
                score += 1
        conn.sendall(f"Ваш рахунок: {score}/{len(self.questions)}".encode())
        conn.close()
    
    def run(self):
        while True:
            conn, addr = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    server = QuizServer()
    server.run()
