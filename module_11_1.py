import requests
import pandas as pd
import matplotlib.pyplot as plt


API_KEY = "176b7d3fca6b4d47a82123633242011"
base_url = "https://api.weatherapi.com/v1/current.json"
cities = ["London", "New York", "Tokyo", "Paris", "Moscow"]
weather_data = []
#используя данные  сверху мы получаем данные с сайта для нашего списка городов
for city in cities:
    params = {
        "key": API_KEY,
        "q": city,
        "aqi": "no"  # Отключение данных о качестве воздуха
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)  # Таймаут 10 секунд
        if response.status_code == 200:
            data = response.json()
            weather_data.append({
                "City": city,
                "Temperature": data["current"]["temp_c"],
                "Humidity": data["current"]["humidity"],
                "Wind Speed": data["current"]["wind_kph"]
            })
        else:
            print(f"Ошибка: {response.status_code} для города {city}")
    except requests.exceptions.ReadTimeout:
        print(f"Запрос к {city} превысил время ожидания")
    except Exception as e:
        print(f"Произошла ошибка при запросе к {city}: {e}")

# Преобразуем данные в DataFrame pandas
df = pd.DataFrame(weather_data)

# Если DataFrame пустой, предупреждаем пользователя
if df.empty:
    print("Не удалось получить данные о погоде. Проверьте подключение или настройки API.")
else:
    # Сохраняем данные в CSV
    df.to_csv("weather_data_weatherapi.csv", index=False)
    print("Данные о погоде сохранены в файл weather_data_weatherapi.csv")

    # Построение графика температуры при помощи matplotlib
    plt.figure(figsize=(10, 6))
    plt.bar(df["City"], df["Temperature"], color="skyblue")
    plt.title("Температура в городах (WeatherAPI)", fontsize=16)
    plt.xlabel("Города", fontsize=12)
    plt.ylabel("Температура (°C)", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()
