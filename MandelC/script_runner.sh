#!/bin/bash
# Check if script to run is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <result output dir>"
  exit 1
fi

output_dir="$1"

for ((i=1; i<=5; i++));
do
    echo "Running $i"
    output_file="$output_dir/results${i}.txt"

    python3 run.py -m test > "$output_file"

    echo "Saved results to $output_file"

    # lull
    sleep 5
done

