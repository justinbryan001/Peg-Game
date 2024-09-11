#
# Driver for the Peg Game
#

# FUTURE CONTENT
# TODO: Implement a peg solitaire mode (rectangle) and the choice to play 
#           either that or the existing triangular mode.
#       Find some useful application for playback of a peg game, something that 
#           is already possible but not available to the user.
#       Experiment with bidirectional DFS instead of the existing DFS

from board import *
from turn import Turn
import interface

def main():

    again = True  # player wants to play again (will always play 1 or more times)
    while again:
        
        print("Welcome to Peg Game!")
        print("How many hints would you like?")
        hints = int(interface.input_handler(None, "num_hints")[0])
        
        board = None
        while board is None:
            print("Would you like a 15 or 21-peg board? (15 - normal, 21 - large)")
            size = int(interface.input_handler(board, "board_size")[0])
            if size == 21:
                print("Warning: the `solve` command with this board size is too slow to be feasible.")
                print("It is not recommended that you use this command early-game.")
                print("Press the `Enter` key to proceed at your own risk.")
                input()
            # initialize the peg board, determining which holes are adjacent to each other
            board = triangle(size)

        print("There are {} pegs and {} holes".format(board.pegs_left, board.size))
        
        # allow user to select starting peg
        print(board.show_names())
        print("Choose a hole to be the empty one")
        start = interface.input_handler(board, "starting_hole")[0]

        print("You chose hole {}!".format(start))
        board.hole(start).has_peg = False

        # query user input. ask_for_move() will only return when game is over
        hints_used = interface.ask_for_move(board, hints)

        # user typed `quit` - program stops running
        if hints_used == -1:
            return

        # game is over. display results
        print("You left {} pegs on the board".format(board.pegs_left))

        match board.pegs_left:
            case 1:
                print("You're genius")
            case 2:
                print("You're purty smart")
            case 3:
                print("You're just plain dumb")
            case _:
                print("You're just *eg-no-ra-moose*")
        
        print("You used {} hints".format(hints_used))
        if hints_used == 0:
            print("Great work!")

        again = interface.try_again(board) # ask the user to try again, quit if no


if __name__ == "__main__":
    main()
