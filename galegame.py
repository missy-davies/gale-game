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
even = [[0 for row in range(n)] for column in range(n)]
odd = [[0 for row in range(n-1)] for column in range(n-1)]
board = [even, odd]


# Game play 
player_a = input("Player A: Enter a move: ")
player_b = input("Player B: Enter a move: ")

# move = [0, 2, 2], player = 1 or 2
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



# [[[0, 0, 0, 0], 
#   [0, 0, 0, 0], 
#   [0, 0, 0, 0], 
#   [0, 0, 0, 0]], 
#  [[0, 0, 0], 
#  [0, 0, 0], 
#  [0, 0, 0]]]