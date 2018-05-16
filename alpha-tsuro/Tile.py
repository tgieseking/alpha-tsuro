class Tile:
	"""A single tile.

	Each tile has eight points on its border where its paths terminate.
	These points are arranged as follows
            UL    UR
	    -----|----|-----
	    |              |
	  LU-              -RU
	    |              |
	  LD-              -RD
	    |              |
	    -----|----|-----
	        DL    DR
	The connections dict maps each point to where the path starting at the
	point ends.
	"""
	def __init__(self):
		self.connections = {"UL":None, "UR":None, "RU":None, "RD":None,
							"DR":None, "DL":None, "LD":None, "LU":None}

	@classmethod
	def from_dict(cls, connections_dict):
		"""Creates a file from a dict of the connections.

		If the dict is a permutation of the points, then the corresponding
		tile is returned. Otherwise, None is returned.
		"""
		tile = Tile()
		try:
			if (set(tile.connections.keys()) != set(connections_dict.keys()) or
				set(tile.connections.keys()) != set(connections_dict.values())):
				return None
		except AttributeError:
			return None
		tile.connections = connections_dict
		return tile