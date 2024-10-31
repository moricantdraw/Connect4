import math

# Function to evaluate the board state based on token placement
def evaluate_game_state(board, rows=6, cols=7, player=2):
    """
    Scores move based on how many player tokens are adjacent to each other.

    Parameters:
        board: List representing current state
        rows: Int representing of rows in the Connect 4 board
        cols: Int representing of columns in the Connect 4 board
        player: Int representing player making the move       

    Returns:
        float: The normalized score of the move (between 0 and 1).
    """
    score = 0 # Initialize score

    # Establish who the opponent is based on the player
    opponent = 1
    if player == 2:
        opponent = 1
    elif player == 1:
        opponent = 2

    # Defines scoring weights for sequences of length 2, 3, and 4 (normalized to 1)
    weights = {1: 0.0, 2: 1, 3: 5, 4: math.inf}

    # Helper function to check sequences
    def count_sequence(start, delta_row, delta_col, p, weight=2):
        # Counts the length of sequences of the player's tokens starting from (start) in the given direction.
        row, col = divmod(start, cols)
        start_row = row
        token_count = 0

        # Traverse the sequence in the specified direction
        detected = False # Check if sequence has started
        jump = 0 # Num of empty spaces
        end = 0 # Track how many times it gets to the end of a sequence
        start = 0


        while 0 <= row < rows and 0 <= col < cols:
            index = row * cols + col
            if board[index] == p: # If slot has token
                token_count += 1
                detected = True
                end = 0  # end on a token
                if jump == 0 and token_count >= 4:  # if a win is detected
                    return math.inf
            elif board[index] == 0: # If slot is empty
                if detected:
                    jump += 1 # track empty spaces
                    end += 1  # does not end on a token
                else:
                    start += 1
            else:
                break  # Stop if different token or empty spot

            # Move to next row and column
            row += delta_row
            col += delta_col

        if token_count + start + jump < 4:  # if not enough space to make a connect 4
            return 0
        if 4 < token_count + jump - end < 7 and jump > 1:  # disincentivize 5,6 (longer sequences)
            return 0
        if jump - end > 0:  # if there was a break, derate
            token_count -= 0.5 * (jump - end)
        if token_count:
            return weight**token_count  # + (0.5 - start_row * 0.08)
        return 0 # return 0 if no sequence is valid

    # Traverse the entire game to evaluate
    opponent_score = 0
    player_score = 0
    opponent_weight = 2
    player_weight = 2

    # Iterate through the board to check sequences for player and opponent
    for row in range(rows):
        for col in range(cols):
            index = row * cols + col
            if board[index] == opponent:
                # Check all directions for opponent sequence
                opponent_score -= count_sequence(
                    index, 0, 1, opponent, opponent_weight
                )  # Horizontal
                opponent_score -= count_sequence(
                    index, 1, 0, opponent, opponent_weight
                )  # Vertical
                opponent_score -= count_sequence(
                    index, 1, 1, opponent, opponent_weight
                )  # Diagonal-down-right
                opponent_score -= count_sequence(
                    index, -1, 1, opponent, opponent_weight
                )  # Diagonal-up-right
            elif board[index] == player:
                # Check in all four directions (horizontal, vertical, diagonal-down-right, diagonal-up-right)
                player_score += count_sequence(
                    index, 0, 1, player, player_weight
                )  # Horizontal
                player_score += count_sequence(
                    index, 1, 0, player, player_weight
                )  # Vertical
                player_score += count_sequence(
                    index, 1, 1, player, player_weight
                )  # Diagonal-down-right
                player_score += count_sequence(
                    index, -1, 1, player, player_weight
                )  # Diagonal-up-right

    # Return score
    if math.isinf(opponent_score):
        return opponent_score
    score = player_score + opponent_score
    return score  # normalized_score


# Code used for testing of implementation (see bottom of file)
def print_game_1d(game_state, rows=6, cols=7):
    "Helper function to print the 1D board as a 2D grid."
    for row in range(rows):
        print(game_state[row * cols : (row + 1) * cols])


# TESTING

# game_state = [
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,  # Row 0 (top)
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,
#     0,  # Row 1
#     0,
#     1,
#     0,
#     0,
#     0,
#     0,
#     0,  # Row 2
#     1,
#     2,
#     0,
#     0,
#     0,
#     0,
#     0,  # Row 3
#     2,
#     1,
#     0,
#     0,
#     0,
#     0,
#     0,  # Row 4
#     1,
#     2,
#     2,
#     2,
#     0,
#     0,
#     0,  # Row 5 (bottom)
# ]

# fmt: off
test_state = [
    0,0,0,2,0,0,0,
    0,0,0,1,0,0,0,
    0,0,0,2,0,0,0,
    0,1,0,1,0,0,0,
    2,2,0,2,0,0,0,
    1,1,0,2,2,0,1,
]
# fmt: on

# Evaluate for Player 2 and normalize
# normalized_score = evaluate_game_state(test_state)
# print(f"Normalized board score for Player 2: {normalized_score}")

# Print  game
# print("\ngame:")
# print_game_1d(game_state)

# so the numbers are quite small but they do get bigger as the game_state gets better for player 2 so maybe that's something
