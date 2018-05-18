import json
from Tile import Tile
from random import shuffle

class Deck:
	"""Stores the tiles in the deck."""
	def __init__(self):
		self.tiles = []

	@classmethod
	def from_json(cls, file_name):
		"""Creates a deck from a json file.

		The json file should be a list of objects. Each object should be a
		permutation of the labels {"UL","UR","RU","RD","DR","DR","LD",LU}.
		Objects that are not of this form are omitted.
		"""
		with open(file_name) as file:
			tile_dict_list = json.load(file)
		deck = Deck()
		for tile_dict in tile_dict_list:
			tile = Tile.from_dict(tile_dict)
			if (tile != None):
				deck.tiles.append(tile)
		return deck

	def shuffle(self):
		shuffle(self.tiles)

	def draw(self):
		return self.tiles.pop()

	def add_tile(self, tile):
		self.tile.append(tile)