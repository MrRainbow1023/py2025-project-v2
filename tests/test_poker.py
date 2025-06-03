import unittest
from main import Card, Deck, Player

class TestCardGame(unittest.TestCase):

    def test_card_creation(self):
        card = Card("A", "s")
        self.assertEqual(card.get_value(), ("A", "s"))
        self.assertEqual(str(card), "A♠")

    def test_invalid_card_rank(self):
        with self.assertRaises(ValueError):
            Card("1", "s")

    def test_invalid_card_suit(self):
        with self.assertRaises(ValueError):
            Card("A", "x")

    def test_deck_has_52_cards(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_deck_shuffle_changes_order(self):
        deck = Deck()
        original = deck.cards[:]
        deck.shuffle()
        self.assertNotEqual(original, deck.cards)

    def test_deal_cards(self):
        deck = Deck()
        player1 = Player(100, "P1")
        player2 = Player(100, "P2")
        deck.deal([player1, player2], cards_per_player=5)
        self.assertEqual(len(player1.get_player_hand()), 5)
        self.assertEqual(len(player2.get_player_hand()), 5)
        self.assertEqual(len(deck.cards), 42)

    def test_deal_too_many_cards(self):
        deck = Deck()
        players = [Player(100, f"P{i}") for i in range(30)]
        with self.assertRaises(ValueError):
            deck.deal(players, cards_per_player=2)

    def test_change_card_valid_index(self):
        player = Player(100, "Tester")
        card1 = Card("5", "h")
        card2 = Card("Q", "s")
        player.take_card(card1)
        replaced = player.change_card(card2, 0)
        self.assertEqual(replaced, card1)
        self.assertEqual(player.get_player_hand()[0], card2)

    def test_change_card_invalid_index(self):
        player = Player(100, "Tester")
        player.take_card(Card("9", "c"))
        with self.assertRaises(IndexError):
            player.change_card(Card("K", "d"), 5)

    def test_hand_rank_pair(self):
        player = Player(100, "Karol")
        cards = [Card("A", "s"), Card("A", "h"), Card("5", "d"), Card("7", "c"), Card("9", "h")]
        for c in cards:
            player.take_card(c)
        self.assertIn("Pair", player.hand_rank()[2])


    def test_hand_rank_high_card(self):
        player = Player(100, "Karol")
        cards = [Card("2", "s"), Card("5", "h"), Card("7", "d"), Card("9", "c"), Card("J", "h")]
        for c in cards:
            player.take_card(c)
        self.assertIn("High Card", player.hand_rank())

if __name__ == "__main__":
    unittest.main()
