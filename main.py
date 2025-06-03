import random
from collections import Counter

class Card:
    unicode_dict = {'s': '\u2660', 'h': '\u2665', 'd': '\u2666', 'c': '\u2663'}  # ♠ ♥ ♦ ♣

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def get_value(self):
        return (self.rank, self.suit)

    def __str__(self):
        return f"{self.rank}{Card.unicode_dict[self.suit]}"


class Deck:
    def __init__(self, *args):
        ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
        suits = ('s', 'h', 'd', 'c')
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]

    def __str__(self):
        return ' '.join(str(card) for card in self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, players, cards_per_player=5):
        for i in range(cards_per_player):
            for player in players:
                if self.cards:  # zabezpieczenie
                    player.take_card(self.cards.pop(0))


class Player:
    def __init__(self, money, name=""):
        self.__stack_ = money
        self.__name_ = name
        self.__hand_ = []

    def take_card(self, card):
        self.__hand_.append(card)

    def get_stack_amount(self):
        return self.__stack_

    def change_card(self, card, idx):
        replaced = self.__hand_[idx]
        self.__hand_[idx] = card
        return replaced

    def get_player_hand(self):
        return tuple(self.__hand_)

    def cards_to_str(self):
        return ' '.join(str(card) for card in self.__hand_)

    def get_name(self):
        return self.__name_

    def hand_rank(self):
        ranks = [card.rank for card in self.__hand_]

        rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                       '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        values = [rank_values[r] for r in ranks]
        count = Counter(values)
        counts = count.values()
        most_common = count.most_common()

        if 4 in counts:
            return (7, most_common[0][0], "Four of a Kind")
        elif 3 in counts and 2 in counts:
            return (6, most_common[0][0], "Full House")
        elif 3 in counts:
            return (3, most_common[0][0], "Three of a Kind")
        elif list(counts).count(2) == 2:
            pairs = [val for val, c in most_common if c == 2]
            return (2, max(pairs), "Two Pair")
        elif 2 in counts:
            return (1, most_common[0][0], "One Pair")
        else:
            return (0, max(values), "High Card")


# -------------------- MAIN --------------------
if __name__ == "__main__":
    deck = Deck()
    deck.shuffle()

    p1 = Player(100, "Karol")
    p2 = Player(100, "CPU")
    players = [p1, p2]

    deck.deal(players, cards_per_player=5)


    for player in players:
        print(f"{player.get_name()}: {player.cards_to_str()}")
        print(f"Hand rank: {player.hand_rank()}")