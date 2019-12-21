"""
Card game durak
"""
from typing import List
from enum import Enum
import random as rd
import itertools as it

class CardSuit(Enum):
	diamond = 1
	heart = 2
	spade = 3
	club = 4


CARD_RANK = ('A', 'K', 'Q', 'J', '10', '9', '8', '7', '6')
CARD_SUIT = ('diamond', 'heart', 'spade', 'club')

class CardMixin:

	def show_cards(self, cards):
		print(f'{self} in game with cards: ')
		for i in cards[::-1]:
			print(i)


class GameCard:
	__slots__ = ('suit', 'rank', 'is_trump')

	def __init__(self, rank: str, suit: str, is_trump: bool = False):
		self.suit = suit
		self.rank = rank
		self.is_trump = is_trump

	def __gt__(self, other):
		return (self.rank > other.rank and self.suit == other.suit) or \
			(self.is_trump and not other.is_trump)

	def __repr__(self):
		return f'<{self.__class__.__name__}>_rank:{self.rank}_suit:{self.suit}'


class CardDeck(CardMixin):
	__slots__ = ('cards', 'trump')

	def __init__(self, cards: list, trump: str):
		self.cards = cards
		rd.shuffle(self.cards)
		self.trump = trump

		self.show_cards(self.cards)
		print(f'and trump is : {self.trump}')

	def is_empty(self):
		return not self.cards

	def take_cards(self, count:int):
		while self.cards and count > 0:
			yield self.cards.pop()
			count -= 1

	def __repr__(self):
		return f'<{self.__class__.__name__}>'
	
	@classmethod
	def create_deck(cls):
	
		trump = CARD_SUIT[rd.randint(0, len(CARD_SUIT)-1)]
		cards = [GameCard(rank, suit, suit==trump) 
			for rank, suit in it.product(CARD_RANK, CARD_SUIT)]
		return CardDeck(cards, trump)


class CardPlayer(CardMixin):
	__slots__ = ('initial_cards', 'name')

	def __init__(self, initial_cards: set, name: str):
		self.initial_cards = initial_cards
		self.name = name
		self.show_cards(self.initial_cards)

	def take_cards(deck: CardDeck):
		return

	def make_turn()-> GameCard:
		while True:
			card = self.select_card(context)
			if card is None:
				break
			yield card
			context = yield

	def select_card(self, context: dict = None):
		filter(lambda c: c.is_trump == False, sorted(self.cards))
		

	def handle_turn(self, card: GameCard):
		print('Handle turn')
		return

	def __repr__(self):
		return f'<Player_{self.name}>'



class GameManager:
	def __init__(self, players: List[CardPlayer], carddeck: CardDeck):
		self.players = players
		self.carddeck = carddeck
		self.played_cards = []

	def get_next_player(self, start=0):
		_max, temp = len(self.players) - 1, start
		while True:
			yield temp
			temp += 1
			if temp > _max:
				temp = 0

	def set_round_defeat(first_player, next_player, context):
		pass

	def set_round_win(first_player, next_player)

	def play_round(first_player, next_player):
		fpgen = first_player.make_turn()
		card = next(fpgen) # warm up generator
		while True:
			context = next_player.handle_turn(card)
			if context is None:
				self.set_round_defeat(first_player, next_player, context)
			elif cord is None:
				self.set_round_win(first_player, next_player)
				break
			card = fpgen.send(context)


	def start_game(self):
		self.serve_cards()
		player_gen = self.get_next_player()
		
		first = self.peak_first()
		_next = next(player_gen)
	
		while len(self.players) > 1:
			self.play_round(self.players[first], self.players[_next])
			first, _next = next(player_gen), next(player_gen)

			
def select_name():
	names = ['Stepan', 'Ivan', 'Petro', 'Nazar', 'Andrii', 'Myron', 'Gania', 'Orysia']
	rd.shuffle(names)
	start = 0
	while True:
		yield names[start]
		start+=1
		if start == len(names):
			start = 0
		

def main():
	deck = CardDeck.create_deck()

	name_gen = select_name()
	next(name_gen)
	players = [CardPlayer([c for c in deck.take_cards(6)], name=next(name_gen)) 
		for i in range(0, rd.randint(2, 6))]
	manager = GameManager(players, deck)
	


if __name__ == '__main__':
	for i in filter(lambda x: x%2 == 0, range(5)):
		print(i)
	# main()
