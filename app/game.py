import random
from datetime import datetime

class GameManager:
    def __init__(self):
        self.players = []
        self.tickets = {}
        self.numbers = list(range(1, 91))
        self.drawn = []
        self.winners = []

    def add_player(self, name):
        self.players.append({
            "name": name,
            "joined_at": str(datetime.now())
        })

    def start_game(self):
        random.shuffle(self.numbers)
        self.tickets = {
            p["name"]: self.generate_ticket()
            for p in self.players
        }

    def generate_ticket(self):
        return sorted(random.sample(range(1, 91), 15))

    def draw_number(self):
        if not self.numbers:
            return None
        num = self.numbers.pop()
        self.drawn.append(num)
        return num

    def check_winners(self):
        winners = []

        for name, ticket in self.tickets.items():
            matched = set(ticket) & set(self.drawn)

            if len(matched) == 5 and "Top" not in self.winners:
                self.winners.append("Top")
                winners.append({"type": "Top Line", "name": name})

            elif len(matched) == 10 and "Middle" not in self.winners:
                self.winners.append("Middle")
                winners.append({"type": "Middle Line", "name": name})

            elif len(matched) == 15 and "Full" not in self.winners:
                self.winners.append("Full")
                winners.append({"type": "Full House", "name": name})

        return winners
