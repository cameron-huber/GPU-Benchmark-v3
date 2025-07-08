#!/usr/bin/env python3
"""
Network Bandwidth Test - GPU Benchmark v3
Measures network bandwidth between all nodes in a cluster using iperf3
"""

import subprocess
import shlex
import json
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
PORT = 5201
TIMEOUT = 5
THRESHOLD_GBPS = 10.0  # Threshold for highlighting low-performance links


def run_command(cmd):
    """Run shell command with timeout"""
    try:
        process = subprocess.run(shlex.split(cmd), capture_output=True, text=True, timeout=TIMEOUT)
        return process.stdout, process.stderr, process.returncode
    except subprocess.TimeoutExpired:
        return None, "Timed out", -1


def start_iperf_server(host):
    """Start iperf3 server on a given host"""
    cmd = f"ssh {host} iperf3 -s -p {PORT}"
    return run_command(cmd)


def stop_iperf_server(host):
    """Stop iperf3 server on a given host"""
    # Best effort, ignore failure
    cmd = f"ssh {host} pkill -f 'iperf3 -s -p {PORT}'"
    run_command(cmd)


def run_iperf_client(client, server):
    """Run iperf3 client to measure bandwidth to server"""
    cmd = f"ssh {client} iperf3 -c {server} -p {PORT}"
    stdout, stderr, returncode = run_command(cmd)
    if returncode != 0:
        return None, stderr

    # Parse output
    for line in stdout.splitlines():
        if "receiver" in line or "sender" in line:
            parts = line.split()
            try:
                # Extract bits/sec and convert to Gbps
                bps = float(parts[-2])
                gbps = bps / 1e9
                return gbps, None
            except (ValueError, IndexError):
                continue

    return None, "Failed to parse iperf3 output"


def test_network_bandwidth(hosts):
    """Test network bandwidth across all nodes"""
    print("🌐 Network Bandwidth Test")
    print("========================")

    # Start iperf3 servers
    with ThreadPoolExecutor() as executor:
        print("🔧 Starting iperf3 servers...")
        servers_future = {executor.submit(start_iperf_server, host): host for host in hosts}
        for future in as_completed(servers_future):
            host = servers_future[future]
            stdout, stderr, _ = future.result()
            if stderr.strip():
                print(f"❌ Error starting server on {host}: {stderr.strip()}")
        print("✅ Servers started")

    # Measure bandwidth
    results = {host: {} for host in hosts}

    with ThreadPoolExecutor() as executor:
        print("📊 Measuring bandwidth...")
        client_server_pairs = [(client, server) for client in hosts for server in hosts if client != server]
        futures = {executor.submit(run_iperf_client, client, server): (client, server) for client, server in client_server_pairs}
        for future in as_completed(futures):
            client, server = futures[future]
            gbps, error = future.result()
            results[client][server] = gbps if gbps is not None else error

    # Stop iperf3 servers
    with ThreadPoolExecutor() as executor:
        print("🛑 Stopping iperf3 servers...")
        for host in hosts:
            executor.submit(stop_iperf_server, host)

    # Print results matrix
    print("\n🚀 Network Bandwidth Matrix (Gbps)")
    print("------------------------------------")
    print("       " + "  ".join([f"{h:7}" for h in hosts]))
    for client in hosts:
        row = f"{client:7} "
        for server in hosts:
            if client == server:
                row += "  X    "
            else:
                bw = results[client][server]
                if isinstance(bw, float):
                    if bw < THRESHOLD_GBPS:
                        row += f"\033[91m{bw:.1f}\033[0m  "  # Red text for low bandwidth
                    else:
                        row += f"{bw:.1f}  "
                else:
                    row += " ERR  "
        print(row)

    # Save results
    results_json = {client: {server: results[client][server] for server in hosts if client != server}
                    for client in hosts}

    with open('network_bandwidth_results.json', 'w') as f:
        json.dump(results_json, f, indent=2)

    print("\n💾 Results saved to: network_bandwidth_results.json")
    print("✅ Network bandwidth test completed")


def main():
    parser = argparse.ArgumentParser(description="Network Bandwidth Test Using iperf3")
    parser.add_argument('hosts', metavar='H', type=str, nargs='+', help='List of hostnames or IP addresses')
    args = parser.parse_args()
    test_network_bandwidth(args.hosts)


if __name__ == "__main__":
    main()
