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
    weights = {2: 0.1, 3: 0.3, 4: math.inf}

    # Helper function to check sequences
    def count_sequence(start, delta_row, delta_col, p):
        # Counts the length of sequences of the player's tokens starting from (start) in the given direction.
        row, col = divmod(start, cols)
        token_count = 0

        # Traverse the sequence in the specified direction
        while 0 <= row < rows and 0 <= col < cols:
            index = row * cols + col
            if board[index] == p:
                token_count += 1
            else:
                break  # Stop if different token or empty spot

            row += delta_row
            col += delta_col

        # Add to score based on length of sequence
        if token_count in weights:
            return weights[token_count]
        return 0

    # Traverse the entire game to evaluate
    for row in range(rows):
        for col in range(cols):
            index = row * cols + col
            if board[index] == player:
                # Check in all four directions (horizontal, vertical, diagonal-down-right, diagonal-up-right)
                score += count_sequence(index, 0, 1, player)  # Horizontal
                score += count_sequence(index, 1, 0, player)  # Vertical
                score += count_sequence(index, 1, 1, player)  # Diagonal-down-right
                score += count_sequence(index, -1, 1, player)  # Diagonal-up-right
            elif board[index] == opponent:
                score -= count_sequence(index, 0, 1, opponent)  # Horizontal
                score -= count_sequence(index, 1, 0, opponent)  # Vertical
                score -= count_sequence(index, 1, 1, opponent)  # Diagonal-down-right
                score -= count_sequence(index, -1, 1, opponent)  # Diagonal-up-right

    # max_possible_score = 4 * rows * cols

    # Normalize the score between 0 and 1
    # normalized_score = min(score / max_possible_score, 1.0)

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

# Evaluate for Player 2 and normalize
# normalized_score = evaluate_game_state(game_state)
# print(f"Normalized board score for Player 2: {normalized_score}")

# Print  game
# print("\ngame:")
# print_game_1d(game_state)

# so the numbers are quite small but they do get bigger as the game_state gets better for player 2 so maybe that's something
