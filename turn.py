#
# An implementation of a doubly-linked list. Contains every move made since the
#   start of the game. As such, it could be used to "play back" a game,
#   starting from the head.
#
class Log:

    # head  ->  head of a doubly-linked list, the start of the game
    # tail  ->  tail of a doubly linked list, the last move made
    def __init__(self):
        self.head = None
        self.tail = None


    # Add a new node containing the latest turn to this log.
    #
    # turn  ->  the turn being added
    def add(self, turn):
        new_node = Node(turn)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node


    # Remove and return the last turn (not the node) of the list. Used to undo
    # a turn.
    def pop(self):

        # empty list
        if self.tail is None:
            return None

        last_turn = self.tail.turn
        self.tail = self.tail.prev

        # removed first turn
        if self.tail is None:
            self.head = None

        self.tail.next = None

        return last_turn


#
# A simple node encapsulation for a doubly-linked list. Contains a Turn object.
#
class Node:


    # turn  ->  the data - a turn object as specified below
    # next  ->  another node
    # prev  ->  the preceding node
    def __init__(self, turn):
        self.turn = turn
        self.next = None
        self.prev = None

#
# Encapsulation of a single move.
#
class Turn:


    # h ->  the hole from which the peg was moved
    # i ->  the hole that was hopped over
    # j ->  the hole the peg was moved to
    # s ->  array representing the current state of the board
    def __init__(self, h, i, j, s):
        self.h = h
        self.i = i
        self.j = j
        self.s = list(map(lambda hole: "\u257F" if hole.has_peg else "\u25CB", s))


    def __str__(self):
        return "Peg {} jumps over peg {} into hole {}".format(self.h.name, self.i.name, self.j.name)
