from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from typing import Dict, List

class Suit(Enum):
    SPADES = 0
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3

    def __str__(self):
        return self.name.lower()

@total_ordering
class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __str__(self):
        return self.name.lower()

    def __lt__(self, other):
        return isinstance(other, Rank) and self.value < other.value


@dataclass(frozen=True)
class Card:
    rank: Rank
    suit: Suit

    def __str__(self):
        return f'{str(self.rank)} of {str(self.suit)}'

class GameResult(Enum):
    WIN = 0
    LOSS = 1
    TIE = 2

Hand = List[Card]
HAND_SIZE = 5
DECK_SIZE = len(Rank) * len(Suit)
MAX_PLAYERS = DECK_SIZE // HAND_SIZE

def rank_counts(h: Hand) -> Dict[Rank, int]:
    '''
    Returns a dictionary mapping Ranks to the number of cards
    of that Rank in h.
    '''
    result = {}
    for c in h:
        result[c.rank] = result.get(c.rank, 0) + 1
    return result

