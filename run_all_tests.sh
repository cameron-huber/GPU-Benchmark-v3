#!/bin/bash

# GPU Benchmark v3 - Comprehensive Test Suite
# Professional GPU and System Performance Analysis

echo "GPU Benchmark v3 - Comprehensive Test Suite"
echo "==========================================="
echo "Test execution started: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Create results directory
RESULTS_DIR="results_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS_DIR"

# Run GPU detection
echo "[1/6] GPU Hardware Detection"
echo "-----------------------------"
./detect_gpus.sh 2>&1 | tee "$RESULTS_DIR/gpu_detection.txt"

echo ""
echo "[2/6] VRAM Capacity Analysis"
echo "-----------------------------"
python3 test_vram_capacity.py 2>&1 | tee "$RESULTS_DIR/vram_capacity.txt"

echo ""
echo "[3/6] CUDA Version Verification"
echo "--------------------------------"
./test_cuda_version.sh 2>&1 | tee "$RESULTS_DIR/cuda_version.txt"

echo ""
echo "[4/6] GPU Topology Analysis"
echo "----------------------------"
./show_gpu_topology.sh 2>&1 | tee "$RESULTS_DIR/gpu_topology.txt"

echo ""
echo "[5/6] PCIe/NVLink Bandwidth Testing"
echo "------------------------------------"
python3 test_bandwidth.py 2>&1 | tee "$RESULTS_DIR/bandwidth_test.txt"

echo ""
echo "[6/6] Storage Performance Testing"
echo "----------------------------------"
python3 test_disk_read_speed.py 2>&1 | tee "$RESULTS_DIR/disk_read_speed.txt"

echo ""
echo "=========================================="
echo "SYSTEM PERFORMANCE ANALYSIS - SUMMARY"
echo "=========================================="
echo "Test execution completed: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Results directory: $RESULTS_DIR"
echo ""
echo "PERFORMANCE METRICS SUMMARY:"
echo "----------------------------"

# Extract key metrics from JSON files
if [ -f "gpu_detection_results.json" ]; then
    GPU_COUNT=$(python3 -c "import json; data=json.load(open('gpu_detection_results.json')); print(data['total_gpus'])" 2>/dev/null || echo "N/A")
    echo "Total GPUs Detected: $GPU_COUNT"
fi

if [ -f "vram_test_results.json" ]; then
    TOTAL_VRAM=$(python3 -c "import json; data=json.load(open('vram_test_results.json')); print(f\"{data['total_vram_gb']:.0f}GB\")" 2>/dev/null || echo "N/A")
    echo "Total GPU Memory: $TOTAL_VRAM"
fi

if [ -f "cuda_version_results.json" ]; then
    CUDA_VERSION=$(python3 -c "import json; data=json.load(open('cuda_version_results.json')); print(data['cuda_version'])" 2>/dev/null || echo "N/A")
    echo "CUDA Runtime Version: $CUDA_VERSION"
fi

if [ -f "bandwidth_test_results.json" ]; then
    echo "Inter-GPU Bandwidth: See detailed results in bandwidth_test.txt"
fi

if [ -f "disk_read_speed_results.json" ]; then
    DISK_SPEED=$(python3 -c "import json; data=json.load(open('disk_read_speed_results.json')); print(f\"{data['read_speed_mbps']:.0f} MB/s\")" 2>/dev/null || echo "N/A")
    echo "Storage Read Performance: $DISK_SPEED"
fi

echo ""
echo "DETAILED RESULTS LOCATION:"
echo "--------------------------"
echo "* GPU Hardware Analysis: $RESULTS_DIR/gpu_detection.txt"
echo "* VRAM Capacity Report: $RESULTS_DIR/vram_capacity.txt"
echo "* CUDA Environment: $RESULTS_DIR/cuda_version.txt"
echo "* GPU Topology Matrix: $RESULTS_DIR/gpu_topology.txt"
echo "* Bandwidth Analysis: $RESULTS_DIR/bandwidth_test.txt"
echo "* Storage Performance: $RESULTS_DIR/disk_read_speed.txt"

echo ""
echo "Analysis completed successfully."
echo "=========================================="
