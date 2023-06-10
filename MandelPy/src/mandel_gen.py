import multiprocessing.sharedctypes
from matplotlib import pyplot as plt
import numpy as np
import time

from typing import List, Tuple
from multiprocessing import Pool, shared_memory
from arg_parser import ArgParser


def mandel_test(c: complex, 
                max_iters: int) -> int:
    
    z: complex = complex(0, 0)

    for i in range(max_iters):
        if abs(z) > 2:
            return i
        z = z * z + c    
    return max_iters


def complex_matrix(xmin, xmax, 
                   ymin, ymax, 
                   pixel_density_x, 
                   pixel_density_y) : 
    """
    creates a complex matrix of size (pixel_density_x, pixel_density_y),
    which stored in shared memory

    """

    re = np.linspace(xmin, xmax, pixel_density_x)
    im = np.linspace(ymin, ymax, pixel_density_y)
    X, Y = np.meshgrid(re, im)  # Generate the meshgrid

    # Create the complex matrix
    complex_matrix = X + 1j * Y

    shm_c = multiprocessing.shared_memory.SharedMemory(name='ComplexMatrix', 
                                                       create=True, 
                                                       size=complex_matrix.nbytes)
    
    c = np.ndarray((pixel_density_y, pixel_density_x),
                    dtype=np.complex128,
                    buffer=shm_c.buf)
    
    np.copyto(c, complex_matrix)




    shm_c.close()

    return c.shape
    

def get_subproblems_cnt(granularity: int, 
                        parallelism: int) -> int:
    return granularity * parallelism


def get_step(subproblem_size: int, 
             parallelism: int) -> int:
    return subproblem_size * parallelism

def run(matrix_shape: Tuple, 
        p: int,
        id: int, 
        size: int, 
        num_iterations: int):

    shm = shared_memory.SharedMemory(name='MandelMatrix')
    shm_c = shared_memory.SharedMemory(name='ComplexMatrix')
    # map the shared memory to a numpy array
    res = np.ndarray(matrix_shape, dtype=np.int32, buffer=shm.buf) 
    matrix = np.ndarray(matrix_shape, dtype=np.complex128, buffer=shm_c.buf)
    #print(matrix)
    row_cnt = matrix_shape[0]
    rem = row_cnt % (size)
    #print (f"size: {size}, rem: {rem}, row_cnt: {row_cnt}")

    for i in range(id * size, row_cnt - rem, p * size):
        #print(f"i: {i}, i + size: {i + size}")
        for j in range(i, i + size):
            for k in range(len(matrix[j])):
                res[j][k] = mandel_test(matrix[j][k], num_iterations)
                #print(f"res[{j}][{k}] = {res[j][k]}")

    shm.close()

def parallel_check(xmin, xmax, 
                   ymin, ymax, 
                   pixel_density_x, 
                   pixel_density_y, 
                   num_iterations, 
                   granularity, 
                   parallelism) -> np.ndarray:

    matrix_shape = complex_matrix(xmin, xmax, 
                                  ymin, ymax, 
                                  pixel_density_x,
                                  pixel_density_y)
    

    res = np.zeros(matrix_shape, dtype=np.int32)
    shm = multiprocessing.shared_memory.SharedMemory(name='MandelMatrix', 
                                                     create=True, 
                                                     size=res.nbytes)
    shm_c = shared_memory.SharedMemory(name='ComplexMatrix')

    
    # shm = shared_memory.SharedMemory(name='MandelMatrix')

    # shm_c = multiprocessing.shared_memory.SharedMemory(name="ComplexMatrix", 
    #                                                    create=True, 
    #                                                    size=c.nbytes)
    
    # shm_c = shared_memory.SharedMemory(name="ComplexMatrix")


    shared_res = np.ndarray(matrix_shape, dtype=np.int32, buffer=shm.buf)
    np.copyto(shared_res, res)  

    start_time = time.perf_counter()
    cnt = granularity * parallelism
    size = matrix_shape[0] // cnt

    if parallelism > 1:
        pool = Pool(processes=parallelism - 1)
        params = [(matrix_shape, parallelism, i, size, num_iterations) 
                  for i in range(1, parallelism)]
        
        pool.starmap(run, params)
        pool.close()

        run(matrix_shape, parallelism, 0, size, num_iterations)

        pool.join()
    else:
        run(matrix_shape, parallelism, 0, size, num_iterations)

    end_time = time.perf_counter()

    print(f"Time taken: {end_time - start_time:0.4f} seconds")

    res = np.copy(shared_res)
    shm.close()
    shm.unlink()
    shm_c.close()
    shm_c.unlink()

    return res



class MandelbrotGenerator: 
    """
    MandelbrotGenerator computes and displays the Mandelbrot set
    """
    def __init__(self, granularity: int = 12, 
                       parallelism: int = 4, 
                       num_iterations: int = 256) -> None:
        
        self.pixel_density_x = 3840
        self.pixel_density_y = 2160
        
        self.num_iterations = num_iterations
        self.granularity = granularity
        self.parallelism = parallelism

        self.res = None

    @classmethod
    def from_parser(cls, parser: ArgParser) -> 'MandelbrotGenerator':
        return cls(parser.granularity, parser.parallelism, parser.iterations)
        

    def compute(self, xmin: float = -0.8, 
                      xmax: float = -0.3, 
                      ymin: float = 0.3, 
                      ymax: float = 0.8) -> None:
        
        self.res = parallel_check(xmin, xmax, ymin, ymax, 
                                  self.pixel_density_x, 
                                  self.pixel_density_y, 
                                  self.num_iterations, 
                                  self.granularity, 
                                  self.parallelism)

    def show(self) -> None:
        plt.imshow(self.res, 
                   extent=(-0.8, -0.3, 0.3, 0.8), 
                   cmap='rainbow_r', 
                   aspect='auto')
        plt.colorbar()
        plt.show()



if __name__ == "__main__":
    pass