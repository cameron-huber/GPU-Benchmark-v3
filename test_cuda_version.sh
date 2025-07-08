#!/bin/bash

# CUDA Version Test Script for GPU Benchmark v3

echo "CUDA Version Analysis"
echo "===================="

# Check if nvidia-smi is available
if ! command -v nvidia-smi &> /dev/null; then
    echo "ERROR: nvidia-smi not found"
    exit 1
fi

# Extract CUDA version from nvidia-smi
CUDA_VERSION=$(nvidia-smi | grep "CUDA Version" | awk '{print $9}')

if [ -n "$CUDA_VERSION" ]; then
    echo "CUDA Version: $CUDA_VERSION"
    
    # Get driver version too
    DRIVER_VERSION=$(nvidia-smi | grep "Driver Version" | awk '{print $6}')
    echo "Driver Version: $DRIVER_VERSION"
    
    # Check if nvcc is available for development
    if command -v nvcc &> /dev/null; then
        NVCC_VERSION=$(nvcc --version | grep "release" | awk '{print $6}' | cut -d',' -f1)
        echo "NVCC Version: $NVCC_VERSION"
    else
        echo "NOTE: NVCC not found (CUDA development tools not installed)"
    fi
else
    echo "ERROR: Could not detect CUDA version"
    exit 1
fi

echo "CUDA version analysis completed"
