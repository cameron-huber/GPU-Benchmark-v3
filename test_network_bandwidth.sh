#!/bin/bash

# Network Bandwidth Test - GPU Benchmark v3
# Measures network bandwidth between all nodes in a cluster using iperf3

PORT=5201
TIMEOUT=30
THRESHOLD_GBPS=10

echo "🌐 Network Bandwidth Test"
echo "========================"

# Check if iperf3 is installed
if ! command -v iperf3 &> /dev/null; then
    echo "❌ Error: iperf3 is not installed"
    echo "   Please install with: sudo apt install iperf3"
    exit 1
fi

# Check if hostnames provided
if [ $# -eq 0 ]; then
    echo "❌ Error: No hostnames provided"
    echo "Usage: $0 <host1> <host2> [host3] ..."
    echo "Example: $0 node1 node2 node3"
    exit 1
fi

HOSTS=("$@")
NUM_HOSTS=${#HOSTS[@]}

echo "📊 Testing ${NUM_HOSTS} nodes: ${HOSTS[*]}"

# Function to cleanup iperf3 servers
cleanup() {
    echo "🛑 Cleaning up iperf3 servers..."
    for host in "${HOSTS[@]}"; do
        ssh "$host" "pkill -f 'iperf3 -s'" 2>/dev/null &
    done
    wait
}

# Set trap for cleanup
trap cleanup EXIT

# Start iperf3 servers on all hosts
echo "🔧 Starting iperf3 servers..."
for host in "${HOSTS[@]}"; do
    echo "   Starting server on $host..."
    ssh "$host" "iperf3 -s -p $PORT -D" &
done

# Wait for servers to start
sleep 3

# Create results matrix
declare -A results

echo "📊 Measuring bandwidth between all node pairs..."

# Test connectivity from each host to every other host
for client in "${HOSTS[@]}"; do
    for server in "${HOSTS[@]}"; do
        if [ "$client" != "$server" ]; then
            echo "   Testing $client -> $server"
            
            # Run iperf3 client test
            output=$(ssh "$client" "timeout $TIMEOUT iperf3 -c $server -p $PORT -f g -t 5" 2>/dev/null)
            
            if [ $? -eq 0 ]; then
                # Parse bandwidth from output (look for receiver line)
                bandwidth=$(echo "$output" | grep "receiver" | awk '{print $7}' | head -1)
                
                if [ -n "$bandwidth" ]; then
                    results["$client,$server"]="$bandwidth"
                else
                    results["$client,$server"]="ERR"
                fi
            else
                results["$client,$server"]="ERR"
            fi
        fi
    done
done

# Display results matrix
echo ""
echo "🚀 Network Bandwidth Matrix (Gbps)"
echo "====================================="

# Print header
printf "%-12s" ""
for host in "${HOSTS[@]}"; do
    printf "%-10s" "$host"
done
echo ""

# Print rows
for client in "${HOSTS[@]}"; do
    printf "%-12s" "$client"
    for server in "${HOSTS[@]}"; do
        if [ "$client" = "$server" ]; then
            printf "%-10s" "X"
        else
            bw="${results[$client,$server]}"
            if [ "$bw" = "ERR" ]; then
                printf "%-10s" "ERR"
            else
                # Check if bandwidth is below threshold
                if (( $(echo "$bw < $THRESHOLD_GBPS" | bc -l 2>/dev/null || echo 0) )); then
                    printf "\033[91m%-10s\033[0m" "$bw"  # Red for low bandwidth
                else
                    printf "%-10s" "$bw"
                fi
            fi
        fi
    done
    echo ""
done

echo ""
echo "📋 Legend:"
echo "   X = Self"
echo "   ERR = Connection failed"
echo "   Red values = Below ${THRESHOLD_GBPS} Gbps threshold"
echo ""
echo "✅ Network bandwidth test completed"
