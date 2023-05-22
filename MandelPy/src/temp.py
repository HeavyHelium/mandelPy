from multiprocessing import shared_memory

import numpy as np

def mandel_test(c: complex, 
                max_iters: int) -> int:
    
    z: complex = complex(0, 0)

    for i in range(max_iters):
        if abs(z) > 2:
            return i
        z = z * z + c    
    return max_iters

def run(matrix: np.ndarray):

    row_cnt = matrix.shape[0]

    shm = shared_memory.SharedMemory(name='MandelMatrix')
    res = np.ndarray(matrix.shape, dtype=np.int32, buffer=shm.buf) # map the shared memory to a numpy array

    shm.close()

def complex_matrix(xmin, xmax, 
                   ymin, ymax, 
                   pixel_density_x, 
                   pixel_density_y) -> np.ndarray: 
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



if __name__ == "__main__":
    c = complex_matrix(-0.8,-0.3, 0.3, 0.8, 3840, 2160)   
    run(c)
