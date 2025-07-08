#!/bin/bash

# VRAM Capacity Test Script for GPU Benchmark v3

function vram_test() {
    echo "🎮 VRAM Capacity Test"
    echo "================================"

    if ! command -v nvidia-smi &> /dev/null; then
        echo "❌ Error: nvidia-smi is required but not installed"
        exit 1
    fi

    # Get VRAM details using nvidia-smi
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits |\
    while IFS=, read -r name vram;
    do
        echo "GPU: $name"
        echo "VRAM Capacity: ${vram} MB"
        echo "---"
    done

    echo "✅ VRAM capacity test completed"
}

vram_test
