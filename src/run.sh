#!/bin/bash

# Loop through command line parameters from 1 to 4
for ((i = 1; i <= 4; i++)); do
    for j in 1 4 5 10 12; do
        echo "Running program with p = $i and g = $j"
        python3 parallel_static.py -p "$i" -g "$j"
        echo "Program execution completed"
        echo
        sleep 20
    done
    sleep 30
done

