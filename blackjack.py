import copy
from enum import Enum
import random


class Blackjack:

    class GameState(Enum):
        IN_PROGRESS = 1
        WIN = 2
        LOSS = 3
        TIE = 4
        OUT_OF_CARDS = 5
    
    class Action(Enum):
        HIT = 1
        STAND = 2

    def __init__(self, num_decks=4, dealer_value_limit=17):
        self.num_decks = num_decks
        self.dealer_value_limit = dealer_value_limit
        self.deck = []
        self.played_cards = []
        self.actions = [self.Action.HIT, self.Action.STAND]

    def shuffle(self):
        self.deck.clear()
        self.played_cards.clear()
        for _ in range(self.num_decks):
            for _ in range(4):
                self.deck += range(1,11)
                self.deck += (10,10,10)
        random.shuffle(self.deck)

    def next_card(self):
        new_card = self.deck.pop()
        self.played_cards.append(new_card)
        return new_card
    
    def has_next_card(self):
        return len(self.deck) > 0
    
    def get_state(self):
         return [self.played_cards.copy(), self.player_cards.copy(), self.dealer_cards.copy(), self.deck.copy()]
    
    def set_state(self, state):
        self.played_cards = state[0]
        self.player_cards = state[1]
        self.dealer_cards = state[2]
        self.deck = state[3]

    def val(self, deck):
        deck_val = sum(deck)
        if 1 in deck:
            if deck_val + 10    <= 21:
                deck_val += 10
        return deck_val

    def start_game(self):        
        self.player_cards = []
        self.dealer_cards = []

        if len(self.deck) < 3:
             return self.GameState.OUT_OF_CARDS

        self.player_cards.append(self.next_card())
        self.player_cards.append(self.next_card())

        self.dealer_cards.append(self.next_card())

        return self.GameState.IN_PROGRESS
    
    def hit(self):
        if not self.has_next_card():
            return self.GameState.OUT_OF_CARDS
        new_card = self.next_card()
        self.player_cards.append(new_card)

        if self.val(self.player_cards) > 21:
            return self.GameState.LOSS
        
        return self.GameState.IN_PROGRESS
    
    def stand(self):
        new_cards = []
        while self.val(self.dealer_cards) < self.dealer_value_limit and self.val(self.dealer_cards) < 21:
            if not self.has_next_card():
                return self.GameState.OUT_OF_CARDS
            new_card = self.next_card()
            self.dealer_cards.append(new_card)
            new_cards.append(new_card)
        
        if self.val(self.dealer_cards) > 21:
            return self.GameState.WIN
        
        if self.val(self.dealer_cards) < self.val(self.player_cards):
            return self.GameState.WIN
        elif self.val(self.dealer_cards) > self.val(self.player_cards):
            return self.GameState.LOSS
        else:
            return self.GameState.WIN

 
    def initial_state(self):
        self.shuffle()
        self.start_game()
        return self.get_state()

    def result(self, current_state, action):
        self.set_state(copy.deepcopy(current_state))
        if action == self.Action.HIT:
            res = self.hit()
        else:
            res = self.stand()
        return self.get_state()
    
    def reward(self, current_state, action):
        self.set_state(copy.deepcopy(current_state))
        if action == self.Action.HIT:
            res = self.hit()
        else:
            res = self.stand()
        if res == self.GameState.IN_PROGRESS or res == self.GameState.TIE:
            return 0
        if res == self.GameState.LOSS:
            return -1
        if res == self.GameState.WIN:
            return 10
    def is_terminal(self, state, action):
        if action == self.Action.STAND:
            return True
        elif self.val(state[1]) > 21:
            return True
        return False
    
