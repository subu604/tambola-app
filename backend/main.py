from fastapi import FastAPI, WebSocket
from game import Game

app = FastAPI()
game = Game()
connections = []

async def broadcast(message):
    for conn in connections:
        await conn.send_json(message)

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    connections.append(ws)

    try:
        while True:
            data = await ws.receive_json()

            if data["action"] == "join":
                game.add_player(data["name"])
                await broadcast({"type": "players", "players": game.players})

            elif data["action"] == "host":
                game.set_host(data["name"])
                await broadcast({"type": "host", "host": game.host})

            elif data["action"] == "start":
                if data["name"] == game.host:
                    await game.start_game(broadcast)

    except:
        connections.remove(ws)
