#!/bin/bash


# Check if script to run is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <script_to_run>"
  exit 1
fi

script_to_run="$1"


for ((i=1; i<=5; i++))
do
    echo "Running $script_to_run $i"
    output_file="results${i}.txt"

    bash "$script_to_run" > "$output_file"

    # lull
    sleep 10
done

