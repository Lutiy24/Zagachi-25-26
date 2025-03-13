from wsgiref.simple_server import make_server
import cgi

def is_palindrome(s):
    return s == s[::-1]

def application(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/html")])
    form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
    text = form.getvalue("text", "")
    
    result = ""
    if text:
        result = f"Рядок '{text}' {'є паліндромом' if is_palindrome(text) else 'не є паліндромом'}."
    
    return [f"""
    <html><body>
        <h2>Перевірка паліндрому</h2>
        <form method='post'>
            Введіть рядок: <input type='text' name='text'><br>
            <input type='submit' value='Перевірити'>
        </form>
        <p><strong>Результат:</strong> {result}</p>
    </body></html>
    ".encode("utf-8")]

if __name__ == "__main__":
    with make_server("", 8000, application) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()
