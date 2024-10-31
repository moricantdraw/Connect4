# Source: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode
# fail-hard implementation

# Import necessary modules
import math
import random
from evaluate_game_state import evaluate_game_state
from alternate_game_state import alternative_gamestate

# Set constants
EMPTY_VALUE = 0
TREE = [5, 6, 4, 69, 3, 70, 71, 72, 6, 42, 6, 420, 7, 101, 102, 103]
RESULT = dict()
progress = 0

# Function that choses the optimal move using alpha-beta minimax
def alpha_beta_minimax(current_state, depth, maximizing_player, alpha, beta):
    '''
    Perform alpha-beta pruning with minimax algorithm and evaluate the optimal 
    move for the player

    Parameters:
        current_state: list representing the current state of the board
        depth: int representing depth of search in the game tree 
        maximizing_player: bool representing if the current player is the 
        maximizer
        alpha: best score maximizing player can guaruntee
        beta: best score minimizing player can guaruntee

    Returns:
        Tuple representing best possible move
    '''
    global progress

    if depth == 0:  # or EMPTY_VALUE not in current_state:
        value = state_value(current_state)
        ret_val = (value, 0)
        progress += 1
        RESULT[depth] = RESULT.get(depth, []) + [ret_val]
        return ret_val
    
    # Maximizing Player
    if maximizing_player:
        value = -math.inf # Set lowest possible score for maximizer
        column = None
        for col in range(7): # loop through columns
            next_state = get_next_state(current_state, col, maximizing_player)
            if next_state is not None:
                temp = alpha_beta_minimax(next_state, depth - 1, False, alpha, beta)
                if ( 
                    temp[0] > value # Choose move if score is higher
                ):  # or (abs(temp[0] - value) < 0.01 and round(random.random())):
                    value = temp[0]
                    column = col
                if value > beta:
                    break
                alpha = max(alpha, value)
        ret_val = (value, column) # Return best score and column for maximizer
        RESULT[depth] = RESULT.get(depth, []) + [ret_val]
        return ret_val
    
    # Minimizing player
    else:
        value = math.inf # Set highest possible score for minimizer
        column = None
        for col in range(7): # loop through columns
            next_state = get_next_state(current_state, col, maximizing_player)
            if next_state is not None:
                temp = alpha_beta_minimax(next_state, depth - 1, True, alpha, beta)
                if (
                    temp[0] < value # Choose move if score is lower
                ):  # or (abs(temp[0] - value) < 0.01 and round(random.random())):
                    value = temp[0]
                    column = col
                if value < alpha:
                    break
                beta = min(beta, value)
        ret_val = (value, column) # Return best score and column for minimizer
        RESULT[depth] = RESULT.get(depth, []) + [ret_val]
        return ret_val


# Check progress
def get_progress():
    global progress
    return progress


# Reset progress for another cycle
def reset_progress():
    global progress
    progress = 0


# Evaluate the current game state
def state_value(state):
    return evaluate_game_state(state)


# Get the next board state based on a given move in a column
def get_next_state(current_state, col, maximizing_player):
    if maximizing_player:
        player = 2
    else:
        player = 1
    return alternative_gamestate(current_state, col, player)


# Print minimax tree of scores
def print_tree(tree):
    for key in sorted(tree.keys(), reverse=True):
        print(f"Depth {key}, {tree[key]}")


# TESTING

# fmt: off
# test_state = [
#     0,0,0,0,0,0,0,
#     0,0,0,2,0,0,0,
#     0,0,1,2,0,0,0,
#     0,0,1,2,0,0,0,
#     0,2,1,1,1,0,0,
#     1,2,2,2,1,0,0,
# ] # column 3
# test_state = [
#     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0,
#     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0,
#     0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0,
#     0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0,
#     2.0, 2.0, 1.0, 1.0, 0.0, 0.0, 0,
#     1.0, 2.0, 2.0, 2.0, 1.0, 0.0, 0,
# ] # column 2
# test_state = [
#     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0,
#     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0,
#     0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0,
#     2.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0,
#     2.0, 2.0, 1.0, 1.0, 0.0, 0.0, 0,
#     1.0, 2.0, 2.0, 2.0, 1.0, 0.0, 0,
# ] # column 2
# test_state = [
#     1.0, 0.0, 0.0, 2.0, 1.0, 2.0, 0.0,
#     1.0, 0.0, 0.0, 1.0, 2.0, 1.0, 0.0,
#     2.0, 0.0, 0.0, 2.0, 2.0, 2.0, 0.0,
#     1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0,
#     2.0, 2.0, 0.0, 1.0, 2.0, 2.0, 0.0,
#     2.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0,
# ] # column 1
# test_state = [
#     0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0,
#     0.0, 1.0, 2.0, 2.0, 1.0, 0.0, 0.0,
#     2.0, 2.0, 2.0, 1.0, 1.0, 0.0, 0.0,
#     2.0, 1.0, 2.0, 2.0, 2.0, 0.0, 0.0,
#     1.0, 2.0, 1.0, 1.0, 1.0, 0.0, 0.0,
#     2.0, 1.0, 2.0, 2.0, 1.0, 0.0, 0.0,
# ] # column 4
test_state = [
    2.0, 2.0, 1.0, 1.0, 1.0, 0.0, 0.0,
    2.0, 1.0, 1.0, 1.0, 2.0, 0.0, 0.0,
    1.0, 2.0, 2.0, 2.0, 1.0, 1.0, 0.0,
    2.0, 2.0, 1.0, 1.0, 2.0, 2.0, 1.0,
    2.0, 1.0, 2.0, 2.0, 1.0, 1.0, 2.0,
    1.0, 2.0, 1.0, 1.0, 2.0, 2.0, 1.0,
]
# fmt: on

# final = alpha_beta_minimax(test_state, 4, True, -math.inf, math.inf)
# print(final)
# print_tree(RESULT)
