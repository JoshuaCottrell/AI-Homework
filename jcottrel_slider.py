#!/usr/bin/env python3

'''
CPSC 415 -- Homework #2.667 template
Stephen Davies, University of Mary Washington, fall 2023
'''

from puzzle import Puzzle
import numpy as np
import sys
from copy import deepcopy


# Works
def h1(p):
    grid = p.grid
    solved_grid = Puzzle(n).grid
    tiles_out_of_place = 0
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] != solved_grid[x][y]:
                tiles_out_of_place += 1
    return tiles_out_of_place

def insert_into_frontier(frontier, frontierEstimates, move_sequence, estimated_cost):
    new_best = False
    index = 0
    for node in frontier:
        if frontierEstimates[node] > estimated_cost:
            frontier.insert(index, move_sequence)
            new_best = True
            break
        index += 1
    if not new_best:
        frontier.append(move_sequence)
    
    return
        


def solve(p):
    frontier = [()]
    frontierEstimates = {():0}
    frontierPuzzles = {():deepcopy(p)}

    while(1):
        # Remove the first node of the frontier for expansion
        expand_node = frontier.pop(0)
        # Get the puzzle corresponding to this node
        expand_puzzle = deepcopy(p)
        for move in expand_node:
            expand_puzzle.move(move)
        # Get the estimate for this node
        frontierEstimates[expand_node] = h1(expand_puzzle)
        # Check if it is solved
        if expand_puzzle.is_solved():
            return expand_node
        # If not solved, ask for all possible legal moves
        legal_moves = expand_puzzle.legal_moves()
        for legal_move in legal_moves:
            temp_puzzle = deepcopy(expand_puzzle)
            temp_puzzle.move(legal_move)
            temp_estimate = h1(temp_puzzle)
            if temp_puzzle not in frontierPuzzles.values():
                moves = expand_node + (legal_move,)
                frontierEstimates[moves] = temp_estimate
                frontierPuzzles[moves] = temp_puzzle
                insert_into_frontier(frontier, frontierEstimates, moves, temp_estimate)

        



        #Get heuristic value for the node (i.e. if we do this move sequence, what is the heuristic value after)

    # print(f"Tiles out of place: {h1(p)}")
    # return ["D","U","L","L"]



if __name__ == '__main__':

    if (len(sys.argv) not in [2,3]  or
        not sys.argv[1].isnumeric()  or
        len(sys.argv) == 3 and not sys.argv[2].startswith("seed=")):
        sys.exit("Usage: puzzle.py dimensionOfPuzzle [seed=###].")

    n = int(sys.argv[1])

    if len(sys.argv) == 3:
        seed = int(sys.argv[2][5:])
    else:
        seed = 120

    # Create a random puzzle of the appropriate size and solve it.
    puzzle = Puzzle.gen_random_puzzle(n, seed)
    print(puzzle)
    solution = solve(puzzle)
    if puzzle.has_solution(solution):
        input("Yay, this puzzle is solved! Press Enter to watch.")
        puzzle.verify_visually(solution)
    else:
        print(f"Sorry, {''.join(solution)} does not solve this puzzle.")
