import random
from collections import Counter
from datetime import datetime


def log_game(filename, players, winner):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"=== New Game ({now}) ===\n")
        for p in players:
            rank_value, high_card, rank_name = p.hand_rank()
            file.write(f"{p.get_name()}: {p.cards_to_str()} --> {rank_name} (high card: {high_card})\n")
        file.write(f"\nWinner: {winner.get_name()}\n\n")


class Card:
    unicode_dict = {'s': '\u2660', 'h': '\u2665', 'd': '\u2666', 'c': '\u2663'}
    str_to_rank = {
        '2': 2, '3': 3, '4': 4, '5': 5,
        '6': 6, '7': 7, '8': 8, '9': 9,
        '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }
    valid_suits = ['s', 'h', 'd', 'c']

    def __init__(self, rank, suit):
        if isinstance(rank, str):
            rank = self.str_to_rank.get(rank)
        if rank not in range(2, 15):
            raise ValueError(f"Invalid card rank: {rank}")
        if suit not in self.valid_suits:
            raise ValueError(f"Invalid card suit: {suit}")

        self.rank = rank
        self.suit = suit

    def get_value(self):
        rank_str = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}.get(self.rank, str(self.rank))
        return (rank_str, self.suit)

    def __str__(self):
        rank_str = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}.get(self.rank, str(self.rank))
        return f"{rank_str}{Card.unicode_dict[self.suit]}"


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
        total_needed = len(players) * cards_per_player
        if total_needed > len(self.cards):
            raise ValueError("Not enough cards in the deck to deal.")

        for _ in range(cards_per_player):
            for player in players:
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
        values = ranks  # już są liczbami
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
def main():
    deck = Deck()
    deck.shuffle()

    p1 = Player(100, "Karol")
    p2 = Player(100, "CPU")
    players = [p1, p2]

    deck.deal(players, cards_per_player=5)

    print("Hands:")
    best_rank = (-1, -1)
    winner = None

    for p in players:
        print(f"{p.get_name()}: {p.cards_to_str()}")
        rank_value, high_card, rank_name = p.hand_rank()
        print(f"  ⤷ Hand: {rank_name} (high card: {high_card})")

        current_rank = (rank_value, high_card)
        if current_rank > best_rank:
            best_rank = current_rank
            winner = p

    print(f"\nWinner: {winner.get_name()} with {winner.hand_rank()[2]}!\n")

    # Zapisz log do pliku
    log_game("game_log.txt", players, winner)


if __name__ == "__main__":
    main()
