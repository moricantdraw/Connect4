import copy

def alternative_gamestate(game_state, column, player, rows=6, cols=7):
    """
    Parameters:
    game_state: what the game looks like 
    column: Column (0-indexed) in which to make the move.
    player: Player making the move 
    rows: Number of rows in the Connect 4 board 
    cols: Number of columns in the Connect 4 board 
    
    Returns:
    new_game_state 
    """
    new_game_state= copy.deepcopy(game_state)  # Create a copy of the gamestate to preserve the original
    
    # Iterate over the rows from bottom to top to find the lowest empty spot in the column
    for row in range(rows-1, -1, -1):  # Start from the last row-- go up
        index = row * cols + column  # 1D array index for (row, col)
        if new_game_state[index] == 0:  # Check if empty
            new_game_state[index] = player  # Place the player's token
            return new_game_state  # Return the updated game_state
    
    # If the column is full...
    print(f"Column {column} is full!")
    return game_state  # No move made !

def print_game_1d(game_state, rows=6, cols=7):   #this was for me to see it... you don't have to keep this 
    for row in range(rows):
        print(game_state[row * cols:(row + 1) * cols])

# TESTING STUFF
game_state = [
    0, 0, 0, 0, 0, 0, 0,  # Row 0 (top)
    0, 0, 0, 0, 0, 0, 0,  # Row 1
    0, 1, 0, 0, 0, 0, 0,  # Row 2
    1, 2, 0, 0, 0, 0, 0,  # Row 3
    2, 1, 0, 0, 0, 0, 0,  # Row 4
    1, 2, 1, 0, 0, 0, 0   # Row 5 (bottom)
]

# Simulate Player 2 making a move in column 3
new_game_state= alternative_gamestate(game_state, 3, 2)

# Print the new board as a 2D grid
print("New board after Player 2's move:")
print_game_1d(new_game_state)
