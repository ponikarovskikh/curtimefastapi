from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from datetime import datetime
import pytz
import asyncio

app = FastAPI()

# Функция для получения текущего времени в городах
def get_current_times():
    cities = {
        "Moscow": "Europe/Moscow",
        "New York": "America/New_York",
        "Paris": "Europe/Paris",
        "Seoul": "Asia/Seoul"
    }
    time_info = {}
    for city, timezone in cities.items():
        tz = pytz.timezone(timezone)
        time_info[city] = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    return time_info

# Отдача HTML-страницы
@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html", "r", encoding="utf-8") as file:
        return file.read()

# WebSocket для обновления времени
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            time_data = get_current_times()
            await websocket.send_json(time_data)
            await asyncio.sleep(1)  # Обновляем каждую секунду
    except Exception as e:
        print(f"WebSocket connection closed: {e}")
