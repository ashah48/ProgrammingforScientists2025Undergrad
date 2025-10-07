import pygame
import numpy as np

def main():
    print("Turing patterns and the Gray-Scott model.")

    # your code goes here

def pygame_surface_to_numpy(surface: pygame.Surface) -> np.ndarray:
    """
    Convert a Pygame Surface to a NumPy RGB image array.

    Returns:
        np.ndarray: The frame as (height, width, 3) uint8 RGB.
    """
    return pygame.surfarray.array3d(surface).swapaxes(0,1)

if __name__ == "__main__":
    main()
