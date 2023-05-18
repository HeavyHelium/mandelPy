
from multiprocessing import Array, Process, Queue, Pool, RawArray, shared_memory
import multiprocessing.sharedctypes


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


c = complex_matrix(xmin, xmax, ymin, ymax, pixel_density_x, pixel_density_y)
res = np.zeros(c.shape, dtype=np.int32)  
shm = multiprocessing.shared_memory.SharedMemory(name='my_shared_memory', create=True, size=res.nbytes)



shm.close()
shm.unlink()


   
