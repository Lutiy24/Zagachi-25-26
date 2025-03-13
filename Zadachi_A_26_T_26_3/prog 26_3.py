import requests
import pandas as pd

# Функція для отримання прогнозу погоди з WeatherAPI
def get_weather(city_name, api_key):
    url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city_name}&days=5&aqi=no&alerts=no'
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Помилка отримання даних від WeatherAPI")
        return None
    
    data = response.json()
    if 'forecast' not in data:
        print("Невірна відповідь API")
        return None
    
    weather_data_list = []
    for day in data['forecast']['forecastday']:
        date = day['date']
        temp_max = day['day']['maxtemp_c']
        temp_min = day['day']['mintemp_c']
        
        weather_data_list.append([date, temp_max, temp_min])
    
    return weather_data_list

# Збереження в Excel
def save_to_excel(city_name, weather_data_list):
    df = pd.DataFrame(weather_data_list, columns=['Дата', 'Макс. температура', 'Мін. температура'])
    filename = f'weather_{city_name}.xlsx'
    df.to_excel(filename, index=False)
    print(f'✅ Дані збережено у {filename}')

# Введення міста та запуск
api_key = "c5f896b8a3624fc8a06105429250603"  # Вставте свій API ключ від WeatherAPI
city_input = input("Введіть назву міста (наприклад, 'Kyiv'): ")
weather_data_result = get_weather(city_input, api_key)
if weather_data_result:
    save_to_excel(city_input, weather_data_result)


