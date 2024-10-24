def print_board(board):
    for row in board:
        print(' '.join(row))
    print()

def check_winner(board, player):
    for row in board:
        for i in range(4):
            if all(piece == player for piece in row[i:i + 4]):
                return True 

    for col in range(7):
        for i in range(3):
            if all(row[col] == player for row in board[i:i + 4]):
                return True
            
    for row in range(3):
        for col in range(4):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True 
            
    for row in range(3, 6):
        for col in range(4):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
            
    return False

def is_full(board):
    return all(piece != ' ' for row in board for piece in row)



# # Minimax implementation
# def get_next_state(board, col, player):
#     if col <= 1:
#         next_state = (current_state<<1)+col
#         # print(f"{current_state},{next_state}")
#         return next_state
#     return None

# def state_value(board):
#     return TREE[state]

# def simple_minimax(board, depth, maximizing_player):
#     if depth == 0: #or EMPTY_VALUE not in current_state:
#         value = state_value(current_state)
#         ret_val = (value,0)
#         # print(f"{depth},{ret_val}")
#         RESULT[depth] = RESULT.get(depth,[])+[ret_val]
#         return ret_val
#     if maximizing_player:
#         value = -math.inf
#         column = None
#         for col in range(7):
#             next_state = get_next_state(current_state, col)
#             if next_state is not None:
#                 temp = simple_minimax(next_state, depth-1, False)
#                 if temp[0]>value:
#                     value = temp[0]
#                     column = col
#         ret_val = (value, column)
#         # print(f"{depth},{ret_val}")
#         RESULT[depth] = RESULT.get(depth,[])+[ret_val]
#         return ret_val
#     else:
#         value = math.inf
#         column = None
#         for col in range(7):
#             next_state = get_next_state(current_state, col)
#             if next_state is not None:
#                 temp = simple_minimax(next_state, depth-1, True)
#                 if temp[0]<value:
#                     value = temp[0]
#                     column = col
#         ret_val = (value, column)
#         # print(f"{depth},{ret_val}")
#         RESULT[depth] = RESULT.get(depth,[])+[ret_val]
#         return ret_val



def main():
    board = [[' ' for _ in range(7)] for _ in range(6)]
    player = 'X'

    while True:
        print_board(board)
        col = int(input(f'Player {player} enter a column 0-6: '))

        if col < 0 or col > 6 :
            print('not valid')

        for row in range(5, -1, -1):
            if board[row][col] == ' ':
                board[row][col] = player
                break
            else:
                print('column full!')
                continue
        
        if check_winner(board, player):
            print_board(board)
            print(f"Player {player} wins!")
            break

        if is_full(board):
            print_board(board)
            print(f'Tie')
            break

        player = 'O' if player == 'X' else 'X'

main()