#!/bin/bash

# GPU Topology Display - GPU Benchmark v3
# Professional GPU interconnection topology analysis

echo "GPU Topology Analysis"
echo "===================="

# Check if nvidia-smi is available
if ! command -v nvidia-smi &> /dev/null; then
    echo "ERROR: nvidia-smi not found"
    exit 1
fi

echo "GPU Topology Matrix:"
echo "--------------------"

# Run nvidia-smi topology
nvidia-smi topo -m

echo ""
echo "Topology analysis completed"
