import os
import re
import requests
from html.parser import HTMLParser
from urllib.parse import urljoin

BASE_URL = "http://matfiz.univ.kiev.ua"
TOPICS_PAGE = "http://matfiz.univ.kiev.ua/pages/13"
DOWNLOAD_DIR = "matfiz_examples"

# Створюємо директорію для збереження файлів
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Функція для отримання HTML-коду сторінки
def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return ""

# 1. Використання регулярних виразів для отримання списку тем
def get_topic_urls():
    html = fetch_html(TOPICS_PAGE)
    topic_links = re.findall(r'href="([^"]+/pages/(\d+))"\s*>Тема\s*(\d+)', html)
    return {int(num): urljoin(BASE_URL, path) for path, num, _ in topic_links}

# 2. Використання HTMLParser для отримання списку файлів із теми
class ExampleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.files = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs_dict = dict(attrs)
            if "href" in attrs_dict and attrs_dict["href"].startswith("/userfiles/files/"):
                self.files.append(urljoin(BASE_URL, attrs_dict["href"]))

# Функція для отримання посилань на приклади з вибраної теми
def get_example_files(topic_url):
    html = fetch_html(topic_url)
    parser = ExampleParser()
    parser.feed(html)
    return [file for file in parser.files if file.endswith(('.py', '.pyw'))]

# Функція для завантаження файлу
def download_file(url, save_dir):
    filename = os.path.join(save_dir, os.path.basename(url))
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {url}")

# Основна функція
def main():
    topic_urls = get_topic_urls()
    print("Доступні теми:")
    for num in sorted(topic_urls.keys()):
        print(f"Тема {num}: {topic_urls[num]}")
    
    topic_num = int(input("Введіть номер теми: "))
    if topic_num not in topic_urls:
        print("Невірний номер теми.")
        return
    
    topic_url = topic_urls[topic_num]
    example_files = get_example_files(topic_url)
    
    if not example_files:
        print("Немає доступних прикладів.")
        return
    
    print(f"Знайдено {len(example_files)} прикладів. Завантаження...")
    for file_url in example_files:
        download_file(file_url, DOWNLOAD_DIR)

if __name__ == "__main__":
    main()