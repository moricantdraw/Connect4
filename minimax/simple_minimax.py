# https://en.wikipedia.org/wiki/Minimax#Pseudocode
import math

EMPTY_VALUE = 0
TREE = [10, math.inf, 5, 5, -10, -10, -10, -10, 7, 5, -math.inf, -math.inf, -7, -5, -7, -5]

def simple_minimax(current_state, depth, maximizing_player):
    if depth == 0: #or EMPTY_VALUE not in current_state:
        value = state_value(current_state)
        ret_val = (value,0)
        print(f"{depth},{ret_val}")
        return ret_val
    if maximizing_player:
        value = -math.inf
        column = None
        for col in range(7):
            next_state = get_next_state(current_state, col)
            if next_state is not None:
                temp = simple_minimax(next_state, depth-1, False)
                if temp[0]>value:
                    value = temp[0]
                    column = col
        ret_val = (value, column)
        print(f"{depth},{ret_val}")
        return ret_val
    else:
        value = math.inf
        column = None
        for col in range(7):
            next_state = get_next_state(current_state, col)
            if next_state is not None:
                temp = simple_minimax(next_state, depth-1, True)
                if temp[0]<value:
                    value = temp[0]
                    column = col
        ret_val = (value, column)
        print(f"{depth},{ret_val}")
        return ret_val
    
def state_value(state):
    return TREE[state]

def get_next_state(current_state, col):
    if col <= 1:
        next_state = (current_state<<1)+col
        # print(f"{current_state},{next_state}")
        return next_state
    return None

final = simple_minimax(0, 4, True)
print(final)