#!/bin/bash

# Disk Read Speed Test - GPU Benchmark v3
# Measures disk read throughput using dd command

echo "💾 Disk Read Speed Test"
echo "======================="

# Check available disk space
TEMP_FILE="temp_test_file_1gb.dat"
REQUIRED_SPACE_MB=1100  # 1GB + some buffer

echo "🔍 Checking disk space..."
AVAILABLE_SPACE=$(df . | tail -1 | awk '{print $4}')
AVAILABLE_SPACE_MB=$((AVAILABLE_SPACE / 1024))

if [ $AVAILABLE_SPACE_MB -lt $REQUIRED_SPACE_MB ]; then
    echo "❌ Error: Insufficient disk space"
    echo "   Required: ${REQUIRED_SPACE_MB}MB"
    echo "   Available: ${AVAILABLE_SPACE_MB}MB"
    exit 1
fi

echo "✅ Disk space check passed (${AVAILABLE_SPACE_MB}MB available)"

# Cleanup function
cleanup() {
    if [ -f "$TEMP_FILE" ]; then
        echo "🧹 Cleaning up temporary file..."
        rm -f "$TEMP_FILE"
    fi
}

# Set trap for cleanup on exit
trap cleanup EXIT

# Create 1GB test file with random data
echo "📝 Creating 1GB test file with random data..."
echo "   This may take a moment..."

if ! dd if=/dev/urandom of="$TEMP_FILE" bs=1M count=1024 2>/dev/null; then
    echo "❌ Error: Failed to create test file"
    exit 1
fi

echo "✅ Test file created successfully"

# Sync to ensure data is written to disk
sync

# Clear filesystem cache (best effort, no root required)
echo "🔄 Clearing filesystem cache..."
echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || echo "   Cache clear skipped (no root privileges)"

# Perform read test
echo "📊 Performing read speed test..."
echo "   Reading 1GB file..."

# Use dd to read the file and capture timing
READ_OUTPUT=$(dd if="$TEMP_FILE" of=/dev/null bs=1M 2>&1)

if [ $? -ne 0 ]; then
    echo "❌ Error: Read test failed"
    exit 1
fi

# Parse dd output to extract timing and calculate speed
# dd output format: "1073741824 bytes (1.1 GB, 1.0 GiB) copied, 2.34567 s, 458 MB/s"

# Extract the speed directly from dd output
SPEED_MBPS=$(echo "$READ_OUTPUT" | grep -o '[0-9.]\+ MB/s' | grep -o '[0-9.]\+')

if [ -z "$SPEED_MBPS" ]; then
    # Fallback: calculate manually from timing
    BYTES_READ=$(echo "$READ_OUTPUT" | grep -o '[0-9]\+ bytes' | head -1 | grep -o '[0-9]\+')
    TIME_TAKEN=$(echo "$READ_OUTPUT" | grep -o '[0-9.]\+ s' | grep -o '[0-9.]\+')
    
    if [ -n "$BYTES_READ" ] && [ -n "$TIME_TAKEN" ]; then
        SPEED_MBPS=$(echo "scale=2; $BYTES_READ / $TIME_TAKEN / 1024 / 1024" | bc 2>/dev/null)
    fi
fi

# Display results
echo ""
echo "📈 Read Speed Test Results:"
echo "=========================="
echo "File size: 1GB (1,073,741,824 bytes)"

if [ -n "$SPEED_MBPS" ]; then
    echo "Read speed: ${SPEED_MBPS} MB/s"
    
    # Performance classification
    if (( $(echo "$SPEED_MBPS > 500" | bc -l 2>/dev/null || echo 0) )); then
        echo "Performance: 🚀 Excellent (NVMe SSD)"
    elif (( $(echo "$SPEED_MBPS > 200" | bc -l 2>/dev/null || echo 0) )); then
        echo "Performance: ✅ Good (SATA SSD)"
    elif (( $(echo "$SPEED_MBPS > 100" | bc -l 2>/dev/null || echo 0) )); then
        echo "Performance: ⚠️  Fair (Fast HDD)"
    else
        echo "Performance: 🐌 Slow (Traditional HDD)"
    fi
else
    echo "❌ Could not determine read speed"
    echo "Raw dd output:"
    echo "$READ_OUTPUT"
fi

# Additional system info
echo ""
echo "💾 Storage Information:"
echo "======================"
echo "Mount point: $(df . | tail -1 | awk '{print $6}')"
echo "Filesystem: $(df -T . | tail -1 | awk '{print $2}')"
echo "Total space: $(df -h . | tail -1 | awk '{print $2}')"
echo "Available space: $(df -h . | tail -1 | awk '{print $4}')"

echo ""
echo "✅ Disk read speed test completed"
