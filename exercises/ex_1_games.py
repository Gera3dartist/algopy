"""
Card game durak
"""
from typing import List
from enum import Enum
import random as rd
import itertools as it
from time import sleep
import logging
import sys


LOGGER = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(handler)



class CardSuit(Enum):
	diamond = 1
	heart = 2
	spade = 3
	club = 4


CARD_RANK = ('A', 'K', 'Q', 'J', '10', '9', '8', '7', '6')
CARD_SUIT = ('diamond', 'heart', 'spade', 'club')

class CardMixin:

	def show_cards(self, cards):
		LOGGER.info(f'{self} in game with cards: ')
		for i in cards[::-1]:
			LOGGER.info(i)


class GameCard:
	__slots__ = ('suit', 'rank', 'is_trump')

	def __init__(self, rank: str, suit: str, is_trump: bool = False):
		self.suit = suit
		self.rank = rank
		self.is_trump = is_trump

	def __gt__(self, other):
		return (self.rank > other.rank and self.suit == other.suit) or \
			(self.is_trump and not other.is_trump)

	def __ge__(self, other):
		return (self.rank >= other.rank and self.suit == other.suit)

	def __repr__(self):
		return f'<{self.__class__.__name__}>_rank:{self.rank}_suit:{self.suit}'


class CardDeck(CardMixin):
	__slots__ = ('cards', 'trump')

	def __init__(self, cards: list, trump: str):
		self.cards = cards
		rd.shuffle(self.cards)
		self.trump = trump

		self.show_cards(self.cards)
		LOGGER.info(f'and trump is : {self.trump}')

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
	__slots__ = ('cards', 'name')

	def __init__(self, cards: set, name: str):
		self.cards = cards
		self.name = name
		self.show_cards(self.cards)

	@property
	def active(self):
		return len(self.cards) > 0
	
	def take_cards(self, deck: CardDeck):
		needed = 6 - len(self.cards)
		if not needed:
			return

		for card in deck.take_cards(needed):
			if not card:
				break
			self.cards.append(card)

	def take_cards_on_defeat(self, context: List[GameCard]):
		LOGGER.info(f'{self} defeat in round and took cars: {context}')
		self.cards.extend(context)
		
	def make_turn(self)-> GameCard:
		context = None
		while True:
			card = self.select_card(context)
			if card is None:
				break
			yield card
			context = yield

	def select_card(self, context: List[GameCard] = None):
		card = None
		try:
			if context is None:
				self.cards.sort(reverse=True)
				card = self.cards[-1]
				
			else:
				for _card in context:
					for c in self.cards.sort(reverse=True):
						 if c.rank==card.rank:
						 	card = c
		except IndexError:
			pass

		if card:
			card = self.cards.pop(self.cards.index(card))	
		return card

	def handle_turn(self, card: GameCard) -> List[GameCard]:
		response_card = None
		for c in self.cards:
			if c > card:
				response_card = c
				break

		if response_card:
			self.cards.remove(c)

		return [card, response_card, not self.active]

	def __repr__(self):
		return f'<Player_{self.name}>'

	def __str__(self):
		return f'<{self.name}>'

class GameManager:
	def __init__(self, players: List[CardPlayer], carddeck: CardDeck):
		self.players = players
		self.carddeck = carddeck
		self.played_cards = []
		self.winners = []

	def get_next_player(self, start=0):
		_max, temp = len(self.players) - 1, start
		while True:
			yield temp
			temp += 1
			if temp > len(self.players) - 1:
				temp = 0

	def set_round_defeat(self, first_player, next_player, context):
		first_player.take_cards(self.carddeck)
		next_player.take_cards_on_defeat(context)
		if not first_player.active:
			LOGGER.info(f'>>REMOVED PLAYER on DEFEAT: {first_player}')
			self.players.remove(first_player)

	def set_round_win(self, first_player, next_player):
		for player in [first_player, next_player]:
			player.take_cards(self.carddeck)
			if not player.active:
				LOGGER.info(f'>>REMOVED PLAYER on WIN: {player}')
				self.players.remove(player)

	def throw_cards(self, context):
		for card in context:
			self.played_cards.append(card)

	def play_round(self, first_player, next_player)-> bool:
		fpgen = first_player.make_turn()
		card = next(fpgen, (None, None)) # warm up generator
		played_cards = []
		attacker_no_cards, defender_no_cards = False, False
		while True:
			LOGGER.info(f'Attacker gave card: {card}')
			sleep(0.5)

			if card is None:
				self.set_round_win(first_player, next_player)
				LOGGER.info(f'Round win: {context}')
				self.throw_cards(context)
				break

			card, response_card, defender_no_cards = next_player.handle_turn(card)
			context = [card, response_card]

			if len(next_player.cards)==0:
				self.set_round_win(first_player, next_player)
				LOGGER.info(f'No cards Round win: {context}')
				self.throw_cards(context)
				break

			elif response_card is None:
				context.pop()
				# None means loss
				LOGGER.info(f'Round lost: {context}')
				LOGGER.info(f'Cards of defender: {next_player.cards}')
				self.set_round_defeat(first_player, next_player, [card])
				LOGGER.info(f'Cards of defender after taking: {next_player.cards}')
				return True

			LOGGER.info(f'Defender has beaten card: {context}')
			played_cards.extend(context)
			card = fpgen.send(context)
		return False

	def peak_first(self):
		res = [] 
		for i, p in enumerate(self.players):
			try:
				min_card = sorted(filter(lambda c: c.is_trump, p.cards), reverse=True).pop()
			except IndexError:
				continue

			res.append((i, min_card))
		return sorted(res, key=lambda x: x[1], reverse=True)[-1][0]

	def get_player(self, first):
		_next = first + 1
		if _next == len(self.players):
			return 0
		return _next
			

	def start_game(self):
		LOGGER.info('starting the game')
		
		first = self.peak_first()
		LOGGER.info(f'FIrst player is {self.players[first]}')
		_next = self.get_player(first)

		round_counter = 1
		
		while len(self.players) > 1:
			attacker = self.players[first]
			defender = self.players[_next]
			LOGGER.info(f'Round number: {round_counter}')
			LOGGER.info(f'Players in round: {"|".join([str(p) for p in self.players if p.active==True])}')
			LOGGER.info(f'Attacker: {attacker}, has cards: {len(attacker.cards)}')
			LOGGER.info(f'Defender: {defender}, has cards: {len(defender.cards)}')
			sleep(0.1)
			LOGGER.info(f'Played cards: {len(self.played_cards)}')

			if self.play_round(attacker, defender):
				if len(self.players) == 2:
					continue
				LOGGER.info('set first/last in IF branch')
				first = self.get_player(_next)
				_next = self.get_player(first)
			else:
				LOGGER.info('set first/last in ELSE branch')
				first, _next = _next, self.get_player(_next)
			LOGGER.info(f'NEXT: {_next}')
			LOGGER.info(f'FIRST: {first}')

			round_counter+=1
		LOGGER.info(f'Player in game: {self.players}')

			
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

	players = [CardPlayer([c for c in deck.take_cards(6)], name=next(name_gen)) 
		for i in range(0, rd.randint(2, 6))]
	manager = GameManager(players, deck)
	manager.start_game()
	

if __name__ == '__main__':
	main()
