#!/bin/bash

for j in 1 2 4 8 16 32; do
    for ((i = 1; i <= 4; i++)); do
        echo "Running program with p = $i and g = $j"
        g++ main.cpp utils/utils.cpp mandel_generator/mandel_generator.cpp input_handler/input_handler.cpp -std=c++17 -pthread && ./a.out "$i" "$j"
        echo "Program execution completed"
        echo
    done
    sleep 5
done

