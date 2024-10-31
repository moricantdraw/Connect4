# import necessary libraries and modules
import numpy as np
import pygame
import sys
import math
import threading
import time
import copy
from alpha_beta_pruning import alpha_beta_minimax, get_progress, reset_progress

# Define colors used in board
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Set board dimensions
ROW_COUNT = 6
COLUMN_COUNT = 7


# Function to create board as an array
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


# Function to drop a piece onto the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece


# Function to check if a given column can hold a piece
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


# Function to find the next available row
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


# Function to flip the rows in the board
def print_board(board):
    print(np.flip(board, 0))


# Check if a piece has won (horzontally, vertically, or diagonally)
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True


# Function to draw the board on the screen
def draw_board(board):
    # Draw blue background and make spaces for pieces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen,
                BLUE,
                (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE),
            )
            pygame.draw.circle(
                screen,
                BLACK,
                (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2),
                ),
                RADIUS,
            )

    # Draw red or yellow pieces based on board values 
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(
                    screen,
                    RED,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        height - 20 - int(r * SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )
            elif board[r][c] == 2:
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        height - 20 - int(r * SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )
    pygame.display.update()


# Function to create a progress bar at the bottom of the screen
def progress_bar():
    while not game_over:
        draw_board(board)
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            pygame.Rect(0, height - 10, width, 10),
        )
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            pygame.Rect(0, height - 10, int(width * get_progress() / DIVISOR), 10),
        )
        pygame.display.update()
        time.sleep(0.03)


# Function to handle the human player's move
def human_player(first):
    global game_over, computer_turn
    if not game_over:
        posx = event.pos[0]
        col = int(math.floor(posx / SQUARESIZE))

        if is_valid_location(board, col):
            computer_turn = True
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2 - first)

            if winning_move(board, 2 - first):
                label = myfont.render(f"Player {2-first} wins!!", 1, WHITE)
                screen.blit(label, (40, 10))
                game_over = True
        draw_board(board)


# Functiom to reverse the board so the algorithm can use it 
def reverse_board(inp):
    out = inp
    out = [3 if i == 2 else i for i in out]  # turn 2 to 3
    out = [2 if i == 1 else i for i in out]  # turn 1 to 2
    out = [1 if i == 3 else i for i in out]  # turn 3 to 1
    return out


# Function to handle the computer's move
def computer_player(first):
    global game_over, computer_turn

    # Check if game isn't over and continue if so
    if not game_over:
        reset_progress() # reset progress bar tracking algorithm computations

        # Modify the board so that the algorithm can do its calculations
        modified_board = np.reshape(
            np.fliplr(np.flip(copy.deepcopy(board))), -1
        ).tolist()

        # Reverse boaerd values if the computer goes first
        if first:
            modified_board = reverse_board(modified_board)

        # Show modified board of 6 rows and 7 columns    
        for i in range(6):
            print(modified_board[7 * i : 7 * i + 7])
        d = None


        # Calculate algorithm move with alpha-beta pruning

        # Calculate winning move for computer
        computer_wins = alpha_beta_minimax(modified_board, 1, True, -math.inf, math.inf)

        # Check if the computer needs to block
        computer_block = alpha_beta_minimax(
            modified_board, 1, False, -math.inf, math.inf
        )

        # Check if the computer can win in one move
        if math.isinf(computer_wins[0]):
            final = computer_wins

        # If its not a win, check if the computer should block the winning move from the opponent
        elif math.isinf(computer_block[0]):
            final = computer_block

        # If there is no clear win or block, calculate move with deeper search based on remaining slots
        else:
            d = min(depth, modified_board.count(0))
            chosen_move = (None, None)
            
            # Find a valid move at decreasing depths if need be
            while chosen_move[1] is None and d > 0:
                # Run alpha-beta minimax at current depth
                chosen_move = alpha_beta_minimax(
                    modified_board, d, True, -math.inf, math.inf
                )
                print(d)
                d -= 2
            final = chosen_move # Set final move after calculations
        print(f"{final}")
        
        # Execute the computer's move
        col = final[1]
        
        # If no valid move present, teh ocmputer resigns
        if col is None:
            label = myfont.render("Resigned!!", 1, WHITE)
            screen.blit(label, (40, 10))
            game_over = True
        
        else:
            # Drop the piece on the board if the selected column is valid
            if is_valid_location(board, col):
                computer_turn = False
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2 - first)

                # Check if the move results in a win
                if winning_move(board, 2 - first):
                    label = myfont.render(f"Player {2-first} wins!!", 1, WHITE)
                    screen.blit(label, (40, 10))
                    game_over = True

        draw_board(board) # Update board


# Set the depth the AI has to search based on the game state
def set_depth(new_depth):
    global depth, DIVISOR
    depth = new_depth
    DIVISOR = depth ** (7 - 1.5)

# Initialize the games settings and start a loop to play the game
board = create_board()
print_board(board)
game_over = False
turn = 0


# Initialize a pygame window
pygame.init()
SQUARESIZE = 100

# define width and height of board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE + 20

size = (width, height) # Set board size
RADIUS = int(SQUARESIZE / 2 - 5) # Set radius of pieces
screen = pygame.display.set_mode(size) # Initialize game screen
myfont = pygame.font.SysFont("monospace", 75) # Set font for messages

# Initialize algorithm computation depth 
set_depth(6)
# Start a new thread to display progress as algorithm calculates moves
t1 = threading.Thread(target=progress_bar)
t1.start()

# Set computer to always go first
computer_first = True
computer_turn = computer_first

# Game loop that runs until the game is over
while not game_over:
    for event in pygame.event.get():
        # Check if the window is closed and terminate the game
        if event.type == pygame.QUIT:
            game_over = True
            sys.exit()

        # Draw a piece for the user to preview before placing above their desired column
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if not computer_first:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)

        # Execute the computers move when it's their turn
        if computer_turn:
            computer_player(computer_first)
            pygame.event.clear()

        # Handle a user clicking a column to make a move
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            human_player(not computer_first)

    # Adjust the Algorithm search depth based on remaining moves
    s = 0
    for c in range(7):
        s += is_valid_location(board, c)
    set_depth(int(10 - s / 2))

    # Tie the game if the board is full
    if 0 not in board:
        draw_board(board)
        label = myfont.render("Tie!!", 1, WHITE)
        screen.blit(label, (40, 10))
        game_over = True
        pygame.display.update()

    # Wait to close the window if the game is over
    if game_over:
        pygame.time.wait(10000)
