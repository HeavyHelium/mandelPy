import multiprocessing
from matplotlib import pyplot as plt
import numpy as np
from typing import List
import time
from multiprocessing import Array, Process, Queue, Pool, RawArray, shared_memory
import multiprocessing.sharedctypes

def mandel_test(c: complex, 
                max_iters: int):
    
    z: complex = complex(0, 0)

    for i in range(max_iters):
        if abs(z) > 2:
            return i
        z = z * z + c    
    return max_iters


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



def get_workload(num_rows: int, workers: int) -> List[int]:
    """
    Returns a list of tuples, 
    where each tuple represents a range of rows
    to be processed by a worker
    """
    row_cnt_per_worker = num_rows // workers
    remaining_rows = num_rows % workers
    i = 0
    workload = [row_cnt_per_worker] * workers

    while remaining_rows: 
        workload[i] += 1
        remaining_rows -= 1
        i += 1

    return workload

#def run_worker(id_mod: int, )

def get_subproblems_cnt(granularity: int, 
                        parallelism: int) -> int:
    return granularity * parallelism


def get_step(subproblem_size: int, 
             parallelism: int) -> int:
    return subproblem_size * parallelism

def run(matrix: np.ndarray, 
        p: int,
        id: int, 
        size: int, 
        num_iterations: int):

    row_cnt = matrix.shape[0]
    rem = row_cnt % (size)

    shm = shared_memory.SharedMemory(name='my_shared_memory')
    res = np.ndarray(matrix.shape, dtype=np.int32, buffer=shm.buf)

    print (f"size: {size}, rem: {rem}, row_cnt: {row_cnt}")

    for i in range(id * size, row_cnt - rem, p * size):
        #print(f"i: {i}, i + size: {i + size}")
        for j in range(i, i + size):
            for k in range(len(matrix[j])):
                res[j][k] = mandel_test(matrix[j][k], num_iterations)
                #print(f"res[{j}][{k}] = {res[j][k]}")

    shm.close()

def parallel_check(xmin, xmax, ymin, ymax, 
                   pixel_density_x, pixel_density_y, 
                   num_iterations, granularity, parallelism):

    c = complex_matrix(xmin, xmax, ymin, ymax, pixel_density_x, pixel_density_y)
    res = np.zeros(c.shape, dtype=np.int32)  
    shm = multiprocessing.shared_memory.SharedMemory(name='my_shared_memory', create=True, size=res.nbytes)
    shared_res = np.ndarray(c.shape, dtype=np.int32, buffer=shm.buf)
    np.copyto(shared_res, res)  

    start_time = time.perf_counter()
    cnt = granularity * parallelism
    size = c.shape[0] // cnt


    pool = Pool(processes=parallelism - 1)
    params = [(c, parallelism, i, size, num_iterations) 
                for i in range(1, parallelism)]
    
    pool.starmap(run, params)
    pool.close()

    run(c, parallelism, 0, size, num_iterations)

    pool.join()
    

    end_time = time.perf_counter()

    print(f"Time taken: {end_time - start_time:0.4f} seconds")

    res = np.copy(shared_res)
    shm.close()
    shm.unlink()


    return res



if __name__ == "__main__": 
    pixel_density_x = 3840
    pixel_density_y = 2160
    num_iterations = 256

    granularity = 10
    parallelism = 3

    res = parallel_check(-0.8, -0.3, 0.3, 0.8, pixel_density_x, pixel_density_y, 
                         num_iterations, granularity, parallelism)

    print(res)

    plt.imshow(res, extent=(-0.8, -0.3, 0.3, 0.8), cmap='rainbow_r', aspect='auto')
    plt.colorbar()
    plt.show()

