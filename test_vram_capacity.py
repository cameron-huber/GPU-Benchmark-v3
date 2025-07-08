#!/usr/bin/env python3
"""
VRAM Capacity Test - GPU Benchmark v3
Professional VRAM capacity analysis and reporting
"""

import subprocess
import json
from datetime import datetime

def run_command(cmd):
    """Run command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else None
    except:
        return None

def test_vram_capacity():
    """Test VRAM capacity for all GPUs"""
    print("VRAM Capacity Analysis")
    print("=" * 50)
    
    # Get VRAM info
    vram_data = run_command("nvidia-smi --query-gpu=index,name,memory.total,memory.used,memory.free --format=csv,noheader,nounits")
    
    if not vram_data:
        print("ERROR: Could not retrieve VRAM information")
        return
    
    gpus = []
    total_vram = 0
    
    for line in vram_data.split('\n'):
        if line.strip():
            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 5:
                gpu_id, name, total, used, free = parts
                total_mb = int(total)
                used_mb = int(used)
                free_mb = int(free)
                
                gpu_info = {
                    'id': gpu_id,
                    'name': name,
                    'total_mb': total_mb,
                    'used_mb': used_mb,
                    'free_mb': free_mb,
                    'total_gb': round(total_mb / 1024, 2),
                    'used_gb': round(used_mb / 1024, 2),
                    'free_gb': round(free_mb / 1024, 2),
                    'usage_percent': round((used_mb / total_mb) * 100, 1)
                }
                
                gpus.append(gpu_info)
                total_vram += total_mb
                
                print(f"GPU {gpu_id}: {name}")
                print(f"   Total VRAM: {gpu_info['total_gb']} GB ({total_mb} MB)")
                print(f"   Used VRAM:  {gpu_info['used_gb']} GB ({used_mb} MB)")
                print(f"   Free VRAM:  {gpu_info['free_gb']} GB ({free_mb} MB)")
                print(f"   Usage: {gpu_info['usage_percent']}%")
                print()
    
    # Summary
    print("VRAM ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Total GPUs: {len(gpus)}")
    print(f"Total VRAM: {round(total_vram / 1024, 2)} GB ({total_vram} MB)")
    print(f"Average VRAM per GPU: {round(total_vram / len(gpus) / 1024, 2)} GB")
    
    # Save results
    results = {
        'timestamp': datetime.now().isoformat(),
        'total_gpus': len(gpus),
        'total_vram_mb': total_vram,
        'total_vram_gb': round(total_vram / 1024, 2),
        'gpus': gpus
    }
    
    with open('vram_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: vram_test_results.json")
    print("VRAM capacity analysis completed")

if __name__ == "__main__":
    test_vram_capacity()
