import json
import pprint 

# define the board
# define how people input their moves
# plays = 0(empty) 1(blue) 2(red)

# functions
# -build game board
# -- allocate a game board
# -- initialize game board

# - game play
# - def try_next_move (board, moves_played): ...
# -- making a move
# -- checking for win

# minimax
# comp vs. user -> comp plays assuming user plays optimally
# monte carlo

# board size = n^2 + (n-1)^2

# Set board size
n = 4

# Initialize board
board = [[[1 for row in range(n - cubity)] 
             for column in range(n - cubity)] 
             for cubity in range(2)]

# Example Board: 
# [[[0, 0, 0, 0],
#   [0, 0, 1, 0],
#   [0, 0, 0, 0],
#   [0, 0, 0, 0]],
#  [[0, 0, 0],
#   [0, 0, 0],
#   [0, 0, 0]]]

# Game play
# player_a = input("Player A: Enter a move: ")
# player_b = input("Player B: Enter a move: ")

# move = [0, 2, 2], player = 1 or 2, board[oddity, row, column]
def play(board, move, player):
    '''Given a board and a player's move, update the board'''

    n = len(board[0][0])

    assert n > 1
    assert type(player) == int()
    assert player == 1 or player == 2

    if move[0] == 0: # even board
        assert move[1] < n and move[2] < n

    if move[0] == 1: # odd board
        assert move[1] < n - 1 and move[2] < n - 1

    assert board[move[0]][move[1]][move[2]] == 0

    board[move[0]][move[1]][move[2]] = player


blues_paths = [(1, 3, 4, 7, 9, 11), (1, 4, 7, 7 )]


# def check_path_regular_h(player = 1 or 2, move = []):
#     """Check to see if there's a path for a play made by either:
#         - blue in an odds cube
#         - red in an evens cube """

#     potential_moves = [[option1], [option2], [option3]...[option6]]

#     for move in potential_moves:
#         if empty or other player or edge: # skip because we're tracing only one player's path
#             skip
#         else:
#             move to that square to keep checking the path
#             call the next relevant function


# blue = 0, red = 1,
# cubity, 1=odd
# horizontal h = 0, vertical h = 1


def determine_moves(board, move, board_size):
    cubity, row, column = move 
    player = board[cubity][row][column]
    potential_moves = []

    assert player > 0
    player -= 1 # re-adjust player to be either 0 or 1 for this function

    orientation = player ^ cubity ^ 1 # XOR with 1 to make it XNOR

    # finding wings 
    potential_moves.extend([
        [cubity, row - orientation, column - (1 - orientation)], 
        [cubity, row + orientation, column + (1 - orientation)], 
        ])  

    # finding other possibilities
    # result independent of orientation 
    additive = (cubity * 2) - 1 

    potential_moves.extend([
        [cubity ^ 1, row, column], 
        [cubity ^ 1, row, column + additive], 
        [cubity ^ 1, row + additive, column + additive], 
        [cubity ^ 1, row + additive, column],
        ])

    inbound_moves = []
    for move in potential_moves:
        assert move[0] == 0 or move[0] == 1
        if (
                move[1] >= 0 
            and move[1] < board_size - cubity
            and move[2] >= 0 
            and move[2] < board_size - cubity
           ):
           inbound_moves.append(move)
    
    # output is a 2D array of inbound potential moves 
    return inbound_moves


# def does_full_path_exist (board, path_walked = [ ]):
#     if is_last_step_at_the_other_end (path_walked [-1]): return True
#     for next_step in generate_unique_next_steps (board, path_walked):
#         if does_full_path_exist (augment (board, next_step), path_walked + next_step): return True
#     return False

# move = [0, 2, 2] (oddity, row, column)

def does_full_path_exist(board, current_move):
    """Checks for a win"""

    board_size = len(board[0][0])

    # TODO: Make this work for both players (vertical and horizontal )
    player = board[current_move[0]][current_move[1]][current_move[2]]
    assert player > 0 # player is either 1=blue (vertically) or 2=red (horizontally)

    # quick check - if extreme sides/top/bottom is empty, then player can't have won 
    if (all (board[0][0][x] != player for x in range(board_size)) or 
        all (board[0][board_size - 1][x] != player for x in range(board_size))):
        return false 

    if (all (board[0][x][0] != player for x in range(board_size)) or 
        all (board[0][x][board_size - 1] != player for x in range(board_size))):
        return false 

    # initialize empty board of breadcrumbs for the player 
    bread = [[[0 for row in range(board_size - cubity)] 
                 for column in range(board_size - cubity)] 
                 for cubity in range(2)]

    # update breadcrumbs board with current move 
    # bread[current_move[0]current_move[1]current_move[2]] = player 

    # span walks the board of breadcrumbs at the current move and updates it 
    # with all the existing connected moves 
    # span(board, bread, player, current_move)
    # return (any (bread[0][0][x] == player for x in range(board_size)) and 
    #         any (bread[0][board_size - 1][x] == player for x in range(board_size)))

# Make plays reversible - TODO: encode a stack, make it possible to walk foward and back
# [move, magic status]
# history.append([coordinates, magic])

history = []

def neighbor_status(current_move, player, board, bread, board_size):
    neighbors = determine_moves(bread, current_move, board_size)

    magic = 0 

    # walk through six neighbors
    for power, neighbor in enumerate(neighbors):
        if board[neighbor[0]][neighbor[1]][neighbor[1]] == player: # 0, 1, 2, 3 whether it's empty, island, L, R
            # 0 * 4^0 + 0 * 4^1 + 1 * 4^2 + 2 * 4^3 + 3 * 4^4 + 1 * 4^5 = 1936
            magic += bread[neighbor[0]][neighbor[1]][neighbor[1]] * 4 ^ power
            
    return magic

# TODO: Walk path to update nearby neighbors in bread -> can use same way of doing this for forward and reverse 
# TODO: Might update bread and board to be unified 
# Let board contain both info? Might help with moving forward and reversing 

# Chat notes 
# Mike C to Everyone (6:02 PM)
# (0, 0, 1, 2 3 1)
# Me to Everyone (6:03 PM)
# 001231
# .001231
# Mike C to Everyone (6:05 PM)
# (3, 1, 4, 1, 5, 9)
# -> 314159
# 3 * 10^5   +  1 * 10^4 + ... + 9 * 10^0
# n * 4^5 + m * 4^4 + el * 4^3 ...
# [ red | yellow | green | purple | blue ]
# Mike C to Everyone (6:10 PM)
# 5 * 5 * 5
# ( 0 .. 4 )
# [15, magic0]
# a = []
# a.append(3)
# Mike C to Everyone (6:16 PM)
# history.append([coordinates, magic])
# len(history)
# Mike C to Everyone (6:42 PM)
# multiplier = 1
# (0, 0, 1, 2, 3, 1)
# 0 * 4^0 + 0 * 4^1 + 1 * 4^2 + 2 * ...
# Mike C to Everyone (6:48 PM)
# (3, 1, 4, 1, 5, 9)
# 314159
# 314159 / 1000 (int divide)
# -> 314
# 314 modulo 10 (314 % 10)
# -> 4