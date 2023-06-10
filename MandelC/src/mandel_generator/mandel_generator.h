#include "../utils/utils.h"

void generateMandelbrotRow(int row, 
                           Matrix& image, 
                           ComplexArea& area, 
                           int max_iterations = 256);


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
                int max_iterations = 256);


void computeSet(Matrix& image, 
                ComplexArea& area, 
                Workloads& workloads,
                int num_workers = 4, 
                int granularity = 10, 
                int max_iterations = 256);



struct MandelGenerator { 

    MandelGenerator(Resolution res, 
                    ComplexArea area,
                    int parallelism = 4, 
                    int granularity = 10, 
                    int max_iterations = 256);

    const Workloads& get_workloads() const;


    int subtasks_cnt() const;

    friend std::ostream& operator<<(std::ostream& os, 
                                    const MandelGenerator& mg);

private: 
    void sort_workloads_by_id();


    Matrix image;
    ComplexArea area;
    Workloads workloads;
    std::vector<double> thread_workload;
    int parallelism;
    int granularity;
};