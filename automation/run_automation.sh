#!/bin/bash

# Automated Design Upload Cron Job Script
# This script runs the Python automation to generate and upload designs

# Activate virtual environment (if using)
# source /path/to/venv/bin/activate

# Change to automation directory
cd "$(dirname "$0")"

# Run the Python script with random category
CATEGORIES=("Landing Page" "Dashboard" "E-commerce" "Portfolio" "Blog")
RANDOM_CATEGORY=${CATEGORIES[$RANDOM % ${#CATEGORIES[@]}]}

echo "Running automated design upload for category: $RANDOM_CATEGORY"
python upload_design.py --category "$RANDOM_CATEGORY"

# Log the execution
echo "[$(date)] Design upload completed for $RANDOM_CATEGORY" >> automation.log
