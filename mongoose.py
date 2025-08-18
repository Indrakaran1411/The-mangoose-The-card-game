import random
from collections import deque, defaultdict

# Define the ranks and suits in a standard deck of cards
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']


# Create a Card class for better structure
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        return str(self)


# Create a Deck class to handle deck operations
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(rank, suit))
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None


# Define the game class for Mongoose
class MongooseGame:
    def __init__(self):
        self.deck = Deck()
        self.hands = {'A': [], 'B': [], 'C': [], 'D': []}

        for player in self.hands:
            for _ in range(13):
                self.hands[player].append(self.deck.draw())

        self.center_pile = []
        self.player_piles = defaultdict(deque)
        self.turn_order = ['A', 'B', 'C', 'D']
        self.current_player = 0

    def play_game(self):
        while not self.is_game_over():
            self.play_turn()
            self.current_player = (self.current_player + 1) % 4

        print(f"Game over! Player {self.turn_order[self.current_player]} wins!")

    def play_turn(self):
        player = self.turn_order[self.current_player]
        hand = self.hands[player]
        print(f"\nPlayer {player}'s turn. Hand: {hand}")

        while hand:
            card = hand.pop(0)
            print(f"Player {player} draws {card}")

            if self.can_place_in_center_pile(card):
                self.center_pile.append(card)
                print(f"Placed {card} in the center pile. Center pile: {self.center_pile}")
            elif self.can_place_on_other_pile(card):
                target_player = self.find_target_player(card)
                self.player_piles[target_player].appendleft(card)
                print(
                    f"Placed {card} on Player {target_player}'s pile. Player {target_player}'s pile: {self.player_piles[target_player]}")
            else:
                self.player_piles[player].appendleft(card)
                print(f"Placed {card} on Player {player}'s pile. Player {player}'s pile: {self.player_piles[player]}")
                break  # End the turn when a card is placed on the player's own pile

        if not hand:
            print(f"Player {player}'s hand is empty. Picking up and flipping the pile.")
            self.hands[player] = []
            while self.player_piles[player]:
                self.hands[player].append(self.player_piles[player].pop())

    def can_place_in_center_pile(self, card):
        if not self.center_pile:
            return True
        top_card = self.center_pile[-1]
        return (
                card.rank == top_card.rank or  # Same rank, different suit
                (card.suit == top_card.suit and self.rank_difference(top_card, card) == 1)  # Same suit, one rank higher
        )

    def can_place_on_other_pile(self, card):
        for opponent in self.turn_order:
            if opponent != self.turn_order[self.current_player]:
                if self.player_piles[opponent]:
                    top_card = self.player_piles[opponent][0]
                    if self.rank_difference(top_card, card) == 1:
                        return True
        return False

    def find_target_player(self, card):
        for opponent in self.turn_order:
            if opponent != self.turn_order[self.current_player]:
                if self.player_piles[opponent]:
                    top_card = self.player_piles[opponent][0]
                    if self.rank_difference(top_card, card) == 1:
                        return opponent
        return None

    def rank_difference(self, card1, card2):
        # Compute the difference in rank between two cards
        rank1 = RANKS.index(card1.rank)
        rank2 = RANKS.index(card2.rank)
        return rank2 - rank1

    def is_game_over(self):
        return any(not hand for hand in self.hands.values())


# To play the game
if __name__ == "__main__":
    game = MongooseGame()
    game.play_game()