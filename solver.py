#! /usr/bin/python

import sys
import logging
from copy import deepcopy

def create_puzzle(filename):
    ret = None
    with open(filename) as f:
        for line in f:
            for x in line.split(","):
                value = int(x)
                if ret is None:
                    ret = [value]
                else:
                    ret.append(value)
    return ret

def print_matrix(boxes):
    if len(boxes) == 81:
        for x in range(0, 72, 9):
            for y in range(x, x+9):
                logging.debug("Printing position {0} value {1}".format(y, boxes[y]))
                print boxes[y],
            print
        print
    else:
        logging.error("Not a full matrix: {0}".format(boxes))


def solve(boxes):
    """
    Takes a collection of 81 integers representing the puzzle
    with zeros in place of unknown values.  Returns a collection
    all possible solutions to this puzzle.
    """
    logging.debug("Solving: {0}".format(boxes))
    #Build row, column, and box collections
    rows = [set([0]) for x in range(0, 9)]
    columns = [set([0]) for x in range(0, 9)]
    squares = [set([0]) for x in range(0, 9)]
    #Iterate through all values filling collections
    for x in range(0, len(boxes)):
        (row, column, square) = find_sets(x)
        rows[row].add(boxes[x])
        columns[column].add(boxes[x])
        squares[square].add(boxes[x])
    #While something has changed:
        #Iterate through all boxes
        #Take the difference of the appropriate row, column, and box values
        #Assign value if only one is possible
    changed = True
    #while something has changed
    while changed:
        changed = False
        #iterate through all records
        for x in range(0, len(boxes)):
            if boxes[x] == 0:
                #trying to assigned based on available values
                found = try_assign(boxes, x, rows, columns, squares)
                #if assigned keep going
                if found is not None:
                    changed = True
    #figure out if this is a solved
    first_zero = None
    for x in range(0, len(boxes)):
        logging.debug("Boxes check for 0: {0}".format(boxes[x]))
        if boxes[x] == 0:
            first_zero = x
            break
    if first_zero is None:
        return [boxes]
    else:
        return try_guess(boxes, first_zero, rows, columns, squares)

def find_sets(x):
    row = x / 9
    column = x % 9
    square = (column / 3) + ((row / 3) * 3)
    return (row, column, square)

def try_assign(boxes, position, rows, columns, squares):
    (r, c, s) = find_sets(position)
    options = set(range(1,10))
    row = rows[r]
    column = columns[c]
    square = squares[s]
    possible = options.difference(row.union(column.union(square)))
    if len(possible) == 1:
        found = possible.pop()
        boxes[position] = found
        row.add(found)
        column.add(found)
        square.add(found)
        return found
    else:
        return None

def try_guess(boxes, position, rows, columns, squares):
    logging.debug("Guessing: {0}".format(boxes))
    logging.debug("Position: {0}".format(position))
    ret = None
    (r, c, s) = find_sets(position)
    options = set(range(1,10))
    row = rows[r]
    column = columns[c]
    square = squares[s]
    possible = options.difference(row.union(column.union(square)))
    logging.debug("Possible options: {0}".format(possible))
    for possibility in possible:
        logging.info("Guessing {0} for position {1}".format(possibility, position))
        boxes_copy = deepcopy(boxes)
        boxes_copy[position] = possibility
        solution = solve(boxes_copy)
        if solution is not None:
            if ret is None:
                ret = []
            ret = ret + solution
    return ret
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        puzzle = create_puzzle(filename)
        print 'Starting with puzzle:'
        print
        print_matrix(puzzle)
        results = solve(puzzle)
        if results is None:
            print 'No solution for this puzzle'
        elif len(results) == 1:
            print 'One result found:'
            print
            result = results[0]
            print_matrix(result)
        else:
            print 'Multiple solutions found:'
            print
            for result in results:
                print_matrix(result)
    else:
        print 'Usage: ./solver <filename>'
