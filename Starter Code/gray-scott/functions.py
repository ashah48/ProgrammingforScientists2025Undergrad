# Insert your simulate_gray_scott() function here, along with any subroutines that you need.
import math
from .datatypes import Board, Cell

def diffuse_board_one_particle(current_board: list[list[float]], kernel: list[list[float]]) -> list[list[float]]:
    """
    Input: A two-dimensional array of decimal numbers current_board and a 3 × 3 matrix of decimal numbers kernel.
    Output: A two-dimensional array of decimal numbers new_board corresponding to applying
    one time step of diffusion to current_board using the kernel kernel.
    """




def find_in_field(current_board: list[list[float]], row: int, col: int) -> list[tuple[int, int]]:
    tuples_list = []
    for r in range(len(current_board)):
        for c in range(len(current_board[r])):
            if in_field(current_board, row, col):
                tuples_list.append(tuple[row, col])

    return tuples_list

def make_field_for_cell(current_board: list[list[float]], row: int, col: int) -> list[list[float]]:
    num_rows = len(current_board)
    specific_board = []
    for i in range(num_rows):
        specific_board.append([])
        if in_field(current_board, row - i, col - i):
            specific_board[i].append(current_board[row-i][col-i])
        elif in_field(current_board, row - i, col + i):
            specific_board[i].append(current_board[row-i][col+i])
        elif in_field(current_board, row + i, col - i):
            specific_board[i].append(current_board[row-i][col+i])
        elif in_field(current_board)


def in_field(current_board: list[list[float]], row: int, col: int) -> bool:
    """
    Takes a two-dimensional slice of decimal numbers current_board, as well as integers row and col as input.
    This function should return true if b[row][col] is in range, and this function should return false otherwise.
    """
    return (0 <= row <= len(current_board) - 1) and (0 <= col <= len(current_board[row]) - 1)
