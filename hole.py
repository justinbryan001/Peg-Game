#
# Encapsulation of a hole on a pegboard.
#
class Hole:


    # Meant to be called by `triangle()` or any other function that returns a 
    # pegboard. 
    #
    # name      ->      the hole name. Meant to be a single char from `a` 
    #                       onwards. More info on this can be found in the 
    #                       documentation for board.py
    # has_peg   ->  whether the whole is currently occupied by a peg
    # adj_holes ->  dictionary of every legal move possible from this hole
    def __init__(self, name):
        self.name = name
        self.has_peg = True
        self.adj_holes = dict()


    def __str__(self):
        result = "Hole {}. Has peg = {}\nAdjacent holes:\n".format(self.name, self.has_peg)
        
        if self.adj_holes:
            for j, i in self.adj_holes.items():
                result += "Hole i: {} Hole j: {}\n".format(i.name, j.name) 
        return result


    # Add hole `i` to the adj_holes dictionary, using hole `j` as the key. 
    # Then, do the same thing in reverse with hole `j`. Hole `i` is the hole 
    # between hole `self` and hole `j`.  Do not check that the holes make sense 
    # being next to each other, as that is the job of `triangle()` or functions 
    # like it that return a board.
    #
    # i     ->  the peg in `self` would hop over this hole
    # j     ->  the peg in `self` would land in this hole
    def add_hole(self, i, j):
        self.adj_holes[j] = i
        j.adj_holes[self] = i

