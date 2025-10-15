from datatypes import Board, Cell
from tkinter.tix import AUTO
from symbol import with_item

def simulate_gray_scott(initial_board:Board, num_gens:int, feed_rate: float, kill_rate: float, prey_diffusion_rate: float
    ,predator_diffusion_rate:float, kernel: list[list[float]]) -> list[Board]:
    """
    Input: An initial board, number of generations, feed rate, kill rate, prey diffusion rate, predator diffusion rate, and a kernel.
    Output: A list of boards where the first board is the initial board and the last board is a board returned after num_gens generations.
    """
    boards = [initial_board]
    for i in range(1, num_gens+1):
        boards.append(update_board(boards[i-1], feed_rate, kill_rate, prey_diffusion_rate, predator_diffusion_rate, kernel))
        print(f"Recorded generation {i}/{num_gens}")

    return boards

def update_board(current_board:Board, feed_rate: float, kill_rate: float, prey_diffusion_rate:float, predator_diffusion_rate:float,
    kernel: list[list[float]]) -> Board:
    """
    Input: A current board, a feed rate, a kill rate, a prey diffusion rate, a predator diffusion rate, and a kernel
    Output: A new updated board.
    """
    num_rows = count_rows(current_board)
    num_cols = count_cols(current_board)
    #Get the diffused matrices for prey and predator concentrations
    a_matrix = tuple_board_to_matrix(current_board, 0)
    b_matrix = tuple_board_to_matrix(current_board, 1)
    a_diffused = diffuse_board_one_particle(a_matrix, prey_diffusion_rate, kernel)
    b_diffused = diffuse_board_one_particle(b_matrix, predator_diffusion_rate, kernel)

    new_board = []
    for row in range(num_rows):
        new_board.append([])
        for col in range(num_cols):
            #add the updated cell to the new Board.
            new_board[row].append(update_cell(current_board, a_diffused, b_diffused, row, col, feed_rate, kill_rate))

    return new_board

def update_cell(current_board: Board, prey_diff_matrix: list[list[float]], pred_diff_matrix: list[list[float]],
    row: int, col: int, feed_rate: float, kill_rate: float) -> Cell:
    """
    Input: Current board, a board-sized matrix of the prey after one diffusion, a board-sized matrix of the predator after one diffusion,
    a (row, col) position of the cell, a feed rate, and a kill rate.
    Output: An updated cell where each element of the cell is a corresponding sum of the elements from the current cell at the (row, col)
    position, the cell returned from the diffusion, and the cell returned from the reaction.
    """
    current_cell = current_board[row][col]
    diffusion_values = change_due_to_diffusion(current_board, prey_diff_matrix, pred_diff_matrix, row, col)
    reaction_values = change_due_to_reactions(current_cell, feed_rate, kill_rate)
    return sum_cells(current_cell, diffusion_values, reaction_values)

def change_due_to_diffusion(current_board, a_diffused_matrix:list[list[float]], b_diffused_matrix:list[list[float]], row:int, col:int) -> Cell:
    """
    Input: A Board current_board, integers row and col,
    decimal variables prey_diffusion_rate and predator_diffusion_rate, and a 3 x 3 decimal matrix kernel.
    Output: A Cell variable storing the result of applying diffusion reactions with parameters
    prey_diffusion_rate, predator_diffusion_rate, and kernel to the Cell variable at current_board[row][col].
    """
    return (-(current_board[row][col][0] - a_diffused_matrix[row][col]), -(current_board[row][col][1] - b_diffused_matrix[row][col]))

def change_due_to_reactions(current_cell: Cell, feed_rate: float, kill_rate: float) -> Cell:
    """
    Input: a cell, a decimal feed rate: the rate of the feed reaction, and a decimal kill rate: the rate of the kill reaction.
    Output: A cell with the new (A,B) concentrations via the reactions.
    """
    feed_rxn_a = (feed_rate*(1-current_cell[0]))
    kill_rxn_b = (-kill_rate*(current_cell[1]))
    reprod_rxn = (current_cell[0] * (current_cell[1]**2))
    return (feed_rxn_a - reprod_rxn, kill_rxn_b  + reprod_rxn)

