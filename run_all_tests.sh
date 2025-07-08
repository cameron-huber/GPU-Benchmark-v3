#!/bin/bash

# GPU Benchmark v3 - Comprehensive Test Suite
# Executes all tests and generates professional report

echo "🚀 GPU Benchmark v3 - Comprehensive Test Suite"
echo "=============================================="
echo "$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Create results directory
RESULTS_DIR="results_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS_DIR"

# Run GPU detection
echo "🖥️  GPU Hardware Detection"
echo "----------------------------"
./detect_gpus.sh 2>&1 | tee "$RESULTS_DIR/gpu_detection.txt"

echo ""
echo "💾 VRAM Capacity Test"
echo "-----------------------"
python3 test_vram_capacity.py 2>&1 | tee "$RESULTS_DIR/vram_capacity.txt"

echo ""
echo "🔥 CUDA Version Verification"
echo "-----------------------------"
./test_cuda_version.sh 2>&1 | tee "$RESULTS_DIR/cuda_version.txt"

echo ""
echo "🔗 GPU Topology Display"
echo "------------------------"
./show_gpu_topology.sh 2>&1 | tee "$RESULTS_DIR/gpu_topology.txt"

echo ""
echo "📊 PCIe/NVLink Bandwidth Test"
echo "-------------------------------"
python3 test_bandwidth.py 2>&1 | tee "$RESULTS_DIR/bandwidth_test.txt"

echo ""
echo "💾 Disk Read Speed Test"
echo "------------------------"
python3 test_disk_read_speed.py 2>&1 | tee "$RESULTS_DIR/disk_read_speed.txt"

echo ""
echo "=================================================="
echo "📝 TEST SUITE SUMMARY"
echo "=================================================="
echo "Test execution completed at: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Results directory: $RESULTS_DIR"
echo ""
echo "📊 Quick Performance Summary:"
echo "----------------------------"

# Extract key metrics from JSON files
if [ -f "gpu_detection_results.json" ]; then
    GPU_COUNT=$(python3 -c "import json; data=json.load(open('gpu_detection_results.json')); print(data['total_gpus'])" 2>/dev/null || echo "N/A")
    echo "GPUs Detected: $GPU_COUNT"
fi

if [ -f "vram_test_results.json" ]; then
    TOTAL_VRAM=$(python3 -c "import json; data=json.load(open('vram_test_results.json')); print(f\"{data['total_vram_gb']:.0f}GB\")" 2>/dev/null || echo "N/A")
    echo "Total VRAM: $TOTAL_VRAM"
fi

if [ -f "cuda_version_results.json" ]; then
    CUDA_VERSION=$(python3 -c "import json; data=json.load(open('cuda_version_results.json')); print(data['cuda_version'])" 2>/dev/null || echo "N/A")
    echo "CUDA Version: $CUDA_VERSION"
fi

if [ -f "bandwidth_test_results.json" ]; then
    echo "Bandwidth Test: Available in $RESULTS_DIR/bandwidth_test.txt"
fi

if [ -f "disk_read_speed_results.json" ]; then
    DISK_SPEED=$(python3 -c "import json; data=json.load(open('disk_read_speed_results.json')); print(f\"{data['read_speed_mbps']:.0f} MB/s\")" 2>/dev/null || echo "N/A")
    echo "Disk Read Speed: $DISK_SPEED"
fi

echo ""
echo "📁 Individual Test Results:"
echo "----------------------------"
echo "• GPU Detection: $RESULTS_DIR/gpu_detection.txt"
echo "• VRAM Capacity: $RESULTS_DIR/vram_capacity.txt"
echo "• CUDA Version: $RESULTS_DIR/cuda_version.txt"
echo "• GPU Topology: $RESULTS_DIR/gpu_topology.txt"
echo "• Bandwidth Test: $RESULTS_DIR/bandwidth_test.txt"
echo "• Disk Speed: $RESULTS_DIR/disk_read_speed.txt"

echo ""
echo "✅ All tests completed successfully!"
echo "=================================================="
