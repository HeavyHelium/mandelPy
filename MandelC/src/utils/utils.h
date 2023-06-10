#pragma once

#include <iostream>
#include <vector>
#include <string>


struct ThreadLog { 
    int id;
    signed long workload;

    bool operator<(const ThreadLog& other) const;

    friend std::ostream& operator<<(std::ostream& os, 
                                    const ThreadLog& tl);
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
                                    const ComplexArea& c);
};


template<typename T>
std::ostream& operator<<(std::ostream& os, 
                         const std::vector<T>& v) { 

    for(const auto& e: v) { 
        os << e;
    }
    return os << std::endl;
}
