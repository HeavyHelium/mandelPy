from arg_parser import ArgParser
from mandel_gen import MandelbrotGenerator



if __name__ == "__main__": 
    parser = ArgParser()
    m = MandelbrotGenerator.from_parser(parser)
    m.compute()
    #m.show()

