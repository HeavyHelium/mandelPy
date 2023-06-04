#include "../utils/utils.h"
#include "../mandel_generator/mandel_generator.h"

struct ArgParser { 
    ArgParser(int argc, char** argv);

    std::string output_file;
    int parallelism;
    int granularity;
    int max_iterations;
    ComplexArea area;
    Resolution resolution;
};

struct InputHandler { 
    InputHandler(int argc, char** argv, std::string output_file="../matrix.txt");

    void handle();

private: 
    ArgParser parser;
    std::string output_file;
};