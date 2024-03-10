import sys
import random
import time
import math


# Find the number of pairs of attacking queens
def get_num_conflict(queen_array):
    num_conflict = 0
    num_queens = len(queen_array)
    for i in range(num_queens): # Loop through each queen checking it against each other queen
        for j in range(i+1, num_queens):
            if queen_array[i] == queen_array[j]: # If they are in the same column they are attacking
                num_conflict += 1
            elif abs(queen_array[i] - queen_array[j]) == abs(i-j): # If they are on a diagonal they are attacking
                num_conflict += 1
            # Don't have to check for same row since they cannot be by the way we have set this up
    return num_conflict

# Print the board
def print_board(queen_array):
    num_queens = len(queen_array)
    print("+" + "-"*(num_queens) + "+") # Print top
    for location in queen_array:
        print("|" + "."*(location) + "Q" + "."*(num_queens-location-1) + "|") # Print queens
    print("+" + "-"*(num_queens) + "+") # Print bottom


# Initialize board randomly but with no overlap
def initialize(num_queens):

    # Fill with -1 to mean not set yet
    queens = [-1] * num_queens

    # For each queen
    for row in range(num_queens):
        while True: # Loop until you are in a unique column
            col = random.randint(0, num_queens-1) # Generate a random column
            if col not in queens[:row]: # If no other queen before it is in that column
                queens[row] = col # Set its location and break the loop
                break
    return queens



# Solve the board with simulated annealing. Temperature cools very slowly because there are a ton of iterations
# Tried to make another program that optimizes the values but it would take way too long to get any meaningful numbers
def simulated_annealing(num_queens, initial_temperature=1000, cooling_rate=0.99):
    # Initialize variables
    current_board = initialize(num_queens)
    current_conflicts = get_num_conflict(current_board)
    best_board = current_board
    best_conflicts = current_conflicts
    temperature = initial_temperature
    max_iterations = 100000000
    iteration = 0

    # Loop until a solution has been found or you've gone an insane number of iterations to avoid infinite loop
    while (iteration < max_iterations):
        # Increment iteration
        iteration += 1

        # Generate a neighbor
        neighbor = current_board.copy() # Start with a copy of the current board
        row_to_move = random.randint(0, num_queens - 1) # Choose a random row to move
        new_col = random.randint(0, num_queens - 1) # Choose a random column to move that row to
        neighbor[row_to_move] = new_col # Do the move
        neighbor_conflicts = get_num_conflict(neighbor) # Get number of queens in conflict for the neighboring board

        # Calculate change in conflicts
        cost_change = neighbor_conflicts - current_conflicts


        # Accept the neighbor if it's a better solution or randomly depending on temperature result
        # The larger the temp result the more likely to choose a "bad" solution.
        # We use e^-x because that is guaranteed to give a number between 0 and 1 (assuming x is positive)
        # -cost change / temperature because it relates the number to how different the neighbor and current board are
        # The more similar the boards are, the more likely it is that we will accept the worse board
        # Still had to relate it to temperature though, hence the / temperature
        if (cost_change < 0 or random.random() < math.exp(-cost_change / temperature)):
            current_board = neighbor
            current_conflicts = neighbor_conflicts
            print(current_board)

            # Update the best solution if possible
            if neighbor_conflicts < best_conflicts:
                best_board = neighbor
                best_conflicts = neighbor_conflicts

            # If a solution has been found, return it
            if best_conflicts == 0:
                return best_board

        # Reduce the temperature by a factor of the cooling rate to choose less "bad"/random as time goes on
        temperature *= cooling_rate

    # If you somehow run out of iterations just return what you have
    return best_board
    
    


# Main
if __name__ == "__main__":
    # Start timer
    start_time = time.time()

    # Set variables
    num_queens = int(sys.argv[1])
    # temperature = int(sys.argv[2])
    # cooling_rate = float(sys.argv[3])

    # Solve
    queens = simulated_annealing(num_queens)

    # End timer
    end_time = time.time()

    # Calculate total time
    total_time = round(end_time-start_time, 1)

    # Print solution
    print("Solution:")
    print_board(queens)
    print(f"Took {total_time} seconds or {round(total_time/60, 4)} minutes.")
    print(f"The final board was: {queens}")
    # print(total_time)


#[32, 92, 37, 129, 163, 52, 137, 191, 98, 122, 178, 93, 48, 13, 157, 94, 180, 18, 20, 108, 27, 66, 80, 138, 109, 147, 29, 90, 62, 71, 44, 151, 91, 117, 14, 184, 1, 174, 50, 196, 111, 133, 107, 142, 85, 141, 198, 63, 156, 33, 25, 162, 42, 45, 171, 21, 81, 143, 152, 194, 68, 17, 164, 188, 35, 6, 97, 73, 149, 197, 132, 8, 83, 43, 135, 51, 104, 126, 192, 195, 65, 96, 39, 189, 130, 59, 150, 106, 140, 7, 2, 115, 26, 72, 166, 172, 15, 28, 167, 82, 173, 158, 56, 112, 159, 185, 146, 34, 89, 4, 49, 41, 182, 57, 124, 53, 121, 22, 136, 179, 67, 187, 99, 190, 199, 120, 69, 170, 181, 54, 116, 76, 123, 46, 23, 186, 95, 131, 70, 176, 153, 128, 165, 169, 148, 175, 88, 47, 30, 5, 16, 79, 12, 36, 102, 177, 119, 154, 11, 31, 127, 134, 77, 87, 113, 118, 10, 38, 74, 168, 3, 160, 60, 161, 114, 0, 193, 139, 101, 125, 61, 110, 75, 103, 64, 55, 78, 183, 24, 144, 86, 58, 9, 40, 155, 145, 100, 84, 105, 19]