import argparse
import os 
import multiprocessing
from vis import MandelSet

class ArgParser:

    descriptions: dict[str, str] = {
        'overall': """ Generates the Mandelbrot set, 
         based on the given parameters.
         """,
        'granularity': 'The granularity of the subproblems',
        'parallelism': 'The number of workers to be used', 
        'iterations': 'The number of iterations to be used',
        'area': 'The area of the complex plane to be investigated',
        'save': 'The output file to be used for the image',  
        'resolution': 'The resolution of the image to be generated',
        'mode': 'The mode to be used for the generation. Either test or gen.',
        'vis': 'To chose the way of visualization. Either cosine fractional mapping, i.e. cos or normal.'
    }


    def __init__(self) -> None: 
        self.parser = argparse.ArgumentParser(description=ArgParser.descriptions['overall'])

        self.parser.add_argument('-a', '--area', 
                                 metavar=('X_MIN', 'X_MAX', 'Y_MIN', 'Y_MAX'),
                                 type=float, nargs=4,
                                 default=[-2.5, 1, -1.5, 1.5], 
                                 help=ArgParser.descriptions['area'])

        self.parser.add_argument('-g', '--granularity', 
                                 type=int, default=12, 
                                 help=ArgParser.descriptions['granularity'])
        self.parser.add_argument('-p', '--parallelism', 
                                 type=int, default=4, 
                                 help=ArgParser.descriptions['parallelism'])
        
        self.parser.add_argument('-i', '--iterations', 
                                 type=int, default=256, 
                                 help=ArgParser.descriptions['iterations'])
        
        self.parser.add_argument('-r', '--resolution',
                                 metavar=('WIDTH', 'HEIGHT'), 
                                 type=int, nargs=2,
                                 default=[3840, 2160], 
                                 help=ArgParser.descriptions['resolution'])
        self.parser.add_argument('-m', '--mode', 
                                 type=str, default='gen', 
                                 help=ArgParser.descriptions['mode'])
        self.parser.add_argument('-v', '--vis',
                                 metavar=('TYPE'),
                                 type=str, default='normal',
                                 help=ArgParser.descriptions['vis'])

        self.parser.add_argument('-s', '--save',
                                 metavar=('FILENAME'),
                                 type=str, default='',
                                 help=ArgParser.descriptions['save'])

        self.args = self.parser.parse_args()
        
        if self.args.mode not in ['gen', 'test']:
            raise ValueError(f"Invalid mode: {self.args.mode}")
        
    @property
    def save(self) -> str:
        return self.args.save

    @property
    def vis(self) -> str:
        return self.args.vis

    @property
    def mode(self) -> str:
        return self.args.mode
    
    @property
    def granularity(self) -> int:
        return self.args.granularity
    
    @property
    def parallelism(self) -> int:
        return self.args.parallelism
    
    @property
    def iterations(self) -> int:
        return self.args.iterations
    
    @property
    def area(self) -> list[float]:
        return self.args.area

    
    @property
    def resolution(self) -> list[int]:
        return self.args.resolution
    
    
    def print_help(self) -> None:
        self.parser.print_help()

def to_nums(lst): 
    return " ".join(str(elem) for elem in lst)

class MandelbrotRunner: 
    def __init__(self, args: ArgParser) -> None:
        self.args = args

    def run(self) -> None:
        if self.args.mode == 'test':
            for g in [1, 4, 16]:
                for p in range(1, multiprocessing.cpu_count() + 1):
                    os.system(f"bash -c 'g++ src/main.cpp src/utils/utils.cpp src/mandel_generator/mandel_generator.cpp\
                                src/input_handler/input_handler.cpp -std=c++17 -pthread && \
                                ./a.out {p} {g} {to_nums(self.args.area)} {to_nums(self.args.resolution)} \
                                {self.args.iterations} test'")

        else:
            os.system(f"bash -c 'g++ src/main.cpp src/utils/utils.cpp src/mandel_generator/mandel_generator.cpp\
                        src/input_handler/input_handler.cpp -std=c++17 -pthread && \
                        ./a.out {self.args.parallelism} {self.args.parallelism} \
                                {to_nums(self.args.area)} {to_nums(self.args.resolution)} \
                                {self.args.iterations} run'")
            if self.args.vis == 'cos':
                m = MandelSet(cos_mapping=True)
                if self.args.save:
                    m.save(self.args.save)
                m.show()
            else: 
                m = MandelSet()
                if self.args.save:
                    m.save(self.args.save)
                m.show()
            
            os.system("bash -c 'rm matrix.txt'")
        
        os.system("bash -c 'rm a.out'")
        

if __name__ == "__main__": 
    MandelbrotRunner(ArgParser()).run()
