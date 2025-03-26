# Poker

""" Poker

Generate approximate chances for Blotkarz win in a specified game of Poker

2 - 10 -> Numbered cards for Blotkarz
11 - 14 (Jack - Ace) -> Cards for Figurant

Suits 1-4 (order doesn't matter)

Generates GAMES number of games, and based on result provides approximation
"""
import random
import itertools
from collections import Counter

GAMES = 1000

JACK = 11
QUEEN = 12
KING = 13
ACE = 14
SUITS = [1,2,3,4]


def checkIncreasingValues(cards):
    cards_len = len(cards)
    ranked_cards = sorted(set(card[0] for card in cards))
    if len(ranked_cards) != cards_len: return False

    return ranked_cards == list(range(ranked_cards[0], ranked_cards[0] + len(ranked_cards)))


def countSuits(cards: list, num: int) -> int:
    return list(sumSuit(cards).values()).count(num)


def countCards(cards: list, num: int ) -> int:
    return list(sumCards(cards).values()).count(num)

# Return highest card value in deck
def getHighCard(cards: list) -> int:
    return max(cards)[0]

def sumCards(cards : list) -> Counter:
    return Counter(card for card,_ in cards)

# Sum instances of the same suit
def sumSuit(cards: list) -> Counter:
    return Counter(suit for _, suit in cards)


# ======= Checks for specific hands =======

def checkPoker(cards: list) -> bool:
    return checkIncreasingValues(cards) and countSuits(cards,5) == 1

def checkQuads(cards: list) -> bool:
    return countCards(cards, 4) == 1

def checkFull(cards:list) -> bool:
    return checkPair(cards) and checkThree(cards)

def checkFlush(cards:list) -> bool:
    return countCards(cards,5) and not checkIncreasingValues(cards)

def checkStraight(cards:list) -> bool:
    return checkIncreasingValues(cards)

def checkThree(cards: list) -> bool:
    return countCards(cards,3) == 1

def checkTwoPairs(cards : list) -> bool:
    return countCards(cards,2) == 2


def checkPair(cards: list) -> bool:
    return countCards(cards, 2) == 1



def genCardDeck(card_range, suits):
    deck = list(itertools.product(card_range,suits))
    return random.sample(deck, 5)



def checkHandStrength(cards):
    for checker, value in hand_checks:
        if checker(cards): return value
    return 0

def play(figurant_range, blotkarz_range):
    blotkarz_wins = 0
    for _ in range(GAMES):
        figurant = genCardDeck(figurant_range, SUITS)
        blotkarz = genCardDeck(blotkarz_range, SUITS)
        if checkHandStrength(blotkarz) > checkHandStrength(figurant):
            blotkarz_wins+=1
    print(f"Blotkarz vs Figurant (win chance): {blotkarz_wins/GAMES}")


hand_checks = [
    (checkPoker, 8),
    (checkQuads, 7),
    (checkFull, 6),
    (checkFlush, 5),
    (checkStraight, 4),
    (checkThree, 3),
    (checkTwoPairs, 2),
    (checkPair, 1)
]


if __name__ == "__main__":
    blotkarz_basic= [i for i in range(2,JACK)]
    figurant_basic = [i for i in range(JACK, ACE + 1)]
    #blotkarz_win = [2,3,4] # After a few experiments, blotkarz needs three consecutive card values to win reliably
    play(figurant_basic, blotkarz_basic)
