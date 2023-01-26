from random import randrange, seed
from time import sleep
import os


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

    def dealAllHands(self):
        for location in ["faceDown", "faceUp", "hand"]:
            for card in range(self.minHandSize):
                for i in range(self.playerCount):
                    getattr(self.players[i], location).append(self.__deck.pop())

    def generateOptions(self):
        # Generate options for the current player
        return ['swapFaceUps'], ['swap face up cards']

    def play(self):
        self.dealAllHands()

        # Take turns swapping hand cards with face up cards

        while self.running:
            self.print()
            # 1 Make choice
            answer = None
            while answer is None:
                optFuncs, optStrs = self.generateOptions()
                optStrs = ' '.join([f'{chr(i + 97)}) {opt}' for i, opt in enumerate(optStrs)])
                answer = input("Options: " + optStrs)

            # 2 Check end state


            # 3 update turn counter
            self.turn = (self.turn + 1) % self.playerCount

    def print(self):
        os.system('cls')
        print(f"## player {self.players[self.turn].name}'s turn ##")
        print('opponents: {opponent\'s name}(face ups)[no of face downs]:\n', end='')
        for i in [(i + self.turn) % self.playerCount for i in range(self.playerCount)][1:]:
            print('{' + str(self.players[i].name) + '}', end='')
            print(f'( {self.__fCards(self.players[i].faceUp)})', end='')
            print(f'[{len(self.players[i].faceDown)}]', end='   ')
        
        dk = len(self.__deck)
        dk = dk if dk > 0 else '--'
        hp = self.heap[-1] if len(self.heap) > 0 else "--"
        print(f"""\n
            ┌────────────────────────────────┐
            │                  ┌──────┐      │
            │       ┌──────┐  ┌┤xxxxxx│      │
            │       │      │  ││x    x│      │
            │       │      │  ││x {dk:<3}x│      │
            │       │  {hp}  │  ││x    x│      │
            │       │      │  ││xxxxxx│      │
            │       │      │  │┼─────┬┘      │
            │       └──────┘  └──────┘       │
            │         heap      deck         │
            └────────────────────────────────┘
            """)
        player = self.players[self.turn]
        print(f'face downs left: {len(player.faceDown)}')
        print(f'your face ups: \t\t{self.__fCards(player.faceUp)}')
        print(f'your hand: \t\t{self.__fCards(player.hand)}\n')

    @staticmethod
    def __fCards(cards):
        string = ''
        for card in cards:
            string += card.__repr__() + ' '
        return string

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.faceDown = []
        self.faceUp = []

    def swapFaceUps(self):
        answer = None
        while answer is None:
            answer = input(
                f"which pair to swap?: "
            ).strip().lower()
            if answer == 'y': answer = True
            elif answer == 'n': answer = False
            else: answer = None

        if answer:
            print("!!!")


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
    game = Shed(4)
    game.play()
    
if __name__ == "__main__":
    main()
