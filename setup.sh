#!/bin/bash

# GPU Benchmark v3 Setup Script
# Installs all dependencies and builds tools

echo "🚀 GPU Benchmark v3 Setup"
echo "========================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root"
   exit 1
fi

# Update system
echo "📦 Updating system packages..."
sudo apt update

# Install essential dependencies
echo "🔧 Installing dependencies..."
sudo apt install -y \
    build-essential \
    git \
    python3 \
    python3-pip \
    libnccl2 \
    libnccl-dev \
    cuda-toolkit-12-9 \
    nvidia-cuda-toolkit

# Verify NVIDIA drivers
echo "🔍 Verifying NVIDIA drivers..."
if ! command -v nvidia-smi &> /dev/null; then
    echo "❌ NVIDIA drivers not found. Please install NVIDIA drivers first."
    exit 1
fi

# Clone and build NCCL tests if not already present
if [ ! -d "nccl-tests" ]; then
    echo "📥 Cloning NCCL tests..."
    git clone https://github.com/NVIDIA/nccl-tests.git
fi

echo "🔨 Building NCCL tests..."
cd nccl-tests
make clean
make MPI=0 -j4
cd ..

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip3 install --user numpy

# Make all scripts executable
echo "✅ Making scripts executable..."
chmod +x *.sh *.py

echo ""
echo "🎉 Setup completed successfully!"
echo "================================="
echo "Available tools:"
echo "  ./detect_gpus.sh           - Detect GPU hardware"
echo "  ./test_vram_capacity.py    - Test VRAM capacity"
echo "  ./test_cuda_version.sh     - Check CUDA version"
echo "  ./test_bandwidth.py        - Test PCIe/NVLink bandwidth"
echo ""
echo "To run bandwidth tests:"
echo "  python3 test_bandwidth.py"
