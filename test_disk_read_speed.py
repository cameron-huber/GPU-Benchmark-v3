#!/usr/bin/env python3
"""
Disk Read Speed Test - GPU Benchmark v3
Measures disk read throughput using dd command
"""

import os
import subprocess
import time
import json
import shutil
from datetime import datetime

def run_command(cmd, shell=True):
    """Run command and return output"""
    try:
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return None, str(e), -1

def get_disk_info(path="."):
    """Get disk information"""
    try:
        usage = shutil.disk_usage(path)
        return {
            'total_bytes': usage.total,
            'used_bytes': usage.used,
            'free_bytes': usage.free,
            'total_gb': round(usage.total / (1024**3), 2),
            'used_gb': round(usage.used / (1024**3), 2),
            'free_gb': round(usage.free / (1024**3), 2)
        }
    except:
        return None

def test_disk_read_speed():
    """Test disk read speed"""
    print("STORAGE: Disk Read Speed Test")
    print("=======================")
    
    temp_file = "temp_test_file_1gb.dat"
    test_size_mb = 1024
    test_size_bytes = test_size_mb * 1024 * 1024
    
    # Check disk space
    print("STATUS: Checking disk space...")
    disk_info = get_disk_info()
    if not disk_info:
        print("ERROR: Error: Could not get disk information")
        return
    
    required_bytes = test_size_bytes + (100 * 1024 * 1024)  # 100MB buffer
    if disk_info['free_bytes'] < required_bytes:
        print(f"ERROR: Error: Insufficient disk space")
        print(f"   Required: {required_bytes / (1024**3):.2f}GB")
        print(f"   Available: {disk_info['free_gb']:.2f}GB")
        return
    
    print(f"SUCCESS: Disk space check passed ({disk_info['free_gb']:.2f}GB available)")
    
    # Cleanup function
    def cleanup():
        if os.path.exists(temp_file):
            print("CLEANUP: Cleaning up temporary file...")
            os.remove(temp_file)
    
    try:
        # Create test file
        print("CREATING: Creating 1GB test file with random data...")
        print("   This may take a moment...")
        
        start_time = time.time()
        stdout, stderr, returncode = run_command(f"dd if=/dev/urandom of={temp_file} bs=1M count={test_size_mb}")
        
        if returncode != 0:
            print(f"ERROR: Error: Failed to create test file: {stderr}")
            return
        
        create_time = time.time() - start_time
        print(f"SUCCESS: Test file created successfully ({create_time:.2f}s)")
        
        # Sync to ensure data is written to disk
        os.sync()
        
        # Clear filesystem cache (best effort)
        print("PROCESSING: Clearing filesystem cache...")
        try:
            with open('/proc/sys/vm/drop_caches', 'w') as f:
                f.write('3')
        except:
            print("   Cache clear skipped (no root privileges)")
        
        # Perform read test
        print("TESTING: Performing read speed test...")
        print("   Reading 1GB file...")
        
        start_time = time.time()
        stdout, stderr, returncode = run_command(f"dd if={temp_file} of=/dev/null bs=1M")
        read_time = time.time() - start_time
        
        if returncode != 0:
            print(f"ERROR: Error: Read test failed: {stderr}")
            return
        
        # Calculate speed
        speed_mbps = test_size_bytes / read_time / (1024 * 1024)
        
        # Display results
        print("")
        print("RESULTS: Read Speed Test Results:")
        print("==========================")
        print(f"File size: {test_size_mb}MB ({test_size_bytes:,} bytes)")
        print(f"Read time: {read_time:.2f}s")
        print(f"Read speed: {speed_mbps:.2f} MB/s")
        
        # Performance classification
        if speed_mbps > 500:
            performance = "EXCELLENT: Excellent (NVMe SSD)"
        elif speed_mbps > 200:
            performance = "SUCCESS: Good (SATA SSD)"
        elif speed_mbps > 100:
            performance = "WARNING:  Fair (Fast HDD)"
        else:
            performance = "SLOW: Slow (Traditional HDD)"
        
        print(f"Performance: {performance}")
        
        # Additional system info
        print("")
        print("STORAGE: Storage Information:")
        print("======================")
        print(f"Total space: {disk_info['total_gb']:.2f}GB")
        print(f"Used space: {disk_info['used_gb']:.2f}GB")
        print(f"Available space: {disk_info['free_gb']:.2f}GB")
        
        # Get filesystem info
        stdout, stderr, returncode = run_command("df -T .")
        if returncode == 0:
            lines = stdout.strip().split('\n')
            if len(lines) >= 2:
                fs_info = lines[1].split()
                if len(fs_info) >= 2:
                    print(f"Filesystem: {fs_info[1]}")
        
        # Save results
        results = {
            'timestamp': datetime.now().isoformat(),
            'test_size_mb': test_size_mb,
            'test_size_bytes': test_size_bytes,
            'read_time_seconds': round(read_time, 2),
            'read_speed_mbps': round(speed_mbps, 2),
            'performance_category': performance,
            'disk_info': disk_info
        }
        
        with open('disk_read_speed_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nSTORAGE: Results saved to: disk_read_speed_results.json")
        print("SUCCESS: Disk read speed test completed")
        
    finally:
        cleanup()

if __name__ == "__main__":
    test_disk_read_speed()
