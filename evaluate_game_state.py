import math


def evaluate_game_state(board, rows=6, cols=7, player=2):
    """
    Scores move based on how many player tokens are adjacent to each other.

    Returns:
    float: The normalized score of the move (between 0 and 1).
    """
    score = 0

    opponent = 1
    if player == 2:
        opponent = 1
    elif player == 1:
        opponent = 2

    # Defines  scoring weights for sequences of length 2, 3, and 4 (normalized to 1)
    weights = {1: 0.0, 2: 1, 3: 5, 4: math.inf}

    # Helper function to check sequences
    def count_sequence(start, delta_row, delta_col, p, weight=2):
        # Counts the length of sequences of the player's tokens starting from (start) in the given direction.
        row, col = divmod(start, cols)
        start_row = row
        token_count = 0

        # Traverse the sequence in the specified direction
        detected = False
        jump = 0
        end = 0
        start = 0
        while 0 <= row < rows and 0 <= col < cols:
            index = row * cols + col
            if board[index] == p:
                token_count += 1
                detected = True
                # if blank:
                #     # token_count -= 1
                #     blank = False
                end = 0  # end on a token
                if jump == 0 and token_count >= 4:  # if a win is detected
                    return math.inf
            elif board[index] == 0:
                if detected:
                    jump += 1
                    end += 1  # does not end on a token
                else:
                    start += 1
            else:
                break  # Stop if different token or empty spot

            row += delta_row
            col += delta_col

        # if jump - end > 0:
        #     token_count = min(token_count, 3)
        # # Add to score based on length of sequence
        # token_count = min(max(1, token_count), 4)
        # if token_count in weights:
        #     return weights[token_count]
        if token_count + start + jump < 4:  # if not enough space
            return 0
        if 4 < token_count + jump - end < 7 and jump > 1:  # disincentivize 5,6
            return 0
        if jump - end > 0:  # if there was a break, derate
            token_count -= 0.5 * (jump - end)
        if token_count:
            return weight**token_count  # + (0.5 - start_row * 0.08)
        return 0

    # Traverse the entire game to evaluate
    opponent_score = 0
    player_score = 0
    opponent_weight = 2
    player_weight = 2
    for row in range(rows):
        for col in range(cols):
            index = row * cols + col
            if board[index] == opponent:
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

    # max_possible_score = 4 * rows * cols

    # Normalize the score between 0 and 1
    # normalized_score = min(score / max_possible_score, 1.0)
    if math.isinf(opponent_score):
        # if math.isinf(player_score):
        #     return 0
        return opponent_score
    score = player_score + opponent_score
    return score  # normalized_score


# MORE TESTING STUFF--- YOU CAN IGNORE THIS
def print_game_1d(game_state, rows=6, cols=7):
    """Helper function to print the 1D board as a 2D grid."""
    for row in range(rows):
        print(game_state[row * cols : (row + 1) * cols])


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
