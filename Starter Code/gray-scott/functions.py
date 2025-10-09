# Insert your simulate_gray_scott() function here, along with any subroutines that you need.
import math
#from .datatypes import Board, Cell

#HW 3 9.1
def diffuse_board_one_particle(current_board: list[list[float]], kernel: list[list[float]]) -> list[list[float]]:
    """
    Input: A two-dimensional array of decimal numbers current_board and a 3 × 3 matrix of decimal numbers kernel.
    Output: A two-dimensional array of decimal numbers new_board corresponding to applying
    one time step of diffusion to current_board using the kernel kernel.
    """
    concentrations = [[] * len(current_board)]
    moores = make_moores(current_board)
    for i in range(len(current_board)):
        for j in range(len(current_board[i])):
            concentrations[i][j] = convolution(moores[i][j], kernel)

    return concentrations



def convolution(neighborhood: list[list[float]], kernel: list[list[float]]) -> float:
    pass

def make_moores(current_board: list[list[float]]) -> list[list[list[float]]]:



def in_field(current_board: list[list[float]], row: int, col: int) -> bool:
    """
    Takes a two-dimensional slice of decimal numbers current_board, as well as integers row and col as input.
    This function should return true if b[row][col] is in range, and this function should return false otherwise.
    """
    return (0 <= row <= len(current_board) - 1) and (0 <= col <= len(current_board[row]) - 1)
