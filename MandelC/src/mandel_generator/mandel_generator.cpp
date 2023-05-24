#include "mandel_generator.h"
#include <chrono>
#include <algorithm>
#include <thread>

void generateMandelbrotRow(int row, 
                           Matrix& image, 
                           ComplexArea& area, 
                           int max_iterations) {

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
    Each worker takes a bunch of rows and computes 
    the mandelbrot set for each row.
    The distribution is cyclic.
*/

void run_worker(Matrix& image, 
                ComplexArea& area,
                Workloads& workloads, 
                int id, 
                int size, 
                int num_workers, 
                int max_iterations) {

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
                int num_workers, 
                int granularity, 
                int max_iterations) { 

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



MandelGenerator::MandelGenerator(Resolution res, 
                                 ComplexArea area,
                                 int parallelism, 
                                 int granularity, 
                                 int max_iterations) 
: image(res.height, std::vector<int>(res.width)), 
    area(area), 
    parallelism(parallelism),
    granularity(granularity) {

    computeSet(image, area, workloads, parallelism, granularity, max_iterations); 
    sort_workloads_by_id();
}

const Workloads& MandelGenerator::get_workloads() const { 
    return workloads;
}


int MandelGenerator::subtasks_cnt() const { 
    return parallelism * granularity;
}

std::ostream& operator<<(std::ostream& os, 
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



void MandelGenerator::sort_workloads_by_id() { 
    std::sort(workloads.begin(), workloads.end());
}
