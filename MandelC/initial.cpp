#include <iostream>
#include <vector>
#include <thread>
#include <utility>
#include <fstream>


const int width = 3840;
const int height = 2160;
const int max_iterations = 1000;

using Matrix = std::vector<std::vector<int>>;


struct Interval { 
    double min = 0;
    double max = 0;
};


struct ComplexArea { 
    Interval x;
    Interval y;

    friend std::ostream& operator<<(std::ostream& os, 
                                    const ComplexArea& c) { 
        os << c.x.min << " " << c.x.max << " ";
        os << c.y.min << " " << c.y.max << std::endl;
        
        return os;
    }
};


void generateMandelbrotRow(int row, 
                           Matrix& image, 
                           ComplexArea& area) {

    int width = image[0].size();
    int height = image.size();

    for(int col = 0; col < width; ++col) {

        double x0 = area.x.min + (area.x.max - area.x.min) * col / width;
        double y0 = area.y.min + (area.y.max - area.y.min) * row / height;

        double x = 0.0;
        double y = 0.0;
        int iterations = 0;

        // Escape time
        while(x * x + y * y < 4.0 && 
              iterations < max_iterations) {

            double xTemp = x * x - y * y + x0;
            y = 2.0 * x * y + y0;
            x = xTemp;
            ++iterations;
        }

        image[row][col] = iterations;
    }
}


void computeSet(Matrix& image, ComplexArea& area) { 
    for(int row = 0; row < height; ++row) { 
        generateMandelbrotRow(row, image, area);
    }
}



int main() { 

    ComplexArea area{Interval{-2, 1}, 
                     Interval{-1.5, 1.5}};    

    Matrix image(height, std::vector<int>(width));

    std::vector<std::thread> threads;



    computeSet(image, area);

    for(int row = 0; row < height; ++row) { 
        for(int col = 0; col < width; ++col)
            std::cout << image[row][col] << " ";
        std::cout << std::endl; 
    }

    std::ofstream file = std::ofstream("matrix.txt");

    file << width << " " << std::endl;
    file << area;

    for(int row = 0; row < height; ++row) {

        for(int col = 0; col < width; ++col)
            file << image[row][col] << " "; 
    }


    file.close();

    return 0;
}