#
#   A series of static methods used by main()
#

from turn import Turn
import time

# Show the user all commands.
def help():
    print("Actions:")
    print("  `x y`   -> move peg x to hole y")
    print("  `hint`  -> receive a hint")
    print("  `solve` -> show statistics for every possible outcome of this game")
    print("  `names` -> show the names of the holes")
    print("  `help`  -> show this screen")
    print("  `quit`  -> end Peg Game")


# Prompt user for input until no more moves can be made.
#
# board ->  the pegboard
# hints ->  the number of hints available at the start of the game
def ask_for_move(board, hints):

    hints_left = hints  # decremented when the player uses a hint

    help()
    print("Press `Enter` to start your game:")
    input()

    while board.check_possible_moves():

        # show the current state of the board after every action
        print(board)
        if hints_left == 1:
            print("You have 1 hint left")
        else:
            print("You have {} hints left".format(hints_left))
        print("Which peg would you like to move where?")
        args = input_handler(board, "move")

        src = args[0]
        match src:
            case "help":
                help()
            case "hint":
                if hints_left > 0:
                    hint = board.hint(board.pegs_left, None, None)
                    if hint[0] > 2:  # won't win, but print best-case scenario
                        print("Winning is impossible at this point. Best case scenario: {} pegs on the board".format(hint[0]))
                    print("You should move the peg on hole {} to hole {}".format(hint[1].name, hint[2].name))
                    hints_left -= 1 # decrement the number of hints the user has left
                else:
                    print("You don't have any hints left! Good luck the rest of the way")
            case "names":
                print(board.show_names())
            case "quit":
                return -1   # exit early and let main() know that the user wants the application to stop running
            case "solve":
                logs_set = board.solve()
                total = 0
                keys = list(logs_set.keys())
                keys.sort()
                logs_set = { key: logs_set[key] for key in keys }
                for logs in logs_set.values():
                    total += len(logs)
                print("There are {} unique games from this point. Of those games...".format(total))
                for pegs_left, logs in logs_set.items():
                    num_pegs, num_logs = pegs_left, len(logs)
                    out1, out2 = "", ""
                    if num_logs == 1:
                        out1 = "1 game results"
                    else:
                        out1 = "{} games result".format(num_logs)
                    if num_pegs == 1:
                        out2 = "1 peg"
                    else:
                        out2 = "{} pegs".format(num_pegs)
                    print("{} in {} being left on the board. That's a {}% chance.".format(out1, out2, round((num_logs / total) * 100, 2)))
            case _: # user entered invalid input or wants to move a peg
                dest = args[1]
                if (perform_move(board, src, dest)):
                    print(board.log.tail.turn)      # print the turn object in the tail node of the log linked list
                else:
                    print("Invalid move!")
    print(board)    # show the final move
    return hints - hints_left


# Return whether move was successful.
#
# board ->  the pegboard
# src   ->  name of the hole occupied by peg
# dest  ->  name of the empty hole to be jumped to
def perform_move(board, src, dest):
    if (board.hole(src) is not None and board.hole(dest) is not None):
        src_hole, dest_hole = board.hole(src), board.hole(dest)
        if dest_hole in src_hole.adj_holes:
            # try to perform move
            return board.hop_peg(src_hole, src_hole.adj_holes[dest_hole], dest_hole)
    return False


# Return only after valid input has been entered. Does not perform other
#   actions, only checks validity of input.
#
# board         ->  the pegboard
# mode          ->  what the user is being asked to enter
def input_handler(board, mode):
    while 1:    # loop forever until user enters valid input

        args = input().split(" ")
        if args[0] != '':
            match mode:
                # user is asked to make a move or ask for a hint
                case "move":
                    if len(args) == 1:
                        if (
                            args[0] == "hint"   or 
                            args[0] == "help"   or 
                            args[0] == "quit"   or 
                            args[0] == "names"  or
                            args[0] == "solve"
                        ):
                            return args
                    else:
                        if (
                            len(args) == 2 and 
                            len(args[0]) == 1 and 
                            len(args[1]) == 1
                        ):
                            return args
                    print("Invalid move!")
                    print(board)
                    print("Which peg would you like to move where?\n(Psst! Type `help` to see valid actions)")

                # does the user want to play again?
                case "again?":
                    if len(args) == 1 and args[0] == 'y' or args[0] == 'n':
                        return args
                    else:
                        print("Invalid input: input should be 'y' for yes or 'n' for no")
                # number of hints the user would like
                case "num_hints":
                    if (
                        len(args) == 1 and 
                        args[0].isdigit() and
                        int(args[0]) > -1
                    ):
                        return args
                # size of the board (either 15 or 21)
                case "board_size":
                    if (
                        len(args) == 1 and 
                        args[0].isdigit() and
                        (
                        int(args[0]) == 15 or
                        int(args[0]) == 21
                        )
                    ):
                        return args
                    else:
                        print("Invalid pegboard size: pegboard should be either 15 (normal) or 21 (large)")
                # which hole should be empty at the start of the game
                case "starting_hole":
                    if len(args) == 1 and len(args[0]) == 1:
                        if board.hole(args[0]) is not None:
                            return args
                    else:
                        print("Invalid input. Hole names should be among those shown above")


# Ask and return whether the user wants to play Peg Game again.
#
# board ->  the pegboard
def try_again(board):
        print("Play again? (y\\n)")
        return True if input_handler(board, "again?")[0] == 'y' else False
