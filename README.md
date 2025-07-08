# GPU Benchmark v3

A comprehensive GPU benchmarking tool for performance testing and analysis.

## Quick Start

### 1. Setup
```bash
./setup.sh
```

### 2. Run Tests
```bash
# Detect GPU hardware
./detect_gpus.sh

# Test VRAM capacity
python3 test_vram_capacity.py

# Check CUDA version
./test_cuda_version.sh

# Test PCIe/NVLink bandwidth
python3 test_bandwidth.py
```

## Features

- **GPU Detection**: Comprehensive GPU hardware detection and profiling
- **VRAM Testing**: Memory capacity and usage monitoring
- **CUDA Version**: Runtime and development environment verification
- **Bandwidth Testing**: PCIe/NVLink bandwidth measurement using NVIDIA NCCL
- **JSON Output**: Structured data for programmatic integration

## Tools

### Hardware Detection
- `detect_gpus.py` - Comprehensive GPU detection with detailed specs
- `detect_gpus.sh` - Simple bash wrapper for GPU detection

### VRAM Testing
- `test_vram.sh` - Quick VRAM capacity test
- `test_vram_capacity.py` - Detailed VRAM analysis with JSON output

### CUDA Testing
- `test_cuda_version.sh` - Simple CUDA version check
- `test_cuda_version.py` - Python CUDA version test with JSON output

### Bandwidth Testing
- `test_bandwidth.py` - PCIe/NVLink bandwidth testing using NVIDIA NCCL

### Setup and Installation
- `setup.sh` - Automated setup script for all dependencies

## Requirements

- NVIDIA GPUs with CUDA support
- Ubuntu 20.04+ (or compatible Linux distribution)
- NVIDIA drivers installed
- Python 3.6+
- Build tools (gcc, make, etc.)

## Installation

The setup script will automatically install:
- NVIDIA CUDA development tools
- NCCL library and development headers
- Python dependencies
- NCCL test suite (compiled from source)

## Output Files

All tests generate JSON output files for easy integration:
- `gpu_detection_results.json` - GPU hardware information
- `vram_test_results.json` - VRAM capacity and usage data
- `cuda_version_results.json` - CUDA runtime information
- `bandwidth_test_results.json` - PCIe/NVLink bandwidth measurements

## Example Usage

```bash
# Full system analysis
./detect_gpus.sh
python3 test_vram_capacity.py
python3 test_cuda_version.py
python3 test_bandwidth.py

# View results
ls -la *_results.json
```

## Contributing

Contributions welcome! Please read our contributing guidelines.

## License

MIT License
