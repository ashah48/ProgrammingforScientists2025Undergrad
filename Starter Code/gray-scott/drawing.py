from typing import List
from PIL import Image, ImageDraw
import matplotlib.cm as cm

from .datatypes import Board, Cell


def draw_boards(boards: List[Board], cell_width: int, n: int) -> List[Image.Image]:
    """
    Takes a list of Board objects as input along with a cell_width and n parameter.
    Returns a list of images corresponding to drawing every nth board,
    where each cell is cell_width x cell_width pixels.
    """
    image_list: List[Image.Image] = []
    for i, board in enumerate(boards):
        if i % n == 0:
            image_list.append(draw_board(board, cell_width))
    return image_list


def draw_board(board: Board, cell_width: int) -> Image.Image:
    """
    Draw a single Board object to an image.
    Each cell is cell_width x cell_width pixels.
    The color of a cell is based on predator / (predator + prey).
    """
    height = len(board) * cell_width
    width = len(board[0]) * cell_width

    # Start with a black canvas
    img = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(img)

    # Colormap similar to moreland.SmoothBlueRed()
    cmap = cm.get_cmap("RdBu_r")

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            prey = cell[0]
            predator = cell[1]

            val = predator / (predator + prey) if (predator + prey) > 0 else 0.0

            # Convert colormap value to RGB
            r, g, b, _ = [int(255 * x) for x in cmap(val)]

            x0 = j * cell_width
            y0 = i * cell_width
            x1 = x0 + cell_width
            y1 = y0 + cell_width

            draw.rectangle([x0, y0, x1, y1], fill=(r, g, b))

    return img
