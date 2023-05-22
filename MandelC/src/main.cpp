#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <utility>
#include <fstream>
#include <chrono>
#include <algorithm>

// TODO: Add an std::vector<int> for computational time 
// for each worker 

struct ThreadLog { 
    int id;
    signed long workload;

    bool operator<(const ThreadLog& other) const { 
        return id < other.id;
    }

    friend std::ostream& operator<<(std::ostream& os, 
                                    const ThreadLog& tl) { 
        
        os << "(id: " << tl.id << ",  " << "time: " 
           << tl.workload << ")" << std::endl;
        return os;
    }
};


using Matrix = std::vector<std::vector<int>>;
using Workloads = std::vector<ThreadLog>;


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

template<typename T>
std::ostream& operator<<(std::ostream& os, 
                        const std::vector<T>& v) { 

    for(const auto& e: v) { 
        os << e;
    }
    return os << std::endl;
}


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
                Workloads& workloads, 
                int id, 
                int size, 
                int num_workers, 
                int max_iterations = 256) {

    auto start_time = std::chrono::high_resolution_clock::now();     
    
    int num_rows = image.size();

    for(int i = id * size; 
            i + size <= num_rows; 
            i += num_workers * size) { 
        
        for (int j = 0; j < size; ++j) { 
            generateMandelbrotRow(i + j, image, 
                                  area, max_iterations);
        }
    }

    auto end_time = std::chrono::high_resolution_clock::now();

    workloads.push_back(ThreadLog{id, 
                                  std::chrono::duration_cast<std::chrono::milliseconds>(
                                  end_time - start_time).count()});
    
}




void computeSet(Matrix& image, 
                ComplexArea& area, 
                Workloads& workloads,
                int num_workers = 4, 
                int granularity = 10, 
                int max_iterations = 256) { 

    int width = image[0].size();
    int height = image.size();

    int size = height / (num_workers * granularity);

    std::vector<std::thread> threads;
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    for(int i = 1; i < num_workers; ++i) { 
        threads.emplace_back(run_worker, 
                             std::ref(image), 
                             std::ref(area), 
                             std::ref(workloads),
                             i, 
                             size, 
                             num_workers, 
                             max_iterations);
    }

    run_worker(image, 
               area, 
               workloads, 
               0, 
               size, 
               num_workers, 
               max_iterations);

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
                    int granularity = 10, 
                    int max_iterations = 256) 
    : image(res.height, std::vector<int>(res.width)), 
      area(area), 
      parallelism(parallelism),
      granularity(granularity) {

        computeSet(image, area, workloads, parallelism, granularity, max_iterations); 
        sort_workloads_by_id();
    }

    const Workloads& get_workloads() const { 
        return workloads;
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
    void sort_workloads_by_id() { 
        std::sort(workloads.begin(), workloads.end());
    }



    Matrix image;
    ComplexArea area;
    Workloads workloads;
    std::vector<double> thread_workload;
    int parallelism;
    int granularity;
};


struct ArgParser { 
    ArgParser(int argc, char** argv)
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


    std::string output_file;
    int parallelism;
    int granularity;
    int max_iterations;
    ComplexArea area;
    Resolution resolution;
};

struct InputHandler { 
    InputHandler(int argc, char** argv, std::string output_file="../matrix.txt"): 
        parser(argc, argv), 
        output_file(output_file) {
    }

    void handle() { 
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

private: 
    ArgParser parser;
    std::string output_file;
};


int main(int argc, char** argv) { 

    InputHandler ih(argc, argv);
    ih.handle();
    
    std::cout << "Done!" << std::endl;

    return 0;
}