#!/bin/bash

# GPU Detection Wrapper Script
# Part of GPU Benchmark v3

echo "🎮 GPU Benchmark v3 - GPU Detection Tool"
echo "========================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "detect_gpus.py" ]; then
    echo "❌ Error: detect_gpus.py not found in current directory"
    exit 1
fi

# Run the detection script
python3 detect_gpus.py "$@"

# Check if JSON file was created
if [ -f "gpu_detection_results.json" ]; then
    echo ""
    echo "📋 Quick Summary:"
    echo "=================="
    TOTAL_GPUS=$(python3 -c "import json; data=json.load(open('gpu_detection_results.json')); print(data['total_gpus'])")
    echo "Total GPUs: $TOTAL_GPUS"
    
    NVIDIA_GPUS=$(python3 -c "import json; data=json.load(open('gpu_detection_results.json')); print(len([g for g in data['gpu_info'] if g['vendor'] == 'NVIDIA']))")
    if [ "$NVIDIA_GPUS" -gt 0 ]; then
        echo "NVIDIA GPUs: $NVIDIA_GPUS"
    fi
    
    OTHER_GPUS=$(python3 -c "import json; data=json.load(open('gpu_detection_results.json')); print(len([g for g in data['gpu_info'] if g['vendor'] != 'NVIDIA']))")
    if [ "$OTHER_GPUS" -gt 0 ]; then
        echo "Other GPUs: $OTHER_GPUS"
    fi
fi
