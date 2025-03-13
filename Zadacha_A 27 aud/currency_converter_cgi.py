#! /usr/bin/env python3

import cgi
import pandas as pd

# Завантаження курсів валют з файлу
file_path = "currency_rates.xlsx"
df = pd.read_excel(file_path)
rates = {(row["Currency1"], row["Currency2"]): row["Rate"] for _, row in df.iterrows()}

def convert_currency(amount, from_currency, to_currency):
    rate = rates.get((from_currency, to_currency))
    if rate:
        return amount * rate
    return None

# Отримання даних з форми
form = cgi.FieldStorage()
currency1 = form.getvalue("currency1", "UAH")
currency2 = form.getvalue("currency2", "USD")
amount = form.getvalue("amount", "1000")

try:
    amount = float(amount)
    converted = convert_currency(amount, currency1, currency2)
    result = f"{amount} {currency1} = {converted:.2f} {currency2}" if converted else "Курс для вибраної пари не знайдено."
except ValueError:
    result = "Некоректна сума."

# Вивід HTML-сторінки з результатами
print("Content-type: text/html\n")
print("<html><body>")
print("<h2>Конвертер валют</h2>")
print("<form method='post'>")
print("Валюта 1: <input type='text' name='currency1' value='UAH'><br>")
print("Валюта 2: <input type='text' name='currency2' value='USD'><br>")
print("Сума: <input type='text' name='amount' value='1000'><br>")
print("<input type='submit' value='Конвертувати'>")
print("</form>")
print(f"<p><strong>Результат:</strong> {result}</p>")
print("</body></html>")
