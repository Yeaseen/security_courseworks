from hypothesis import given, settings, strategies as st
from typing import Dict, List
from card_game_utils import *
from correct_card_game import deal, draw, play_hand
from hypothesis import settings, Verbosity
from hypothesis.strategies import lists, sampled_from, builds


MAX_EXAMPLES = 1_000 # lower number => faster, but less coverage
settings.register_profile("yeaseen", settings(max_examples=MAX_EXAMPLES, deadline=None))
settings.load_profile("yeaseen")


def is_valid_deal(num_players: int, dealt_hands: List[Hand]) -> bool:
    '''
    Check that dealt_hands is a valid deal for num_players

    Every player needs HAND_SIZE cards. All cards must be unique, no duplicates.
    It is illegal to call deal with no players or with more than MAX_PLAYERS players.
    '''

    ##1 checking number of players validity (Assuming minimum 2 for win/loss/tie and max)     
    ##2 checking if correct number of hands are dealt
    if not (2 <= num_players <= MAX_PLAYERS) or len(dealt_hands) != num_players:
        return False


    ##3 checking each hand has correct number of cards
    if not all(len(hand) == HAND_SIZE for hand in dealt_hands):
        return False
    
    ##4 checking for duplicates in all of the hands
    unique_cards = set()
    for hand in dealt_hands:
        for card in hand:
            #if card.suit.value<0 or card.suit.value>3:
            #   return False
            #if card.rank.value<2 or card.rank.value>14:
            #    return False
            if card in unique_cards:
                return False
            unique_cards.add(card)
    return True

def num_players_strat():
    return st.integers(min_value=2, max_value=MAX_PLAYERS)


@settings(verbosity=Verbosity.verbose)
@given(num_players=num_players_strat())
def test_deal(num_players: int):
    print("Testing with num_players:", num_players)
    dealt_hands = deal(num_players)
    assert is_valid_deal(num_players, dealt_hands)


def is_valid_draw(old_hand: Hand, num_to_draw: int, new_hand: Hand) -> bool:
    '''
    Check that new_hand is a valid result for draw(old_hand, num_to_draw)

    The new hand should have num_to_draw cards replaced with different cards.
    It is illegal to call draw on an invalid hand or with a negative
    num_to_draw or with a num_to_draw that is greater than the number of cards.
    '''
    rank_count = {}
    suit_count = {}
    unique_cards = set()
    for old_card in old_hand:

        ##checking duplicity in old_hand
        if old_card in unique_cards:
            return False
        unique_cards.add(old_card)
        
        ##checking same rank card should not be greater than 4
        rank_count[old_card.rank.value] = rank_count.get(old_card.rank.value, 0) + 1
        if rank_count[old_card.rank.value] > 4:
            return False
        
        ##checking black with same rank should not be greater than 2
        if old_card.suit.value == 0 or old_card.suit.value == 3: 
            suit_count[('Black',old_card.rank.value)] = suit_count.get(('Black',old_card.rank.value),0) + 1
            if suit_count[('Black',old_card.rank.value)] > 2:
                return False
        
        ##checking white with same rank should not be greater than 2
        else:
            suit_count[('White',old_card.rank.value)] = suit_count.get(('White',old_card.rank.value),0) + 1
            if suit_count[('White',old_card.rank.value)] > 2:
                return False
    
    ##checking unacceptable num_to_draw value
    if num_to_draw < 0 or num_to_draw > HAND_SIZE:
       return False
    
    ##checking old hand and new hand sizes should be equal to HAND_SIZE
    if len(old_hand) != HAND_SIZE or len(new_hand) != HAND_SIZE:
        return False
    

    ##different cards in new hand should match num_to_draw
    different_cards = sum(1 for card in new_hand if card not in old_hand)
    if different_cards != num_to_draw:
        return False
    
    return True

def old_hand_strat():
    #Generating card strategy
    card_strategy = builds(Card, 
                           rank=sampled_from(Rank),
                           suit=sampled_from(Suit))
    #Build a hand of cards of size HAND_SIZE
    #return lists(card_strategy, min_size=2, max_size=HAND_SIZE, unique=True)
    #return lists(card_strategy, min_size=HAND_SIZE, max_size=HAND_SIZE, unique=False)
    return lists(card_strategy, min_size=HAND_SIZE, max_size=HAND_SIZE, unique=True)

def num_to_draw_strat():
    return st.integers(min_value=0, max_value=HAND_SIZE)



@given(old_hand=old_hand_strat(), num_to_draw=num_to_draw_strat())
def test_draw(old_hand: Hand, num_to_draw: int):
    new_hand = draw(old_hand, num_to_draw)
    assert is_valid_draw(old_hand, num_to_draw, new_hand)


"""
def is_valid_play_hand(player: Hand, opponent: Hand, result: GameResult) -> bool:
    '''
    Check that result is a valid outcome of play_hand(player, opponent)
    from the perspective of the player.
    '''
    raise NotImplementedError



def player_strat():
    raise NotImplementedError

def opponent_strat():
    raise NotImplementedError

@given(player=player_strat(), opponent=opponent_strat())
def test_play_hand(player: Hand, opponent: Hand):
    result = play_hand(player, opponent)
    assert is_valid_play_hand(player, opponent, result)

## ---
# Write at least one test for each of the is_valid functions.
# These tests do NOT need to use hypothesis.

def test_is_valid_deal_1():
    raise NotImplementedError

def test_is_valid_draw_1():
    raise NotImplementedError

def test_is_valid_play_hand_1():
    raise NotImplementedError
"""




"""
def main():
    
    print("!Hello, world")

    #hand = deal(1)
    #for card in hand:
        #print(card)
        #rc = rank_counts(card)
        #print(rc)
    
    old_hand = [Card(Rank.TWO, Suit.SPADES), Card(Rank.TWO, Suit.CLUBS), Card(Rank.TWO, Suit.CLUBS)]
    rank_count = {}
    suit_count = {}
    unique_cards = set()
    for old_card in old_hand:
        if old_card in unique_cards:
            print("Anomaly 0")
        unique_cards.add(old_card)

        rank_count[old_card.rank.value] = rank_count.get(old_card.rank.value, 0) + 1
        if rank_count[old_card.rank.value] > 4:
            print("Anomaly 1")
        if old_card.suit.value == 0 or old_card.suit.value == 3: 
            suit_count[('Black',old_card.rank.value)] = suit_count.get(('Black',old_card.rank.value),0) + 1
            if suit_count[('Black',old_card.rank.value)] > 2:
                print("Anomaly 2")
        else:
            suit_count[('White',old_card.rank.value)] = suit_count.get(('White',old_card.rank.value),0) + 1
            if suit_count[('White',old_card.rank.value)] > 2:
                print("Anomaly 3")    
    
    print(rank_count)
    print(suit_count)

if __name__ == "__main__":
    main()
"""