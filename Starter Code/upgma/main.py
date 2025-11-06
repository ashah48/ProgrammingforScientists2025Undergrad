from functions import upgma
from io_util import read_matrix_from_file, write_newick_to_file


def main() -> None:
    print("Happy trees.")
    filename = "blah"
    mtx,species_names = read_matrix_from_file(filename)

    t = upgma(mtx, species_names)

    #write the tree to file so that we can visualize it
    # Classic example: everybody in the world needs to agree on how we write the tree to file
