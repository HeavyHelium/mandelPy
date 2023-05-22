#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <utility>
#include <fstream>
#include <chrono>


using Matrix = std::vector<std::vector<int>>;

struct Resolution { 
    int height = 0;
    int width = 0;
};


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
                           ComplexArea& area, 
                           int max_iterations = 256) {

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


/*
@brief:
    Each woker takes a chunck of rows and computes them.
    The chunck size is determined by the granularity parameter.
    The distribution is cyclic.
*/

void run_worker(Matrix& image, 
                ComplexArea& area,
                int id, 
                int size, 
                int num_workers) {
    
    int num_rows = image.size();

    for(int i = id * size; i < num_rows; i += num_workers * size) { 
        for (int j = 0; j < size; ++j) { 
            generateMandelbrotRow(i + j, image, area);
        }
    }
}




void computeSet(Matrix& image, 
                ComplexArea& area, 
                int num_workers = 4, 
                int granularity = 10) { 
    int width = image[0].size();
    int height = image.size();

    int size = height / (num_workers * granularity);

    std::vector<std::thread> threads;
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    for(int i = 1; i < num_workers; ++i) { 
        threads.emplace_back(run_worker, 
                             std::ref(image), 
                             std::ref(area), 
                             i, 
                             size, 
                             num_workers);
    }

    run_worker(image, area, 0, size, num_workers);

    for(auto& t : threads) { 
        t.join();
    }

    auto end_time = std::chrono::high_resolution_clock::now();

    std::cout << "Execution time: " 
              << std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count() 
              << " ms" << std::endl;
}





struct MandelGenerator { 
    MandelGenerator(Resolution res, 
                    ComplexArea area,
                    int parallelism = 4, 
                    int granularity = 10) 
    : image(res.height, std::vector<int>(res.width)), 
      area(area), 
      parallelism(parallelism),
      granularity(granularity) {

        computeSet(image, area, parallelism, granularity); 
    }

    int subtasks_cnt() const { 
        return parallelism * granularity;
    }

    friend std::ostream& operator<<(std::ostream& os, 
                                    const MandelGenerator& mg) { 
        os << mg.image[0].size() << std::endl;
        os << mg.area;

        for(int row = 0; row < mg.image.size(); ++row) { 
            for(int col = 0; col < mg.image[0].size(); ++col) { 
                os << mg.image[row][col] << " ";
            }
        }

        return os << std::endl;
    }


private: 
        Matrix image;
        ComplexArea area;
        int parallelism;
        int granularity;
};


struct ArgParser { 
    ArgParser(int argc, char** argv) { 
        if(argc < 2) { 
            std::cout << "Usage: " << argv[0] << " <output_file>" << std::endl;
            exit(1);
        }

        output_file = argv[1];
    }

    std::string output_file;
};


int main(int argc, char** argv) { 

    // const int width = 3840;
    // const int height = 2160;
    const int width = 7680;
    const int height = 4320;

    const int max_iterations = 1000;

    ComplexArea area{Interval{-2, 1}, 
                     Interval{-1.5, 1.5}};

    int parallelsim = 4;
    int granularity = 10;


    if(argc != 3) { 
        std::cerr << "Usage: " << argv[0] << " <parallelism> <granularity>\n\n" << std::endl;
        exit(1);
    }

    parallelsim = std::stoi(argv[1]);
    granularity = std::stoi(argv[2]);
    

    MandelGenerator mg(Resolution{height, width}, 
                       area, 
                       parallelsim, 
                       granularity);

    std::ofstream file = std::ofstream("matrix.txt");

    file << mg;


    file.close();

    std::cout << "Done!" << std::endl;

    return 0;
}