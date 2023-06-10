#include "utils.h"


bool ThreadLog::operator<(const ThreadLog& other) const { 
    return id < other.id;
}

std::ostream& operator<<(std::ostream& os, 
                            const ThreadLog& tl) { 
    
    os << "(id: " << tl.id << ",  " << "time: " 
        << tl.workload << ")" << std::endl;
    return os;
}



std::ostream& operator<<(std::ostream& os, 
                                const ComplexArea& c) { 

    os << c.x.min << " " << c.x.max << " ";
    os << c.y.min << " " << c.y.max << std::endl;
    
    return os;
}
