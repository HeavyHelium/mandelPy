import numpy as np
from PIL import Image
from scipy.interpolate import interp1d
from dataclasses import dataclass


def flatten(lst): 
    return [item for sublist in lst for item in sublist]

@dataclass
class ComplexArea:
    x_min: float = 0
    x_max: float = 0
    y_min: float = 0
    y_max: float = 0

@dataclass
class MandelSet: 
    complex_area: ComplexArea
    matrix: list[list[int]]

    def __init__(self): 
        self.__parse_file()

    def __parse_file(self, filename="../../matrix.txt"):
        with open(filename, 'r') as file:
            
            width = int(file.readline())
            x_min, x_max, y_min, y_max = map(float, file.readline().split())
            
            self.complex_area = ComplexArea(x_min, x_max, y_min, y_max)
            
            data = [int(x) for x in file.readline().split()]
            
        self.matrix = [data[i:i+width] for i in range(0, len(data), width)]


def create_gradient(iterations, colors):
    min_value = np.min(iterations)
    max_value = np.max(iterations)

    gradient = make_gradient(colors, interpolation="cubic")
    palette = denormalize(
        [gradient((value - min_value) / (max_value - min_value)) for value in np.ravel(iterations)]
    )

    # Reshape the palette back to the original shape of the iterations matrix
    palette = np.array(palette).reshape(iterations.shape + (3,))

    return Image.fromarray((palette * 255).astype(np.uint8))

def denormalize(palette):
    return [
        tuple(int(channel * 255) for channel in color) for color in palette
    ]


def make_gradient(colors, interpolation="linear"):
    X = [i / (len(colors) - 1) for i in range(len(colors))]
    Y = [[color[i] for color in colors] for i in range(3)]
    channels = [interp1d(X, y, kind=interpolation) for y in Y]
    return lambda x: [np.clip(channel(x), 0, 1) for channel in channels]


if __name__ == "__main__":
    #print(flatten([[1, 2, 3], [4, 2, 8]]))


    print("This might take a while...")

    colors = [(1, 0, 0), (1, 0.5, 0),
              (1, 1, 0), (0, 1, 0),
              (0, 0.5, 1), (0.5, 0, 1)]
    
    mand = MandelSet()
    image1 = np.array(mand.matrix)
    image = create_gradient(image1, colors)
    image.save("mandelbrot.png")    
