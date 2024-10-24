# https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode
# fail-hard implementation
import math
from evaluate_game_state import evaluate_game_state
from alternate_game_state import alternative_gamestate  # , game_state

EMPTY_VALUE = 0
# TREE = [10, math.inf, 5, 5, -10, -10, -10, -10, 7, 5, -math.inf, -math.inf, -7, -5, -7, -5]
TREE = [5, 6, 4, 69, 3, 70, 71, 72, 6, 42, 6, 420, 7, 101, 102, 103]
RESULT = dict()


def alpha_beta_minimax(current_state, depth, maximizing_player, alpha, beta):
    if depth == 0:  # or EMPTY_VALUE not in current_state:
        value = state_value(current_state)
        ret_val = (value, 0)
        # print(f"{depth},{ret_val}")
        RESULT[depth] = RESULT.get(depth, []) + [ret_val]
        return ret_val
    if maximizing_player:
        value = -math.inf
        column = None
        for col in range(7):
            next_state = get_next_state(current_state, col, maximizing_player)
            if next_state is not None:
                temp = alpha_beta_minimax(next_state, depth - 1, False, alpha, beta)
                if temp[0] > value:
                    value = temp[0]
                    column = col
                if value > beta:
                    break
                alpha = max(alpha, value)
        ret_val = (value, column)
        # print(f"{depth},{ret_val}")
        RESULT[depth] = RESULT.get(depth, []) + [ret_val]
        return ret_val
    else:
        value = math.inf
        column = None
        for col in range(7):
            next_state = get_next_state(current_state, col, maximizing_player)
            if next_state is not None:
                temp = alpha_beta_minimax(next_state, depth - 1, True, alpha, beta)
                if temp[0] < value:
                    value = temp[0]
                    column = col
                if value < alpha:
                    break
                beta = min(beta, value)
        ret_val = (value, column)
        # print(f"{depth},{ret_val}")
        RESULT[depth] = RESULT.get(depth, []) + [ret_val]
        return ret_val


def state_value(state):
    return evaluate_game_state(state)
    # return TREE[state]


def get_next_state(current_state, col, maximizing_player):
    if maximizing_player:
        player = 2
    else:
        player = 1
    return alternative_gamestate(current_state, col, player)
    # if col <= 1:
    #     next_state = (current_state<<1)+col
    #     # print(f"{current_state},{next_state}")
    #     return next_state
    # return None


def print_tree(tree):
    for key in sorted(tree.keys(), reverse=True):
        # v = (key*"\t").join([str(t) for t in tree[key]])
        print(f"Depth {key}, {tree[key]}")


test_state = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    2,
    0,
    0,
    0,
    0,
    0,
    0,
    2,
    0,
    0,
    0,
    0,
    0,
    0,
    2,
    1,
    1,
    1,
    0,
    0,
    0,
]
# final = alpha_beta_minimax(test_state, 2, False, -math.inf, math.inf)
# print(final)
# print_tree(RESULT)
