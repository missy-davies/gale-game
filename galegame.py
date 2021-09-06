import json
import pprint

# Allocate a game board

# board size = n^2 + (n-1)^2
# Set board size
n = 4

# Initialize board as being empty for the determined board size
board = [[[0 for row in range(n - cubity)]
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

    # 'converting' information to base 4 for consistency with other calcuations
    # for reference:
        # >>> bin(((num // 4) * (4 ** 1)) + new)
        # '0b1011001011110110000010110'
        # here we take the original number, remove last 2 digits,
        # add space for 2 bits back, then replace them with whatever we want
    board[move[0]][move[1]][move[2]] = ((board[move[0]][move[1]][move[2]] // 4) * (4 ** 1)) + (player * 4**0)


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
    '''Determine what potential paths are available surrounding an existing move.
       This consists of finding the wings and pack as per our examples.'''

    cubity, row, column = move

    player = board[cubity][row][column] % 4 # get last 2 digits of encoded info

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

# legacy
# def does_full_path_exist(board, current_move):
#     """Checks for a win"""

#     board_size = len(board[0][0])

#     # TODO: Make this work for both players (vertical and horizontal )
#     player = board[current_move[0]][current_move[1]][current_move[2]] % 4
#     assert player > 0 # player is either 1=blue (vertically) or 2=red (horizontally)

#     # quick check - if extreme sides/top/bottom is empty, then player can't have won
#     if (all (board[0][0][x] % 4 != player for x in range(board_size)) or
#         all (board[0][board_size - 1][x] % 4 != player for x in range(board_size))):
#         return false

#     if (all (board[0][x][0] % 4 != player for x in range(board_size)) or
#         all (board[0][x][board_size - 1] % 4 != player for x in range(board_size))):
#         return false

    # span walks the board of breadcrumbs at the current move and updates it
    # with all the existing connected moves
    # span(board, bread, player, current_move)
    # return (any (bread[0][0][x] == player for x in range(board_size)) and
    #         any (bread[0][board_size - 1][x] == player for x in range(board_size)))

# Make plays reversible - TODO: encode a stack, make it possible to walk foward and back
# [move, magic status]
# history.append([coordinates, magic])

# history = []

def neighbor_status(current_move, player, board, board_size):
    '''Given a current move, determine what the status of the neighboring cells
       are - empty, island, Left or Right (Top / Bottom) attached'''

    neighbors = determine_moves(board, current_move, board_size)

    status = 0

    # walk through six neighbors
    for power, neighbor in enumerate(neighbors):
        if board[neighbor[0]][neighbor[1]][neighbor[2]] % 4 == player:
            # 0 * 4^0 + 0 * 4^1 + 1 * 4^2 + 2 * 4^3 + 3 * 4^4 + 1 * 4^5 = 1936
            status += (board[neighbor[0]][neighbor[1]][neighbor[2]] % 4) * (4 ^ power)

    return status # 0, 1, 2, 3 whether it's empty, island, L, R per neighbor

# Walk path to update nearby neighbors in bread -> can use same way of doing this for forward and reverse
# Let board contain both info? Might help with moving forward and reversing
def walk_path(starting_point, board, highest_status):
    board[starting_point[0]][starting_point[1]][starting_point[2]] |= 4 # set_breadcrumb(starting_point)

    # add in bit space to store status, then update it 
    (board[starting_point[0]][starting_point[1]][starting_point[2]] // 8) % 4 # how we access status bit
    # TODO: Need to examine the status bit, and change it if needed  

    for move in determine_moves(starting_point):
        if not (board[move[0]][move[1]][move[2]] // 4) % 2: # get_breadcrumbs(move)
            walk_path(move, board)
    

def consider_endgame(board, current_move):
    # look around where you are by last move 
    # send elf down the path 

    neighbors = determine_moves(board, current_move, board_size)

    highest = 0
    # walk through six neighbors
    for power, neighbor in enumerate(neighbors):
        if board[neighbor[0]][neighbor[1]][neighbor[2]] % 4 == player:
            status = (board[neighbor[0]][neighbor[1]][neighbor[2]] % 4) 
            if status > highest:
                highest = status 
                status = highest # promoting, maybe need to call walk path with highest thing as status point? 
        
    
# Board and bread are now unified - where board contains information about what player
# occupies the space and info about the surrounding neighbors

# bits 1 and 0: claimed
# bit 2: claimed
# bits 3 4: status
# bits 5 and higher (5 + 6 - 1)... : integer status encoding for reverseing