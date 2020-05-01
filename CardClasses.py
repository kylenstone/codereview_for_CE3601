"""Created: 3/30/2019

Objects to represent a playing Card, playing Deck, and Player
"""

from enum import Enum
from itertools import product
from random import shuffle

class ranks(Enum):
    TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE = range(2, 15)

class suits(Enum):
    CLUBS,DIAMONDS,HEARTS,SPADES = range(1, 5)

class Card(object):
    """Card object represents a standard playing card.

    The object attributes, suit and rank, are implemented as enums whose values determine the weight of the card
    """

    def __init__(self, suit, rank, in_deck = False, image = None):
        if rank in ranks and suit in suits:
            self.rank = rank
            self.suit = suit
        else:
            self.rank = None
            self.suit = None

        self.in_deck = in_deck
        self.image = image
        self.position_x, self.position_y = 0,0
        self.horizontal_demension = None
        self.vertical_demension = None

    def __str__(self):
        return str(self.rank.name) + " " + str(self.suit.name)

    def __eq__(self, other):
        return True if self.rank == other.rank and self.suit == other.suit else False

    def __gt__(self, other):
        """Tests suit precedence, if suits are equal then checks ranks precedence"""
        if self.suit == other.suit:
            if self.rank.value > other.rank.value:
                return True
        if self.suit.value > other.suit.value:
            return True

        return False

class Deck(object):
    """A deck is a collection of 52 Card objects

    Object attributes: cards, removed
    methods: draw(range = 1), deck_shuffle()
    """

    def __init__(self):
        self.cards = [Card(suit, rank, in_deck = True) for suit, rank in product(suits, ranks)]
        self.removed = []

    def __str__(self):
        return str([str(card) for card in self.cards])

    def draw(self, range = 1):
        """Draw card(s) by removing them from deck"""
        drawn_cards = self.cards[:range]
        for card in drawn_cards:
            card.in_deck = False
        del self.cards[:range]
        self.removed.append(drawn_cards)
        return drawn_cards

    def deck_shuffle(self):
        """Shuffles deck object in place"""
        shuffle(self.cards)

class Player(object):
    """Implementation of a player object

    Object attributes: name, hand, score, turn, card_selected
    methods: remove_from_hand(card)
    """

    def __init__(self, name, hand = None, score = 0, turn = False):
        self.name = name
        self.hand = hand
        self.score = score
        self.turn = turn
        self.selected_card = None

    def __str__(self):
        return str(self.name)

    def remove_from_hand(self, card):
        """Removes a card object from the players hand"""
        if card and card in self.hand:
            position = self.hand.index(card)
            del self.hand[position]
            return card