from matplotlib import pyplot as plt
from dataclasses import dataclass

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

    def __parse_file(self, filename="../matrix.txt"):
        with open(filename, 'r') as file:
            
            width = int(file.readline())
            x_min, x_max, y_min, y_max = map(float, file.readline().split())
            
            self.complex_area = ComplexArea(x_min, x_max, y_min, y_max)
            
            data = [int(x) for x in file.readline().split()]
            
        self.matrix = [data[i:i+width] for i in range(0, len(data), width)]
    

    def show(self) -> None:
        plt.imshow(self.matrix,
                   extent = (self.complex_area.x_min, 
                             self.complex_area.x_max, 
                             self.complex_area.y_min, 
                             self.complex_area.y_max),
                   cmap='rainbow_r',
                   aspect='auto')
        plt.colorbar()
        plt.show()





if __name__ == "__main__":
    mandel_set = MandelSet()
    mandel_set.show()