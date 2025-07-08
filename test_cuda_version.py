#!/usr/bin/env python3
"""
CUDA Version Test - GPU Benchmark v3
Tests and reports CUDA version information
"""

import subprocess
import json
import re
from datetime import datetime

def run_command(cmd):
    """Run command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else None
    except:
        return None

def test_cuda_version():
    """Test CUDA version and related information"""
    print("🔥 CUDA Version Test")
    print("=" * 30)
    
    # Get nvidia-smi output
    nvidia_smi_output = run_command("nvidia-smi")
    if not nvidia_smi_output:
        print("❌ Error: nvidia-smi not available")
        return
    
    # Extract CUDA version
    cuda_match = re.search(r'CUDA Version: (\d+\.\d+)', nvidia_smi_output)
    cuda_version = cuda_match.group(1) if cuda_match else "Unknown"
    
    # Extract driver version
    driver_match = re.search(r'Driver Version: ([\d.]+)', nvidia_smi_output)
    driver_version = driver_match.group(1) if driver_match else "Unknown"
    
    # Check for NVCC
    nvcc_output = run_command("nvcc --version")
    nvcc_version = "Not installed"
    if nvcc_output:
        nvcc_match = re.search(r'release (\d+\.\d+)', nvcc_output)
        nvcc_version = nvcc_match.group(1) if nvcc_match else "Unknown"
    
    # Display results
    print(f"✅ CUDA Version: {cuda_version}")
    print(f"🔧 Driver Version: {driver_version}")
    print(f"🛠️  NVCC Version: {nvcc_version}")
    
    # Save results
    results = {
        'timestamp': datetime.now().isoformat(),
        'cuda_version': cuda_version,
        'driver_version': driver_version,
        'nvcc_version': nvcc_version,
        'nvcc_available': nvcc_version != "Not installed"
    }
    
    with open('cuda_version_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: cuda_version_results.json")
    print("✅ CUDA version test completed")

if __name__ == "__main__":
    test_cuda_version()
