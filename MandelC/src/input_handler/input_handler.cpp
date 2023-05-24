#include "input_handler.h"
#include <fstream>


ArgParser::ArgParser(int argc, char** argv)
:area(ComplexArea{Interval{-2, 1}, 
                    Interval{-1.5, 1.5}}),
    resolution(Resolution{4320, 7680}), 
    max_iterations(256) {

    if(argc != 3) { 
        std::cerr << "Usage: " << argv[0] << 
                    " <parallelism> <granularity>\n\n" << std::endl;
        throw std::invalid_argument("Invalid number of arguments");
    } 

    parallelism = std::stoi(argv[1]);
    granularity = std::stoi(argv[2]);

}

 
InputHandler::InputHandler(int argc, char** argv, std::string output_file): 
    parser(argc, argv), 
    output_file(output_file) {
}

void InputHandler::handle() { 
    MandelGenerator mg(parser.resolution, 
                        parser.area, 
                        parser.parallelism, 
                        parser.granularity, 
                        parser.max_iterations);

    std::ofstream out(output_file);
    
    out << mg;
    out.close();

    std::cout << "Workloads:\n" << mg.get_workloads();
}
