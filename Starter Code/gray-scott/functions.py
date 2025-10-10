from posix import system
# Insert your simulate_gray_scott() function here, along with any subroutines that you need.
#HW 3 9.1
from numpy._typing import _128Bit
from .datatypes import Board, Cell

"""
SimulateGrayScott(initialBoard, numGens, feedRate, killRate, preyDiffusionRate, predatorDiffusionRate, kernel)
	boards ← array of numGens + 1 Boards
	boards[0] ← initialBoard
	for i ← 1 to numGens
		boards[i] ← UpdateBoard(boards[i-1], feedRate, killRate, preyDiffusionRate, predatorDiffusionRate, kernel)
	return boards
"""
"""
UpdateBoard(currentBoard, feedRate, killRate, preyDiffusionRate, predatorDiffusionRate, kernel)
	numRows ← CountRows(currentBoard)
	numCols ← CountColumns(currentBoard)
	newBoard ← InitializeBoard(numRows, numCols)
	for row ← 0 to numRows – 1
		for col ← 0 to numCols – 1
			newBoard[row][col] ← UpdateCell(currentBoard, row, col, feedRate, killRate, preyDiffusionRate, predatorDiffusionRate, kernel)
	return newBoard
"""
def board_to_matrix(current_board: Board, particle: int) -> list[list[float]]:
    """
    Input: Takes a Board of tuples and a particle(0 if "prey"; 1 if "predator")
    Output: A matrix of floats with each element being the concentration of one single particle of the same type.
    """
    matrix = []
    for i in range(len(current_board)):
        matrix.append([])
        for j in range(len(current_board[i])):
            matrix[i].append(current_board[i][j][particle])

    return matrix

def change_due_to_reactions(current_cell: Cell, feed_rate: float, kill_rate: float) -> Cell:
    """
    Input: a cell, a feed rate: the rate of the feed reaction, and a kill rate: the rate of the kill reaction.
    Output: A cell with the new (A,B) concentrations before adding those concentrations to the diffusion concentrations.
    """
    #reproduction reaction rate
    r = 1
    #new concentrations
    feed_rxn_a = (feed_rate*(1-current_cell[0]))
    feed_rxn_b = (kill_rate*(current_cell[1]))
    reprod_rxn = r*(current_cell[0] * current_cell[1]**2)
    new_A = current_cell[0] + feed_rxn_a - reprod_rxn
    new_B = current_cell[1] - feed_rxn_b + reprod_rxn
    return (new_A, new_B)

def change_due_to_diffusion(current_board:list[list[float]], row:int, col:int, prey_diffusion_rate:float,
    predator_diffusion_rate:float, kernel:list[list[float]]) -> Cell:
    """
    Input: A Board variable current_board, integers row and col,
    decimal variables prey_diffusion_rate and predator_diffusion_rate, and a 3 x 3 decimal matrix kernel.
    Output: a Cell variable storing the result of applying diffusion reactions with parameters
    prey_diffusion_rate, predator_diffusion_rate, and kernel to the Cell variable at current_board[row][col].
    """
    a_board = diffuse_board_one_particle(current_board, prey_diffusion_rate, kernel)
    b_board = diffuse_board_one_particle(current_board, predator_diffusion_rate, kernel)
    return (a_board[row][col], b_board[row][col])

def diffuse_board_one_particle(current_board: list[list[float]], diffusion_rate: float, kernel: list[list[float]]) -> list[list[float]]:
    """
    Input: A two-dimensional array of decimal numbers current_board and a 3 × 3 matrix of decimal numbers kernel.
    Output: A two-dimensional array of decimal numbers new_board corresponding to applying
    one time step of diffusion to current_board using the kernel kernel.
    """
    concentrations = []
    for i in range(len(current_board)):
        concentrations.append([])
        for j in range(len(current_board[i])):
            moore = make_moore(current_board, i, j)
            concentrations[i].append(current_board[i][j] + convolution(moore, diffusion_rate, kernel))

    return concentrations



def convolution(neighborhood: list[list[float]], diffusion_rate: float, kernel: list[list[float]]) -> float:
    convolution = 0
    new_kernel = scale_kernel(kernel, diffusion_rate)
    assert_3by3(neighborhood, new_kernel)
    for i in range(len(neighborhood)):
        for j in range(len(neighborhood[i])):
            convolution += neighborhood[i][j] * new_kernel[i][j]

    return convolution

def scale_kernel(kernel: list[list[float]], diffusion_rate: float) -> list[list[float]]:
    new_kernel = []
    for i in range(len(kernel)):
        new_kernel.append([])
        for j in range(len(kernel[i])):
            new_kernel[i].append(kernel[i][j] * diffusion_rate)

    return new_kernel

def assert_3by3(neighborhood, kernel):
    if len(neighborhood) != len(kernel) and len(neighborhood[0]) != len(kernel[0]):
        raise ValueError("Moore neighborhood and kernel must be matrices of the same dimensions")

def make_moore(current_board: list[list[float]], row: int, col: int) -> list[list[float]]:
    neighborhood = []
    row_checks = [-1, 0, 1]
    col_checks = [-1, 0, 1]
    for i in row_checks:
        new_row = []
        for j in col_checks:
            if in_field(current_board, row + i, col + j):
                new_row.append(current_board[row+i][col+j])
            else:
                new_row.append(0)

        neighborhood.append(new_row)

    return neighborhood

def in_field(current_board: list[list[float]], row: int, col: int) -> bool:
    """
    Takes a two-dimensional slice of decimal numbers current_board, as well as integers row and col as input.
    This function should return true if b[row][col] is in range, and this function should return false otherwise.
    """
    return (0 <= row <= len(current_board) - 1) and (0 <= col <= len(current_board[row]) - 1)

def sum_cells(*cells: Cell) -> Cell:
    sum_a = 0
    sum_b = 0
    for cell in cells:
        sum_a += cell[0]
        sum_b += cell[1]

    return (sum_a, sum_b)
