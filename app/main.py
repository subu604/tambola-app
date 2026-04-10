
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import json, asyncio, random
from datetime import datetime

app = FastAPI()

players = {}
connections = {}
numbers = list(range(1,91))
drawn = []
tickets = {}
winners = {"top": None, "middle": None, "bottom": None, "full": None}
host = None

@app.get("/")
def home():
    return HTMLResponse(open("app/templates/index.html").read())

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    name = None
    try:
        while True:
            data = json.loads(await websocket.receive_text())

            if data["type"] == "join":
                name = data["name"]
                players[name] = str(datetime.now())
                connections[name] = websocket
                await broadcast({"type":"players","players":list(players.keys()),"count":len(players),"host":host})

            if data["type"] == "start":
                global host
                if not host:
                    host = data["name"]
                if data["name"] != host:
                    continue
                await broadcast({"type":"host","host":host})
                await broadcast({"type":"countdown"})
                await asyncio.sleep(3)
                generate_tickets()
                await broadcast({"type":"tickets","tickets":tickets})
                asyncio.create_task(auto_draw())

    except:
        if name and name in connections:
            del connections[name]
            if name in players:
                del players[name]

async def auto_draw():
    global numbers
    random.shuffle(numbers)
    while numbers:
        num = numbers.pop()
        drawn.append(num)
        win = check_winners()
        await broadcast({"type":"number","number":num,"winners":win})
        await asyncio.sleep(3)

def generate_tickets():
    global tickets
    tickets = {name: sorted(random.sample(range(1,91),15)) for name in players}

def check_winners():
    results = []
    for name, ticket in tickets.items():
        match = set(ticket) & set(drawn)

        if len(match)>=5 and not winners["top"]:
            winners["top"]=name
            results.append(f"Top Line: {name}")
        if len(match)>=10 and not winners["middle"]:
            winners["middle"]=name
            results.append(f"Middle Line: {name}")
        if len(match)>=12 and not winners["bottom"]:
            winners["bottom"]=name
            results.append(f"Bottom Line: {name}")
        if len(match)==15 and not winners["full"]:
            winners["full"]=name
            results.append(f"Full House: {name}")
    return results

async def broadcast(msg):
    for c in connections.values():
        await c.send_text(json.dumps(msg))
