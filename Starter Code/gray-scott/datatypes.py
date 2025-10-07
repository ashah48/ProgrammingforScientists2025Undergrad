# Cell contains two attributes corresponding to
# the concentration of predator (0-th element) and prey (1-th element) in the cell
Cell = tuple[float, float]

# Board is a two-dimensional slice of Cells
Board = list[list[Cell]]
