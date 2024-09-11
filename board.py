#
# An encapsulation of a pegboard. Only one pegboard is instantiated per game
#

from hole import Hole
from turn import Log, Node, Turn

class Board:


    # Constructor: Relies on static method triangle() to feed it the correct inputs
    #
    # holes     ->  An array of the holes of the board, already given proper 
    #                   adjacencies. Storing holes this way keeps iteration 
    #                   simple. Holes should be named starting from ASCII 'a', 
    #                   because that guarantees array lookups happen in 
    #                   constant time.
    # size      ->  len(holes) set as a class attribute during initialization 
    #                   for convenience.
    # num_rows  ->  Can be derived from hole size, also calculated ahead of 
    #                   time for convenience.
    # pegs_left ->  Keep track of progress through the game, decremented 
    #                   whenever the player makes a move.
    # log       ->  Doubly-linked list containing every turn made so far. Meant
    #                   for playback of a game and to enable recursive "solver" 
    #                   and "hint-giver" functions
    def __init__(self, holes, size, num_rows):
        self.holes = holes
        self.size = size
        self.num_rows = num_rows
        self.pegs_left = self.size - 1
        self.log = Log()


    # A getter for holes. Hides ugly code from the method caller
    # 
    # name  ->  char containing the name of the hole
    def hole(self, name):
        if (name is None or
            len(name) > 1 or 
            ord(name) - 97 >= self.size or
            ord(name) <= 96
        ):
            return None
        
        return self.holes[ord(name) - 97]


    # Visualize the occupation of pegs on the board.
    def __str__(self):
        return self.show_board(list(map(lambda hole: "\u257F" if hole.has_peg else "\u25CB", self.holes)))


    # Visualize the names of each hole on the board.
    def show_names(self):
        return self.show_board(list(map(lambda hole: hole.name, self.holes)))


    # Helper method for __str__ and show_names.
    # Print the array in the shape of a triangular pegboard
    # leave the decision-making regarding what to print to the other
    # methods.
    # 
    # arr   ->  Array of values to print
    def show_board(self, arr):
        result = ""
        num, i = 0, 0
        while num < len(arr):
            for _ in range(self.num_rows - i):
                result += " "
            for j in range(num, num + i + 1):
                result += "{} ".format(arr[j])
            result += "\n"
            num += i + 1
            i += 1
        return result[:-1]  # remove the last newline


    # Return whether a move is possible after this one. Used to determine
    # whether the game should end and results should be displayed.
    def check_possible_moves(self):
        for h in self.holes:
            if h.has_peg:
                for j, i in h.adj_holes.items():
                    # is a hop from hole h over hole i to hole j possible?
                    if self.hop_peg(h, i, j):
                        self.rewind()
                        return True
        return False


    # Find 1 move that could lead to a win (1 peg left) and return the move to 
    # the user. If no win is possible, find move which could lead to the least
    # amount of pegs left on the board on game completion.
    #
    # best_case ->  A "best-case scenario" number of pegs left on the board
    # l         ->  The hole from which the player should move the peg
    # m         ->  The hole to which the player should move the peg
    def hint(self, best_case, l, m):
        best_case = self.pegs_left  # save best-case scenario in case there a
        # base case (if won, return)
        if self.win():
            return [best_case, l, m]
        for h in self.holes:
            if h.has_peg:
                for j, i in h.adj_holes.items():
                    if self.hop_peg(h, i, j):
                        if self.pegs_left < best_case:
                            best_case = self.pegs_left
                        l, m = h, j
                        result = self.hint(best_case, l, m)
                        if result[0] < best_case:
                            best_case = result[0]
                        self.rewind()
                        # if win state, exit loop early. We're done
                        if best_case == 1:
                            return [best_case, h, j]
                        else:
                            if result[0] < best_case:
                                l, m = h, j
        return [best_case, l, m] # winning is not possible if reached this point


    # Return a dictionary of log objects, each one representing a unique 
    # outcome of this game, organized by the number of pegs left at the end of 
    # the game. Used by `solve` to display statistics about the current state 
    # of the game. If someone wanted to implement this feature, it would be 
    # possible to replay each outcome turn-by-turn using the return value of
    # this function. 
    def solve(self):

        # number of games possible with x amount of pegs left
        # compromising space for performance
        logs = dict()

        # base case: if game is over, return pegs_left
        if not self.check_possible_moves():
            if self.pegs_left in logs:
                logs[self.pegs_left] += [self.log]
            else:
                logs[self.pegs_left] = [self.log] 
            return logs

        for h in self.holes:
            if h.has_peg:
                for j, i in h.adj_holes.items():
                    if self.hop_peg(h, i, j):
                        solve = self.solve()
                        for key, item in solve.items():
                            if key in logs:
                                logs[key] += item
                            else:
                                logs[key] = item
                        self.rewind()
        return logs


    # Check to see if the player won the game
    def win(self):
        return self.pegs_left == 1


    # Return whether peg on hole h successfully hopped over peg on hole i into 
    # hole j. Does not do anything if the maneuver is not possible.
    #
    # h ->  hole containing peg that hops
    # i ->  hole with peg to be hopped over
    # j ->  hole in which the peg will enter
    def hop_peg(self, h, i, j):

        # should not get here!
        if h is None or i is None or j is None:
            raise "ERROR: hop_peg() was passed a null peg!"

        # check whether holes meet criteria for a hop
        if h.has_peg == False or i.has_peg == False or j.has_peg:
            return False

        # all criteria is met - hop is successful
        h.has_peg = False
        i.has_peg = False
        j.has_peg = True
        self.pegs_left -= 1
        self.log.add(Turn(h, i, j, self.holes)) # record turn
        return True


    # Set the board to the state it was in on the previous turn. Used for
    # recursive "hint generators" and "solvers".
    def rewind(self):
        turn = self.log.pop()              # "pops" the last turn off Log
        if turn is not None:    
            turn.h.has_peg = True   
            turn.i.has_peg = True
            turn.j.has_peg = False
            self.pegs_left += 1


