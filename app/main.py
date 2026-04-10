from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from app.game import GameManager
import json

app = FastAPI()
game = GameManager()

connections = []

@app.get("/")
def get():
    with open("app/templates/index.html") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)

            if data["type"] == "join":
                game.add_player(data["name"])
                await broadcast({"type": "players", "players": game.players})

            elif data["type"] == "start":
                game.start_game()
                await broadcast({"type": "tickets", "tickets": game.tickets})

            elif data["type"] == "next_number":
                number = game.draw_number()
                winners = game.check_winners()
                await broadcast({
                    "type": "update",
                    "number": number,
                    "winners": winners
                })

    except WebSocketDisconnect:
        connections.remove(websocket)


async def broadcast(message):
    for conn in connections:
        await conn.send_text(json.dumps(message))
