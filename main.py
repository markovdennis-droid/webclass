from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

# Папка с твоими HTML-файлами
app.mount("/", StaticFiles(directory=".", html=True), name="static")

rooms = {}  # Комнаты для WebRTC сигналинга


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, room: str, role: str):
    await websocket.accept()

    if room not in rooms:
        rooms[room] = {}

    rooms[room][role] = websocket

    other = "teacher" if role == "student" else "student"

    try:
        while True:
            data = await websocket.receive_text()

            if other in rooms[room]:
                await rooms[room][other].send_text(data)

    except WebSocketDisconnect:
        pass
