from card_game_utils import *
from typing import Dict, List
import random

def deck():
    return [Card(Rank(rank), Suit(suit)) for suit in range(0, 4) for rank in range(2, 15)]

def deal(num_players:int) -> List[Hand]:
    # everyone gets 5 unique cards
    dd = deck()
    random.shuffle(dd)
    return [dd[p*HAND_SIZE:(p*HAND_SIZE)+HAND_SIZE] for p in range(num_players)]

def draw(h:Hand, num_to_draw:int) -> Hand:
    # replace num_to_draw with new cards
    dd = deck()
    for c in h:
        dd.remove(c)
    random.shuffle(dd)
    return dd[:num_to_draw] + h[num_to_draw:]

def play_hand(player:Hand, opponent:Hand) -> bool:
    # did player beat opponent? (intentionally ugly)
    pc = rank_counts(player)
    oc = rank_counts(opponent)
    for i in range(HAND_SIZE, 0, -1):
        if i in pc.values():
            if i not in oc.values():
                return GameResult.WIN
            else:
                break
        if i in oc.values():
            return GameResult.LOSS
    for i in range(HAND_SIZE, 0, -1):
        if i in oc.values():
            if i not in pc.values():
                return GameResult.LOSS
            else:
                break
        if i in pc.values():
            break
    for i in range(HAND_SIZE, 0, -1):
        if i in oc.values():
            pm = min([k.value for (k, v) in pc.items() if v == i])
            om = min([k.value for (k, v) in oc.items() if v == i])
            if pm == om:
                return GameResult.TIE
            else:
                return GameResult.WIN if pm < om else GameResult.LOSS

