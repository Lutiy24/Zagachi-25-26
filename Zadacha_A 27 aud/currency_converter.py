#!C:/install/python.exe
from wsgiref.simple_server import make_server
import cgi
import pandas as pd

def load_rates():
    df = pd.read_excel("currency_rates.xlsx")
    rates = {(row["Currency1"], row["Currency2"]): row["Rate"] for _, row in df.iterrows()}
    return rates

def application(environ, start_response):
    rates = load_rates()
    start_response("200 OK", [("Content-Type", "text/html")])
    form = cgi.FieldStorage(fp=environ["wsgi.input"], environ=environ)
    currency1 = form.getvalue("currency1", "")
    currency2 = form.getvalue("currency2", "")
    amount = form.getvalue("amount", "0")
    
    result = ""
    if currency1 and currency2 and amount:
        amount = float(amount)
        rate = rates.get((currency1, currency2))
        if rate:
            converted = amount * rate
            result = f"{amount} {currency1} = {converted:.2f} {currency2}"
        else:
            result = "Курс для вибраної пари не знайдено."
    
    return [f"""
    <html><body>
        <h2>Конвертер валют</h2>
        <form method='post'>
            Валюта 1: <input type='text' name='currency1'><br>
            Валюта 2: <input type='text' name='currency2'><br>
            Сума: <input type='text' name='amount'><br>
            <input type='submit' value='Конвертувати'>
        </form>
        <p><strong>Результат:</strong> {result}</p>
    </body></html>
    ".encode("utf-8")]

if __name__ == "__main__":
    with make_server("", 8000, application) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()