# ---------------------------------
# STATIC FUNCTIONS BEYOND THIS POINT
# ---------------------------------


# Return a triangular pegboard of a given size (recommended 15 or 21).
# Feed the proper inputs into the constructor. The user should not call the
# constructor directly, instead using this function or others like it to
# generate the pegboard.
#
# size  ->  Size of the to-be pegboard. Will be checked for validity
def triangle(size):

    # Initialize set N(n) = N(n - 1) + n, with  N(0) = 0 and N(n) < `size`
    # (Example: [0, 1, 3, 6, 10] with `size` = 15)
    # In other words, calculate valid sizes for trianglular board, and the 
    # indexes at which a new row begins
    nums = []
    num, i = 0, 0
    while num < size:
        nums.append(num)
        num += i + 1
        i += 1

    # check that size given forms a perfect triangular board
    if num > size or size < 10 or size > 160:
        print("Invalid pegboard size")
        return None  # will ask for size again if the one given is invalid

    # array of holes, names in ascending order from ASCII lowercase a
    holes = []
    for i in range(size):
        holes.append(Hole(chr(97 + i)))

    # handle adjacencies - each iteration does this for one row
    # will only add valid moves to avoid unnecessary checks
    for new_left, old_left in zip(nums[1:], nums):
        right = 2 * new_left - old_left
        row_size = 1 + new_left - old_left
        if new_left > 1:
            # leftmost hole in a given row
            holes[new_left].add_hole(holes[old_left], holes[new_left - 2 * row_size + 3])
            # rightmost holes in a given row
            holes[right].add_hole(holes[new_left - 1], holes[old_left - 1])
            holes[right].add_hole(holes[right - 1], holes[right - 2])
        # holes in the center
        # k = index of current hole
        for k in range(new_left + 1, right):
            # size of the new row
            if new_left > 3:
                if k > new_left + 1:
                    holes[k].add_hole(holes[k - row_size], holes[k - 2 * row_size + 1])
                    holes[k].add_hole(holes[k - 1], holes[k - 2])
                if k < right - 1:
                    holes[k].add_hole(holes[k - row_size + 1], holes[k - 2 * row_size + 3])
    return Board(holes, size, len(nums))
