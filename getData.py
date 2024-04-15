import re
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

#INPUT PGN FILE AND PARSES THROUGH THE FILE FOR MOVES
def parse_pgn_moves(pgn_file):
    #EMPTY LISTS;..STORING VARIABLES
    white_moves = []
    black_moves = []
    white_queen_captures = []
    black_queen_captures = []
    white_queen_squares = []
    black_queen_squares = []
    #OPEN PGN FILE...READ FILE
    with open(pgn_file, 'r') as f:
        pgn_text = f.read()
    # EXTRACT MOVES FROM THE PGN...STORING THEM IN THE MOVES LIST
    moves = re.findall(r'\d+\.\s+(\S+)\s+(\S+)', pgn_text)
    #ITERATES THROUGH THE MOVES..SPLITS DEPENDING ON PIECE MOVE
    for white_move, black_move in moves:
        white_moves.append(white_move)
        black_moves.append(black_move)

    for white_move, black_move in zip(white_moves, black_moves):
        #X INDICATES THERE IS A CAPTURE
        if 'x' in white_move:
            #Q INDICATES ITS THE QUEEN MAKING A MOVE
            if 'Q' in white_move:
                #STORE THE QUEEN CAPTRUING SQUARE
                match = re.search(r'[a-h][1-8]', white_move)
                if match:
                    captured_square = match.group()
                    white_queen_captures.append(captured_square)
                    # MOVE BACKWARDS TO FIND THE SQUARE THE QUEEN WAS PREVIOUSLY ON
                    #THIS IS THE QUEEN'S ATTACKING SQUARE
                    prev_move_index = white_moves.index(white_move) - 1
                    while prev_move_index >= 0:
                        prev_move = white_moves[prev_move_index]
                        if 'Q' in prev_move:
                            prev_match = re.search(r'[a-h][1-8]', prev_move)
                            if prev_match:
                                white_queen_squares.append(prev_match.group())
                            break
                        prev_move_index -= 1
        #SAME LOGIC FOR BLACK
        if 'x' in black_move:
            if 'Q' in black_move:
                match = re.search(r'[a-h][1-8]', black_move)
                if match:
                    captured_square = match.group()
                    black_queen_captures.append(captured_square)
                    prev_move_index = black_moves.index(black_move) - 1
                    while prev_move_index >= 0:
                        prev_move = black_moves[prev_move_index]
                        if 'Q' in prev_move:
                            prev_match = re.search(r'[a-h][1-8]', prev_move)
                            if prev_match:
                                black_queen_squares.append(prev_match.group())
                            break
                        prev_move_index -= 1

    #COUNTS THE FREQUENCY OF THE ATTACKING SQUARES
    white_attacking_square_frequency = Counter(white_queen_squares)
    black_attacking_square_frequency = Counter(black_queen_squares)

    return (white_moves, black_moves, white_queen_captures, black_queen_captures,
            white_queen_squares, black_queen_squares, white_attacking_square_frequency,
            black_attacking_square_frequency)


def plot_heatmap(attacking_square_frequency, title):
    # Initialize the chess board as an 8x8 grid
    board = np.zeros((8, 8))

    # Map the attacking square frequency to the corresponding positions on the board
    for square, frequency in attacking_square_frequency.items():
        file, rank = square
        x = ord(file) - ord('a')
        y = 8 - int(rank)
        board[y][x] = frequency

    plt.imshow(board, cmap='hot', interpolation='nearest')
    plt.title(title)
    plt.colorbar(label='Frequency')
    plt.xticks(np.arange(8), labels=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    plt.yticks(np.arange(8), labels=['8', '7', '6', '5', '4', '3', '2', '1'])
    plt.xlabel('File')
    plt.ylabel('Rank')
    plt.show()


# RUN
pgn_file = "/Users/jenniferperez/Desktop/lichess_db_standard_rated_2013-01.pgn"
(white_moves, black_moves, white_queen_captures, black_queen_captures,
 white_queen_squares, black_queen_squares, white_attacking_square_frequency,
 black_attacking_square_frequency) = parse_pgn_moves(pgn_file)

plot_heatmap(white_attacking_square_frequency, 'White Queen Attacking Squares')
plot_heatmap(black_attacking_square_frequency, 'Black Queen Attacking Squares')










