from dotenv import load_dotenv, find_dotenv
import requests
import json
import os

# Настройки Mistral API
load_dotenv(find_dotenv())  # загрузка переменных окружения из файла .env
API_KEY = os.environ['API_KEY']  # имя бота в discord
API_URL = "https://api.mistral.ai/v1/chat/completions"  # Исправленный endpoint
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Путь к входному и выходному файлам
# Путь к входному и выходному файлам
INPUT_FILE = "C:\\AudioRecordings\\23_02_25___16_31\\23_02_25___16_34___id1.txt"  # Файл с запросом
OUTPUT_FILE = "C:\\AudioRecordings\\23_02_25___16_31\\output.txt"  # Файл для ответа

# Чтение текста из входного файла
try:
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        prompt = file.read().strip()
    if not prompt:
        raise ValueError("Файл пустой!")
except FileNotFoundError:
    print(f"Ошибка: Файл '{INPUT_FILE}' не найден.")
    exit()

# Формирование запроса к Mistral API с использованием "messages"
payload = {
    "model": "mistral-large-latest",
    "messages": [
        {
            "role": "user",
            "content": f"Ответь на русском языке: {prompt}"
        }
    ],
    "max_tokens": 1000,
    "temperature": 0.7
}

# Отправка запроса
response = requests.post(API_URL, headers=HEADERS, json=payload)

# Обработка ответа
if response.status_code == 200:
    # Получаем текст ответа из структуры "choices"
    result = response.json()["choices"][0]["message"]["content"].strip()

    # Записываем ответ в файл
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(result)
    print(f"Ответ успешно сохранён в '{OUTPUT_FILE}'!")
    print("Текст ответа:")
    print(result)
else:
    print(f"Ошибка API: {response.status_code} - {response.text}")