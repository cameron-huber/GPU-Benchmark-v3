#!/usr/bin/env python3
"""
GPU Detection Script for GPU Benchmark v3
Detects and reports GPU models present on the system
"""

import subprocess
import sys
import json
import re
from datetime import datetime


class GPUDetector:
    def __init__(self):
        self.gpu_info = []
        self.system_info = {}
        
    def run_command(self, command):
        """Run a command and return output, or None if failed"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return None
        except Exception as e:
            print(f"Error running command '{command}': {e}")
            return None
    
    def detect_nvidia_gpus(self):
        """Detect NVIDIA GPUs using nvidia-smi"""
        print("🔍 Detecting NVIDIA GPUs...")
        
        # Check if nvidia-smi is available
        nvidia_smi_output = self.run_command("nvidia-smi --query-gpu=index,name,driver_version,memory.total,power.max_limit,temperature.gpu --format=csv,noheader,nounits")
        
        if nvidia_smi_output:
            lines = nvidia_smi_output.split('\n')
            for line in lines:
                if line.strip():
                    parts = [part.strip() for part in line.split(',')]
                    if len(parts) >= 6:
                        gpu_info = {
                            'vendor': 'NVIDIA',
                            'index': parts[0],
                            'name': parts[1],
                            'driver_version': parts[2],
                            'memory_total_mb': parts[3],
                            'power_max_limit_w': parts[4],
                            'temperature_c': parts[5] if parts[5] != '[Not Supported]' else 'N/A'
                        }
                        self.gpu_info.append(gpu_info)
        
        # Get additional NVIDIA GPU details
        nvidia_details = self.run_command("nvidia-smi --query-gpu=gpu_name,compute_cap,gpu_bus_id,gpu_uuid --format=csv,noheader")
        if nvidia_details:
            lines = nvidia_details.split('\n')
            for i, line in enumerate(lines):
                if line.strip() and i < len(self.gpu_info):
                    parts = [part.strip() for part in line.split(',')]
                    if len(parts) >= 4:
                        self.gpu_info[i].update({
                            'compute_capability': parts[1],
                            'bus_id': parts[2],
                            'uuid': parts[3]
                        })
    
    def detect_other_gpus(self):
        """Detect other GPUs using lspci"""
        print("🔍 Detecting other GPUs via lspci...")
        
        lspci_output = self.run_command("lspci | grep -i 'vga\\|3d\\|display'")
        if lspci_output:
            lines = lspci_output.split('\n')
            for line in lines:
                if line.strip():
                    # Parse lspci output
                    parts = line.split(': ')
                    if len(parts) >= 2:
                        pci_id = parts[0]
                        gpu_desc = parts[1]
                        
                        # Skip if already detected by nvidia-smi
                        if any('NVIDIA' in gpu.get('name', '') for gpu in self.gpu_info):
                            if 'NVIDIA' in gpu_desc:
                                continue
                        
                        vendor = 'Unknown'
                        if 'NVIDIA' in gpu_desc:
                            vendor = 'NVIDIA'
                        elif 'AMD' in gpu_desc or 'ATI' in gpu_desc:
                            vendor = 'AMD'
                        elif 'Intel' in gpu_desc:
                            vendor = 'Intel'
                        
                        gpu_info = {
                            'vendor': vendor,
                            'name': gpu_desc,
                            'pci_id': pci_id,
                            'detection_method': 'lspci'
                        }
                        
                        # Only add if not already in the list
                        if not any(gpu.get('name') == gpu_desc for gpu in self.gpu_info):
                            self.gpu_info.append(gpu_info)
    
    def get_system_info(self):
        """Get system information"""
        print("📊 Gathering system information...")
        
        self.system_info = {
            'hostname': self.run_command("hostname"),
            'kernel': self.run_command("uname -r"),
            'os': self.run_command("cat /etc/os-release | grep PRETTY_NAME | cut -d'=' -f2 | tr -d '\"'"),
            'cpu': self.run_command("cat /proc/cpuinfo | grep 'model name' | head -1 | cut -d':' -f2 | xargs"),
            'memory_gb': self.run_command("free -g | grep Mem | awk '{print $2}'"),
            'detection_time': datetime.now().isoformat()
        }
    
    def display_results(self):
        """Display detection results"""
        print("\n" + "="*60)
        print("🖥️  GPU DETECTION RESULTS")
        print("="*60)
        
        # System info
        print(f"🖥️  System: {self.system_info.get('hostname', 'Unknown')}")
        print(f"🐧 OS: {self.system_info.get('os', 'Unknown')}")
        print(f"🧠 CPU: {self.system_info.get('cpu', 'Unknown')}")
        print(f"💾 Memory: {self.system_info.get('memory_gb', 'Unknown')} GB")
        print(f"📅 Detection Time: {self.system_info.get('detection_time', 'Unknown')}")
        
        print("\n" + "-"*60)
        print("🎮 GPU INFORMATION")
        print("-"*60)
        
        if not self.gpu_info:
            print("❌ No GPUs detected")
            return
        
        for i, gpu in enumerate(self.gpu_info, 1):
            print(f"\n📱 GPU #{i}:")
            print(f"   Vendor: {gpu.get('vendor', 'Unknown')}")
            print(f"   Name: {gpu.get('name', 'Unknown')}")
            
            if 'driver_version' in gpu:
                print(f"   Driver: {gpu['driver_version']}")
            if 'memory_total_mb' in gpu:
                print(f"   Memory: {gpu['memory_total_mb']} MB")
            if 'power_max_limit_w' in gpu:
                print(f"   Max Power: {gpu['power_max_limit_w']} W")
            if 'temperature_c' in gpu:
                print(f"   Temperature: {gpu['temperature_c']}°C")
            if 'compute_capability' in gpu:
                print(f"   Compute Capability: {gpu['compute_capability']}")
            if 'bus_id' in gpu:
                print(f"   Bus ID: {gpu['bus_id']}")
            if 'pci_id' in gpu:
                print(f"   PCI ID: {gpu['pci_id']}")
        
        print(f"\n📊 Total GPUs Found: {len(self.gpu_info)}")
    
    def save_results(self, filename='gpu_detection_results.json'):
        """Save results to JSON file"""
        results = {
            'system_info': self.system_info,
            'gpu_info': self.gpu_info,
            'total_gpus': len(self.gpu_info)
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n💾 Results saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {e}")
    
    def run_detection(self):
        """Run full GPU detection"""
        print("🚀 Starting GPU Detection...")
        print("="*60)
        
        self.get_system_info()
        self.detect_nvidia_gpus()
        self.detect_other_gpus()
        self.display_results()
        self.save_results()
        
        return self.gpu_info


def main():
    detector = GPUDetector()
    gpu_info = detector.run_detection()
    
    # Exit with status code based on detection
    if gpu_info:
        print(f"\n✅ Detection completed successfully! Found {len(gpu_info)} GPU(s)")
        sys.exit(0)
    else:
        print("\n⚠️  No GPUs detected")
        sys.exit(1)


if __name__ == "__main__":
    main()
