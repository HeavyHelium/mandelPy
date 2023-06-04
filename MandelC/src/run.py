import argparse
import os 


class ArgParser:

    descriptions: dict[str, str] = {
        'overall': """ Generates the Mandelbrot set, 
         based on the given parameters, namely 
         granularity, parallelism, and the number of iterations.
         The resolution is fixed to 3840x2160.
         """,
        'granularity': 'The granularity of the subproblems',
        'parallelism': 'The number of workers to be used', 
        'iterations': 'The number of iterations to be used',
        'area': 'The area of the complex plane to be used,\n in the format: x_min x_max y_min y_max',
        'output': 'The output file to be used for the image', 
        'resolution': 'The resolution of the image to be generated, in the format: width height',
    }


    def __init__(self) -> None: 
        self.parser = argparse.ArgumentParser(description=ArgParser.descriptions['overall'])
        
        self.parser.add_argument('-g', '--granularity', type=int, 
                                 default=12, help=ArgParser.descriptions['granularity'])
        self.parser.add_argument('-p', '--parallelism', type=int, 
                                 default=4, help=ArgParser.descriptions['parallelism'])
        self.parser.add_argument('-i', '--iterations', type=int, 
                                 default=256, help=ArgParser.descriptions['iterations'])
        
        self.parser.add_argument('-a', '--area', type=float, nargs=4,
                                  default=[-2.5, 1, -1.5, 1.5], help=ArgParser.descriptions['area'])
        self.parser.add_argument('-o', '--output', type=str,
                                 default=os.path.join(os.getcwd(), 'mandel_res.png'), 
                                 help=ArgParser.descriptions['output'])
        self.parser.add_argument('-r', '--resolution', type=int, nargs=2,
                                  default=[3840, 2160], help=ArgParser.descriptions['resolution'])

        self.args = self.parser.parse_args()
    
    @property
    def granularity(self) -> int:
        return self.args.granularity
    
    @property
    def parallelism(self) -> int:
        return self.args.parallelism
    
    @property
    def iterations(self) -> int:
        return self.args.iterations
    
    def print_help(self) -> None:
        self.parser.print_help()

"""
TODO: implement class to run the c++ code 
modify the c++ code to accept the arguments
"""

if __name__ == "__main__": 
    arg_parser = ArgParser()
