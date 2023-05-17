#!/bin/bash

# Loop through command line parameters from 1 to 4
for ((i = 1; i <= 4; i++)); do
    echo "Running program with parameter $i"
    python3 parallel_static.py "$i" 
    echo "Program execution with parameter $i completed"
    echo
done

