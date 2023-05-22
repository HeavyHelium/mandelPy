import argparse


class ArgParser:

    descriptions: dict[str, str] = {
        'overall': """ Generates the Mandelbrot set, 
         based on the given parameters, namely 
         granularity, parallelism, and the number of iterations.
         The resolution is fixed to 3840x2160.
         """,
        'granularity': 'The granularity of the subproblems',
        'parallelism': 'The number of workers to be used', 
        'iterations': 'The number of iterations to be used'
    }


    def __init__(self) -> None: 
        self.parser = argparse.ArgumentParser(description=ArgParser.descriptions['overall'])
        
        self.parser.add_argument('-g', '--granularity', type=int, 
                                 default=12, help=ArgParser.descriptions['granularity'])
        self.parser.add_argument('-p', '--parallelism', type=int, 
                                 default=4, help=ArgParser.descriptions['parallelism'])
        self.parser.add_argument('-i', '--iterations', type=int, 
                                 default=256, help=ArgParser.descriptions['iterations'])

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
