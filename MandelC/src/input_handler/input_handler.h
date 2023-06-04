#include "../utils/utils.h"
#include "../mandel_generator/mandel_generator.h"
#include <string>

enum class Mode { 
    TEST, 
    RUN,
};

struct ArgParser { 
    ArgParser(int argc, char** argv);

    std::string output_file;
    int parallelism;
    int granularity;
    int max_iterations;
    ComplexArea area;
    Resolution resolution;
    Mode mode;
};

struct InputHandler { 
    InputHandler(int argc, char** argv, std::string output_file="../matrix.txt");

    void handle();

private: 
    ArgParser parser;
    std::string output_file;
};