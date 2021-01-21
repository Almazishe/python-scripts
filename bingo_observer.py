import random



class BingoGame:

    _players = []
    _current_game = []

    def attach(self, player):
        if len(self._players) == 5:
            print("Too many players, sorry =(")

        self._players.append(player)
        print(f"{player.name} joined the game.")


    def detach(self, player):

        self._players.remove(player)
        print(f"{player.name} left the game.")


    def check_players(self, num):

        for player in self._players:
            won = player.check(num)
            if won:
                return player
        return None


    def _generate_num(self):

        n = random.choice([i for i in range(1,100) if i not in self._current_game])
        self._current_game.append(n)
        print(f"We got number: {n}")
        return n


    def start(self):
        print("Welcome to the bingo game")
        for i in range(99):
            n = self._generate_num()
            player = self.check_players(n)
            if player:
                print(f'{player.name} BINGO!!!'.upper())
                return

class Player:

    _bilet = []
    _current_game = []

    def __init__(self, name):
        self.name = name
        self._generate_bilet()

    def _generate_bilet(self):
        for i in range(5):
            n = random.randint(1, 99)
            if not n in self._bilet:
                self._bilet.append(n)
            else:
                i -= 1

    def check(self, num):
        if num in self._bilet:
            self._current_game.append(num)

        if len(self._bilet) == len(self._current_game):
            return True
        return False

if __name__ == '__main__':

    game = BingoGame()

    p1 = Player('Almaz')
    game.attach(p1)

    p2 = Player('Miraz')
    game.attach(p2)

    p3 = Player('Akbota')
    game.attach(p3)

    p4 = Player('Nurtas')
    game.attach(p4)

    p5 = Player('Yelaman')
    game.attach(p5)

    game.start()