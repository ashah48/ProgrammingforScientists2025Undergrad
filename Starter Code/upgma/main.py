from functions import upgma
from io_util import read_matrix_from_file, write_newick_to_file


def main() -> None:
    print("Happy trees.")
    v = Node(num=2, age=3.0, label = "New node")
    print(v)
