import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count

def mandelbrot(c, max_iters=100):
    z = c
    for i in range(max_iters):
        if abs(z) > 2:
            return i
        z = z*z + c
    return max_iters

def process_rows(args):
    rows, x, y, max_iters = args
    pixels = np.zeros((len(rows), len(x)))
    
    for i, row in enumerate(rows):
        for j, col in enumerate(x):
            pixels[i, j] = mandelbrot(complex(col, y[row]), max_iters)
    
    return pixels

def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iters=100, num_processes=None):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)

    if not num_processes:
        num_processes = cpu_count()

    pool = Pool(num_processes)

    # Use load balancing approach to distribute rows among processes
    chunk_size = int(np.ceil(height / num_processes))
    rows = [(range(i, min(i + chunk_size, height)), x, y, max_iters) for i in range(0, height, chunk_size)]
    results = pool.map(process_rows, rows)

    pool.close()
    pool.join()

    pixels = np.vstack(results)

    return pixels

# Example usage
xmin, xmax, ymin, ymax = -0.748, -0.746, 0.1, 0.102
width, height = 3840, 2160
max_iters = 256
num_processes = 8
pixels = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iters, num_processes)
plt.imshow(pixels, cmap='hot')
plt.show()
