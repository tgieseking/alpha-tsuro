import pygame

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
        for key in connections_dict.keys():
            if connections_dict[key] == key or connections_dict[connections_dict[key]] != key:
                return None
        tile.connections = connections_dict
        return tile


    def rotate_clockwise(self, turns=1):
        turns = turns % 4
        if turns == 1:
            clockwise = {"UL":"RU", "UR":"RD", "RU":"DR", "RD":"DL",
                         "DR":"LD", "DL":"LU", "LD":"UL", "LU":"UR"}
            new_connections = {}
            for point in self.connections:
                new_connections[clockwise[point]] = clockwise[self.connections[point]]
            self.connections = new_connections
        else:
            for i in range(turns):
                self.rotate_clockwise()

    def draw(self, screen, x, y):
        RED = (150, 0, 0)
        point_coords = {"UL":[x + 10, y], "UR":[x + 30, y], "RU":[x + 40, y + 10], "RD":[x + 40, y + 30],
                         "DR":[x + 30, y + 40], "DL":[x + 10, y + 40], "LD":[x, y + 30], "LU":[x, y + 10]}
        for point in self.connections:
            pygame.draw.line(screen, RED, point_coords[point], point_coords[self.connections[point]], 2)