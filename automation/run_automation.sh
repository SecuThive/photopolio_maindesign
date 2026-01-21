#!/bin/bash

# Automated Design Upload Cron Job Script
# This script runs the Python automation to generate and upload designs

# Activate virtual environment (if using)
# source /path/to/venv/bin/activate

# Change to automation directory
cd "$(dirname "$0")"

# Run the Python script 10 times with random categories
CATEGORIES=("Landing Page" "Dashboard" "E-commerce" "Portfolio" "Blog")
TOTAL_RUNS=10

for ((i = 1; i <= TOTAL_RUNS; i++)); do
	RANDOM_CATEGORY=${CATEGORIES[$RANDOM % ${#CATEGORIES[@]}]}
	echo "Running automated design upload $i/$TOTAL_RUNS for category: $RANDOM_CATEGORY"
	python upload_design.py --category "$RANDOM_CATEGORY"
	echo "[$(date)] Design upload $i/$TOTAL_RUNS completed for $RANDOM_CATEGORY" >> automation.log
done

echo "All $TOTAL_RUNS uploads completed."
