#!/usr/bin/env python3
"""
PCIe/NVLink Bandwidth Test - GPU Benchmark v3
Uses NVIDIA NCCL tests to measure actual bandwidth between GPUs
"""

import subprocess
import json
import re
import os
from datetime import datetime

def run_command(cmd, cwd=None):
    """Run command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return None, str(e), -1

def test_bandwidth():
    """Test bandwidth using NCCL tests"""
    print("🚀 PCIe/NVLink Bandwidth Test")
    print("=" * 50)
    
    # Check if NCCL tests are available
    nccl_path = "nccl-tests/build"
    if not os.path.exists(nccl_path):
        print("❌ NCCL tests not found. Please run ./setup.sh first")
        return
    
    # Get GPU count
    gpu_count_cmd = "nvidia-smi --query-gpu=count --format=csv,noheader,nounits"
    stdout, stderr, returncode = run_command(gpu_count_cmd)
    
    if returncode != 0:
        print("❌ Failed to get GPU count")
        return
    
    try:
        gpu_count = int(stdout.strip().split('\n')[0])
        print(f"📱 Detected {gpu_count} GPUs")
    except:
        print("❌ Failed to parse GPU count")
        return
    
    # Run bandwidth tests
    tests = [
        ("All-Reduce", "all_reduce_perf"),
        ("All-Gather", "all_gather_perf"),  
        ("Broadcast", "broadcast_perf"),
        ("Reduce-Scatter", "reduce_scatter_perf")
    ]
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'gpu_count': gpu_count,
        'tests': {}
    }
    
    for test_name, test_binary in tests:
        print(f"\n🔍 Running {test_name} test...")
        
        # Run test with multiple GPUs (smaller range for faster execution)
        cmd = f"./{test_binary} -b 1K -e 1M -f 2 -g {gpu_count}"
        stdout, stderr, returncode = run_command(cmd, cwd=nccl_path)
        
        if returncode != 0:
            print(f"❌ {test_name} test failed: {stderr}")
            continue
        
        # Parse results
        bandwidth_data, avg_bandwidth = parse_nccl_output(stdout)
        results['tests'][test_name] = {
            'bandwidth_data': bandwidth_data,
            'avg_bus_bandwidth': avg_bandwidth
        }
        
        if bandwidth_data:
            max_bw = max(bandwidth_data, key=lambda x: x['algbw'])
            print(f"✅ {test_name}")
            print(f"   Max Algorithm BW: {max_bw['algbw']:.2f} GB/s")
            print(f"   Max Bus BW: {max_bw['busbw']:.2f} GB/s")
            if avg_bandwidth:
                print(f"   Average Bus BW: {avg_bandwidth:.2f} GB/s")
        else:
            print(f"⚠️  {test_name} - Could not parse bandwidth data")
    
    # Save results
    with open('bandwidth_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: bandwidth_test_results.json")
    print("✅ Bandwidth test completed")

def parse_nccl_output(output):
    """Parse NCCL test output to extract bandwidth data"""
    lines = output.split('\n')
    bandwidth_data = []
    avg_bandwidth = None
    
    for line in lines:
        # Parse data lines (not headers or comments)
        if not line.startswith('#') and 'float' in line and 'sum' in line:
            parts = line.split()
            if len(parts) >= 8:
                try:
                    size_bytes = int(parts[0])
                    time_us = float(parts[5])
                    algbw = float(parts[6])
                    busbw = float(parts[7])
                    
                    bandwidth_data.append({
                        'size_bytes': size_bytes,
                        'time_us': time_us,
                        'algbw': algbw,
                        'busbw': busbw
                    })
                except:
                    continue
        
        # Parse average bandwidth line
        elif line.startswith('# Avg bus bandwidth'):
            try:
                avg_bandwidth = float(line.split(':')[1].strip())
            except:
                pass
    
    return bandwidth_data, avg_bandwidth

if __name__ == "__main__":
    test_bandwidth()
