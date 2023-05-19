from matplotlib import pyplot as plt
import numpy as np
from typing import List, Tuple
import time

"""
This is a simple implementation of the Mandelbrot set 
sequential generation algorithm.
"""

def mandel_test(c: complex, 
                max_iters: int):
    
    z: complex = complex(0, 0)

    for i in range(max_iters):
        if abs(z) > 2:
            return i
        z = z * z + c    
    return max_iters


def complex_matrix(xmin, xmax, ymin, ymax, pixel_density_x, pixel_density_y): 
    """
    returns a 2D array of complex numbers
    enclosed in a rectanlgular area 
    xmin, xmax: the bounds in the horizontal direction
    ymin, ymax: the bounds in the vertical direction
    pixel_density: the numbber of pixels per unit
    """
    re = np.linspace(xmin, xmax, int((xmax - xmin) * pixel_density_x))
    im = np.linspace(ymin, ymax, int((ymax - ymin) * pixel_density_y))

    return re[np.newaxis, :] + im[:, np.newaxis] * 1j


def seq_check(xmin, xmax, ymin, ymax, pixel_density_x, pixel_density_y, num_iterations): 
    """
    Runs the mandelbrot set test for a given complex matrix
    """
    c = complex_matrix(xmin, xmax, ymin, ymax, pixel_density_x, pixel_density_y)
    res = np.zeros(c.shape, dtype=int)   
    
    start_time = time.perf_counter()

    for i, row in enumerate(c):
        for j in range(len(row)):
            res[i][j] = mandel_test(row[j], num_iterations)

    end_time = time.perf_counter()

    print(f"Time taken: {end_time - start_time:0.4f} seconds")

    return res



  



if __name__ == "__main__":

    stable = seq_check(-0.8, -0.3, 0.3, 0.8, 3840, 2160, 256)
    plt.imshow(stable, extent=(-2, 1, -1, 1), cmap='rainbow_r', aspect='auto')
    plt.colorbar()
    plt.show()

      