#!C:/install/python.exe

import cgi

def is_palindrome(s):
    return s == s[::-1]

print("Content-Type: text/html\n")
form = cgi.FieldStorage()
input_text = form.getvalue("text", "")

html = """
<html>
<head><title>Перевірка паліндрома</title></head>
<body>
    <form method="post" action="">
        Введіть рядок: <input type="text" name="text">
        <input type="submit" value="Перевірити">
    </form>
"""

if input_text:
    result = "це паліндром" if is_palindrome(input_text) else "це не паліндром"
    html += f"<p>Результат: <b>{input_text}</b> - {result}</p>"

html += "</body></html>"
print(html)

