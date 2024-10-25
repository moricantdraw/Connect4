import numpy as np
import pygame
import sys
import math
import threading
import time
from alpha_beta_pruning import alpha_beta_minimax, get_progress, reset_progress

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


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


def draw_board(board):
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


board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100

# define width and height of board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE + 20

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
# draw_board(board)
# pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

depth = 6
DIVISOR = depth**7
t1 = threading.Thread(target=progress_bar)
t1.start()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
        # pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # Ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

            # print_board(board)
            draw_board(board)
            turn += 1
            turn = turn % 2

            # Ask for Player 2 Input
            # else:
            #     # posx = event.pos[0]
            #     # col = int(math.floor(posx / SQUARESIZE))
            if not game_over:
                reset_progress()
                modified_board = np.reshape(np.fliplr(np.flip(board)), -1).tolist()
                for i in range(6):
                    print(modified_board[7 * i : 7 * i + 7])
                d = None
                # Computer wins
                computer_wins = alpha_beta_minimax(
                    modified_board, 1, True, -math.inf, math.inf
                )
                # Computer must block
                computer_block = alpha_beta_minimax(
                    modified_board, 1, False, -math.inf, math.inf
                )
                if math.isinf(computer_wins[0]):
                    final = computer_wins
                elif math.isinf(computer_block[0]):
                    final = computer_block
                else:
                    d = min(depth, modified_board.count(0))
                    chosen_move = (None, None)
                    while chosen_move[1] is None and d > 0:
                        chosen_move = alpha_beta_minimax(
                            modified_board, d, True, -math.inf, math.inf
                        )
                        print(d)
                        d -= 2
                    final = chosen_move
                print(f"{final}")
                col = final[1]
                if col is None:
                    label = myfont.render("Resigned!!", 1, GREEN)
                    screen.blit(label, (40, 10))
                    game_over = True
                else:
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            label = myfont.render("Player 2 wins!!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True

                # print_board(board)
                draw_board(board)

            turn += 1
            turn = turn % 2

            pygame.event.clear()

            if game_over:
                pygame.time.wait(10000)
