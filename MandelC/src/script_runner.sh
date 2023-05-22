#!/bin/bash
# Check if script to run is provided as an argument
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <script_to_run> <result output dir>"
  exit 1
fi


script_to_run="$1"
output_dir="$2"

for ((i=1; i<=5; i++));
do
    echo "Running $script_to_run $i"
    output_file="$output_dir/results${i}.txt"

    bash "$script_to_run" > "$output_file"

    echo "Saved results to $output_file"

    # lull
    sleep 5
done

