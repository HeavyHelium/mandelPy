#include <iostream>
#include "input_handler/input_handler.h"


int main(int argc, char** argv) { 

    InputHandler ih(argc, argv);
    ih.handle();
    
    std::cout << "Done!" << std::endl;
    

    return 0;
}