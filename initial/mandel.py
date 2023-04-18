import numpy as np
import matplotlib.pyplot as plt

def z(n, c):
    return 0 if n == 0 else z(n - 1, c) ** 2 + c

# tail recursion is not optimized in python


def sequence(c):
    # make use of lazy evaluation
    z = 0
    while True:
        yield z
        z = z ** 2 + c


def complex_matrix(xmin, xmax, ymin, ymax, pixel_density): 
    """
    returns a 2D array of complex numbers
    enclosed in a rectanlgular area 
    xmin, xmax: the bounds in the horizontal direction
    ymin, ymax: the bounds in the vertical direction
    pixel_density: the numbber of pixels per unit
    """
    re = np.linspace(xmin, xmax, int((xmax - xmin) * pixel_density))
    im = np.linspace(ymin, ymax, int((ymax - ymin) * pixel_density))

    return re[np.newaxis, :] + im[:, np.newaxis] * 1j

def is_stable(c, num_iterations): 
    """
    c: the numpy matrix of complex numbers
    num_iterations: the number of iterations to perform
    reuturns: a 2D mask of booleans indicating whether the sequence
    is stable or not at each point
    """
    z = 0
    for _ in range(num_iterations):
        z = z ** 2 + c
    
    return abs(z) < 2

def get_members(c, num_iterations): 
    """
    returns: stable complex numbers as a 1d numpy array
    """
    mask = is_stable(c, num_iterations)
    return c[mask]

  



if __name__ == "__main__":
    
    c = complex_matrix(-2, 1, -1, 1, 10000)
    stable = get_members(c, num_iterations=1000)
    plt.scatter(stable.real, stable.imag, s=0.1)
    plt.gca().set_aspect('equal')
    plt.tight_layout()
    plt.show()






