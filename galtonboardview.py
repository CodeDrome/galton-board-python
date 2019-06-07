import os
import math
import sys
import time

# ANSI terminal colour codes
RED = "\x1B[91m"
GREEN = "\x1B[92m"
RESET = "\x1B[0m"

X_OFFSET = 2
Y_OFFSET = 6

def __clear_screen():

    """
    Hopefully this is cross-platform enough: no guarantees!
    """

    os.system('cls' if os.name=='nt' else 'clear')

def __gotoxy(x, y):

    """
    Uses ANSI terminal codes to move cursor
    """

    print("%c[%d;%d%s" % (0x1B, y, x, "H"), end="")
    sys.stdout.flush()

def on_init(gb):

    """
    To be called by a GaltonBoard object when the board has first been created

    Just draws an empty board
    """

    __clear_screen()

    print("-----------------")
    print("| codedrome.com |")
    print("| Galton Board  |")
    print("-----------------\n")

    for r in range(0, gb.gridrows):

        print(' ', end="");

        for c in range(0, gb.gridcolumns):
            print(gb.board[r][c], end="")

        print("")

    print("")

    # draw buckets
    for r in range(0, 16):

        for c in range(0, gb.rowcount + 2):
            print(GREEN + "| " + RESET, end="")

        print(GREEN + "%d" % abs(r - 16) + RESET)

def on_ball_moved(gb):

    """
    Called by GaltonBoard object when ball moves.
    """

    # delete ball if it has a previous position
    if gb.prevballx >= 0 and gb.prevbally >= 0:
        __gotoxy(gb.prevballx + X_OFFSET, gb.prevbally + Y_OFFSET)
        print(" ")

    # draw ball in new position
    __gotoxy(gb.ballx + X_OFFSET, gb.bally + Y_OFFSET)
    print(RED + "o" + RESET, end="")
    sys.stdout.flush()

def on_total_changed(gb, index, count):

    """
    Called by GaltonBoard object when total changes.
    """

    bottom_of_bucket = 4 + gb.gridrows + 19

    if index == 0:
        bucketx = 2
    else:
        bucketx = (index + 1) * 2

    # animate ball into bucket
    starty = bottom_of_bucket - 17
    end_y = bottom_of_bucket - gb.totals[index]

    for y in range(starty, end_y + 1):

        time.sleep(gb.pause_ms/1000)

        __gotoxy(bucketx, y-1)
        print(" ")
        sys.stdout.flush()

        __gotoxy(bucketx, y)
        print(RED + "o" + RESET)
        sys.stdout.flush()

    # show totals vertically
    total_y = bottom_of_bucket + 1
    total_x = 2

    for t in range(0, gb.rowcount + 1):

        totalstr = str(gb.totals[t])

        for c in range(0, len(totalstr)):
            __gotoxy(total_x, total_y + c)
            print("%c" % totalstr[c])
            sys.stdout.flush()

        total_x += 2

    # show ball count
    __gotoxy(2, bottom_of_bucket + 4)
    print("Ball %d of %d" % (count, gb.ballcount))
    sys.stdout.flush()
