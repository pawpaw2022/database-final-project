#!/bin/bash

echo "Starting MySQL container..."
docker start mysql-oracle
if [ $? -ne 0 ]; then
    echo "Error: Failed to start MySQL container"
    exit 1
fi

echo "Waiting for MySQL to be ready..."
sleep 5  # Give MySQL some time to start up

echo "Activating conda environment..."
# Source conda for bash shell
source ~/miniconda3/etc/profile.d/conda.sh
# Activate the environment
conda activate database
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate conda environment 'database'"
    exit 1
fi

echo "Starting Streamlit application..."
streamlit run app.py

# Note: The script will wait here while Streamlit is running
# When Streamlit is closed, we'll clean up

echo "Application closed. Cleaning up..."
# Optionally stop MySQL container when done
# docker stop mysql

echo "Done!" 