def diffuse_board_one_particle(current_board: list[list[float]], diffusion_rate: float, kernel: list[list[float]]) -> list[list[float]]:
    """
    Input: A two-dimensional array of decimal numbers current_board and a 3 × 3 matrix of decimal numbers kernel.
    Output: A two-dimensional array of decimal numbers new_board corresponding to applying
    one time step of diffusion to current_board using the scaled version of the input kernel.
    """
    scaled_kernel = scale_kernel(kernel, diffusion_rate) #scale kernel once per generation
    concentrations = []
    for i in range(len(current_board)):
        concentrations.append([])
        for j in range(len(current_board[i])):
            moore = make_moore(current_board, i, j) #get a moore neighborhood for the cell on (i,j).
            concentrations[i].append(current_board[i][j] + convolution(moore, scaled_kernel))

    return concentrations

def convolution(neighborhood: list[list[float]], kernel: list[list[float]]) -> float:
    """
    Input: Moore neighborhood and a kernel
    Output: Returns the convolution of the moore neighborhood with a kernel.
    """
    convolution = 0
    assert_3by3(neighborhood, kernel) #assert that the moore neighborhood and the kernel have the same dimensions.
    for i in range(len(neighborhood)):
        for j in range(len(neighborhood[i])):
            convolution += neighborhood[i][j] * kernel[i][j] #sum the products of the corresponding entries of the two matrices.

    return convolution

def scale_kernel(kernel: list[list[float]], diffusion_rate: float) -> list[list[float]]:
    """
    Input: kernel, diffusion rate
    Output: A kernel where every entry is scaled by the diffusion_rate constant
    """
    new_kernel = []
    for i in range(len(kernel)):
        new_kernel.append([])
        for j in range(len(kernel[i])):
            #scale each entry in the kernel by the diffusion rate
            new_kernel[i].append(kernel[i][j] * diffusion_rate)

    return new_kernel

def assert_3by3(neighborhood: list[list[float]], kernel: list[list[float]]):
    """
    Checks that the moore neighborhood and the kernel are both 3x3 matrices
    """
    if len(neighborhood) != len(kernel) or len(neighborhood[0]) != len(kernel[0]):
        raise ValueError("Moore neighborhood and kernel must be matrices of the same dimensions")

def make_moore(current_board: list[list[float]], row: int, col: int) -> list[list[float]]:
    """
    Input: an m x n matrix with float entries, a row position, and a column position
    Output: Returns the moore neighborhood of the entry at (row, col) in the input board.
    """
    neighborhood = []
    row_checks = [-1, 0, 1]
    col_checks = [-1, 0, 1]
    for i in row_checks:
        new_row = []
        for j in col_checks:
            #In this way, each moore neighbor of the cell at (row, col) is checked if it is inside the current board,
            #by using i and j as offsets from (row, col).
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
    return (0 <= row < len(current_board)) and (0 <= col < len(current_board[row]))

def sum_cells(*cells: Cell) -> Cell:
    """
    Input: some number of cells in the form of an array.
    Output: A cell whose elements are the sum of the corresponding elements of each of the cells in the input.
    """
    sum_a = 0
    sum_b = 0
    for cell in cells:
        sum_a += cell[0]
        sum_b += cell[1]

    return (sum_a, sum_b)

def initialize_board(num_rows: int, num_cols: int) -> Board:
    """
    Input: number of rows and cols to make the board
    Output: A board with num_rows rows and num_cols cols, with (1,1) in the center
    """
    board = []
    for i in range(num_rows):
        board.append([])
        for j in range(num_cols):
            board[i].append((0,0))

    #Set the middle cell as (1, 1)
    board[num_rows//2][num_cols//2] = (1, 1)
    return board

def count_rows(current_board: Board) -> int:
    #returns number of rows in the board
    return len(current_board)

def count_cols(current_board: Board) -> int:
    #returns number of columns in the first row
    return len(current_board[0])

def tuple_board_to_matrix(current_board: Board, particle: int) -> list[list[float]]:
    """
    Input: Takes a Board of tuples and a particle(0 if "prey"; 1 if "predator")
    Output: A matrix of floats with each element being the concentration of one single particle of the same type(A/B).
    """
    matrix = []
    for i in range(len(current_board)):
        matrix.append([])
        for j in range(len(current_board[i])):
            #append the desired particle from the current_board's cell at (i,j), to the matrix.
            matrix[i].append(current_board[i][j][particle])

    return matrix
