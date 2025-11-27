from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

# room -> {"teacher": ws, "student": ws}
rooms = {}


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket, room: str, role: str):
    await ws.accept()

    if room not in rooms:
        rooms[room] = {}

    rooms[room][role] = ws
    other = "teacher" if role == "student" else "student"

    try:
        while True:
            data = await ws.receive_text()
            # просто пересылаем строку второму участнику
            if other in rooms[room]:
                await rooms[room][other].send_text(data)
    except WebSocketDisconnect:
        # при дисконнекте просто молча выходим
        pass
