#!/bin/bash

# GPU Benchmark v3 - GPU Detection Tool
# Comprehensive GPU hardware detection and profiling

echo "GPU Benchmark v3 - GPU Detection Tool"
echo "======================================"

# Run the Python detection script
python3 detect_gpus.py

# Extract and display quick summary
if [ -f "gpu_detection_results.json" ]; then
    echo ""
    echo "SYSTEM SUMMARY:"
    echo "==============="
    TOTAL_GPUS=$(python3 -c "import json; data=json.load(open('gpu_detection_results.json')); print(data['total_gpus'])" 2>/dev/null)
    NVIDIA_GPUS=$(python3 -c "import json; data=json.load(open('gpu_detection_results.json')); print(len([g for g in data['gpu_info'] if g['vendor'] == 'NVIDIA']))" 2>/dev/null)
    OTHER_GPUS=$(python3 -c "import json; data=json.load(open('gpu_detection_results.json')); print(len([g for g in data['gpu_info'] if g['vendor'] != 'NVIDIA']))" 2>/dev/null)
    
    echo "Total GPUs: $TOTAL_GPUS"
    echo "NVIDIA GPUs: $NVIDIA_GPUS"
    echo "Other GPUs: $OTHER_GPUS"
fi
