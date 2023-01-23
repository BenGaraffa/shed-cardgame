from random import randrange, seed


CARD_SUITS = ["♤", "♧", "♡", "♢"]
CARD_VALUES = [f"{i}" for i in range(1, 11)] \
            + ["J", "Q", "K", "A"]
RANDOM_SEED = None

class Shed:
    def __init__(self, players=2):
        self.players = players
        self.deck = Deck()
    
class Deck(list):
    def __init__(self, jokers=False):
        super().__init__()
        for suit in CARD_SUITS:
            for value in CARD_VALUES:
                super().append(Card(value, suit))

    def shuffle(self):
        seed(0)
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
        self.magic = value in [2, 3, 7, 10]
    
    def __repr__(self):
        return f"{self.value}{self.suit}"


def main():
    game = Shed()
    print(game.deck)
    game.deck.shuffle()
    print(game.deck)

if __name__ == "__main__":
    main()
