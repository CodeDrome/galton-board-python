import math
from random import choice
import time

GREEN = "\x1B[94m"
RESET = "\x1B[0m"

class GaltonBoard(object):

    """
    Implements the logic of a Galton Board.

    No UI is provided in this class,
    instead 3 functions are provided as arguments to init
    which are called by the class whenever anything happens which
    requires a UI update.
    """

    def __init__(self, rowcount = 7, ballcount = 40, on_init = None, on_ball_moved = None, on_total_changed = None):

        """
        Simply set the attributes of the class from init arguments or to defaults
        """

        self.board = []
        self.rowcount = rowcount
        self.ballcount = ballcount
        self.totals = []
        self.gridrows = 0
        self.gridcolumns = 0
        self.ballx = 0
        self.bally = 0
        self.prevballx = 0
        self.prevbally = 0
        self.pause_ms = 100
        self.on_init = on_init
        self.on_ball_moved = on_ball_moved
        self.on_total_changed = on_total_changed

    def initialize(self):

        """
        Initializes the data structure to represent the Galton board
        """

        # need to allow for spaces between pegs and a larger space above the pegs for balls to drop
        self.gridrows = ((self.rowcount * 2) - 1) + 3
        self.gridcolumns = (self.rowcount * 2) + 1

        rowpegcount = 1
        pegsdrawn = 0
        # this centres the top peg horixontally
        firstpegx = math.floor(self.gridcolumns / 2)
        pegx = firstpegx
        pegy = 3

        # create a list for totals of the necessary size
        self.totals = [0] * (self.rowcount + 1)
        self.prevballx = -1
        self.prevbally = -1

        # create 2D array of pegs using letter 'O' to indicate a peg
        for r in range(0, self.gridrows):

            self.board.append(['*'] * self.gridcolumns)

            for c in range(0, self.gridcolumns):

                if r == pegy and c == pegx and pegsdrawn < rowpegcount:
                    self.board[r][c] = 'O'
                    pegsdrawn+=1
                    pegx+= 2
                else:
                    self.board[r][c] = ' '

            if r > 2 and (r%2) == 0:
                rowpegcount+=1
                pegsdrawn = 0
                firstpegx-=1
                pegx = firstpegx
                pegy+= 2

        # don't forget to call the function to tell the UI to draw the new board
        if self.on_init:
            self.on_init(self)

    def start(self):
        
        """
        Sets the board running in a big loop for the specified number of balls
        """

        for b in range(1, self.ballcount + 1):

            # set ball horizontal position to centre
            self.ballx = math.floor(self.gridcolumns / 2)

            for r in range(0, self.gridrows):

                self.bally = r

                # if we hit a peg move left or right
                if self.board[r][self.ballx] == 'O':
                    self.ballx += choice([-1, 1])

                if self.on_ball_moved:
                    self.on_ball_moved(self)

                self.prevballx = self.ballx
                self.prevbally = self.bally

                if r < (self.gridrows - 1):
                    time.sleep(self.pause_ms/1000)

            # calculate index of totals for current ball position
            if self.ballx == 0:
                totalindex = 0
            else:
                totalindex = int(self.ballx / 2)

            self.totals[totalindex] += 1

            if self.on_total_changed:
                self.on_total_changed(self, totalindex, b);
