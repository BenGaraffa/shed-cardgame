from random import randrange, seed
from time import sleep


CARD_SUITS = ["♤", "♧", "♡", "♢"]
CARD_VALUES = [f"{i}" for i in range(2, 11)] \
            + ["J", "Q", "K", "A"]
RANDOM_SEED = 0 # Set to None for complete randomness


class Shed:
    def __init__(self, players=2):
        if players < 2: raise InvalidPlayerCount(players)

        self.playerCount = players
        self.players = [Player(i) for i in range(self.playerCount)]
        self.__deck = Deck()
        self.heap = []
        self.minHandSize = 3
        self.turn = 0
        self.running = True
        print(sum([card.magic for card in self.__deck]))

    def dealAllHands(self):
        for location in ["faceDown", "faceUp", "hand"]:
            for card in range(self.minHandSize):
                for i in range(self.playerCount):
                    getattr(self.players[i], location).append(self.__deck.pop())

    def play(self):
        self.dealAllHands()
        self.print()

        # Take turns swapping hand cards with face up cards

        while self.running:
            # 1 Make choice
            # 2 Check end state
            # 3 update turn counter
            print(f"player {self.players[self.turn].name}'s turn")
            sleep(3)
            
            self.turn = (self.turn + 1) % self.playerCount

    def print(self):
        print(f"Deck {self.__deck}")
        for i, player in enumerate(self.players):
            print(f"Player {i}:")
            print(f"    - Face down: {player.faceDown}")
            print(f"    - Face up: {player.faceUp}")
            print(f"    - Hand: {player.hand}")


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.faceDown = []
        self.faceUp = []


class Deck(list):
    def __init__(self, jokers=False):
        super().__init__()
        for suit in CARD_SUITS:
            for value in CARD_VALUES:
                super().append(Card(value, suit))

    def shuffle(self):
        if RANDOM_SEED is not None:
            seed(RANDOM_SEED)

        # Random card insertion in to it's self
        length = len(self)
        for i in range(length):
            card = self.pop(i)
            self.insert(randrange(0, length), card)

    def __repr__(self):
        string = "["
        for card in self:
            string += card.__repr__() + ", "
        return string[:-2] + "]"


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.magic = value in ['2', '3', '7', '10']
    
    def __repr__(self):
        return f"{self.value}{self.suit}"


## Error classes ##
class InvalidPlayerCount(Exception):
    def __init__(self, playerCount):
        message = f"{playerCount} is not enough players for a game of Shed"
        super().__init__(message)


def main():
    game = Shed(2)
    game.play()
    
if __name__ == "__main__":
    main()
