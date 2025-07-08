#!/bin/bash

# GPU Topology Display - GPU Benchmark v3
# Shows GPU interconnection topology using nvidia-smi

echo "🔗 GPU Topology Analysis"
echo "=========================="

# Check if nvidia-smi is available
if ! command -v nvidia-smi &> /dev/null; then
    echo "❌ Error: nvidia-smi not found"
    exit 1
fi

echo "📊 GPU Topology Matrix:"
echo "-----------------------"

# Run nvidia-smi topology
nvidia-smi topo -m

echo ""
echo "✅ Topology display completed"
