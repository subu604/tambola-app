import random
import asyncio

class Game:
    def __init__(self):
        self.players = []
        self.host = None
        self.started = False
        self.numbers = list(range(1, 91))
        random.shuffle(self.numbers)
        self.called_numbers = []

    def add_player(self, name):
        if len(self.players) < 5 and name not in self.players:
            self.players.append(name)

    def set_host(self, name):
        if name == "SUBU":
            self.host = name

    async def start_game(self, broadcast):
        self.started = True

        for i in range(5, 0, -1):
            await broadcast({"type": "countdown", "value": i})
            await asyncio.sleep(1)

        for num in self.numbers:
            await broadcast({"type": "number", "value": num})
            await asyncio.sleep(2)
