#include "input_handler.h"
#include <fstream>
#include <cstring>

ArgParser::ArgParser(int argc, char** argv)
:area(ComplexArea{Interval{-2, 1}, 
                    Interval{-1.5, 1.5}}),
    resolution(Resolution{2160, 3840}), 
    max_iterations(40) {

    if(argc != 11) { 
        std::cerr << "Usage: " << argv[0] << 
                    " <parallelism> <granularity> <complex area> \
                    <resolution> <max_iterations> <output_file>\n\n" << std::endl;
        
        throw std::invalid_argument("Invalid number of arguments");
    } 

    parallelism = std::stoi(argv[1]);
    granularity = std::stoi(argv[2]);
    area = ComplexArea{{std::stod(argv[3]), std::stod(argv[4])}, 
                        {std::stod(argv[5]), std::stod(argv[6])}};

    resolution = Resolution{std::stoi(argv[7]), std::stoi(argv[8])};
    max_iterations = std::stoi(argv[9]);
    
    if(std::strcmp(argv[10], "test") == 0) { 
        mode = Mode::TEST;
    } else if(std::strcmp(argv[10], "run") == 0) { 
        mode = Mode::RUN;
    } else { 
        std::cerr << "Invalid mode: " << argv[11] << std::endl;
        throw std::invalid_argument("Invalid mode");
    }

}

 
InputHandler::InputHandler(int argc, char** argv, std::string output_file): 
    parser(argc, argv), 
    output_file(output_file) {
}

void InputHandler::handle() { 
    std::ofstream out;
    if(parser.mode == Mode::TEST) { 
        std::cout << "\nTesting..." << std::endl;
        
        std::cout << "Running with p = " 
                  << parser.parallelism << ", g = " 
                  << parser.granularity << std::endl;    
        
    } else {
        out.open(output_file); 
        std::cout << "\nRunning..." << std::endl;
    }

    MandelGenerator mg(parser.resolution, 
                        parser.area, 
                        parser.parallelism, 
                        parser.granularity, 
                        parser.max_iterations);

    if(parser.mode == Mode::RUN) { 
        std::cout << "Writing to " << output_file << std::endl;
        out << mg;
        out.close();
    } else {
        std::cout << "Workloads:\n" << mg.get_workloads();
    }

}
