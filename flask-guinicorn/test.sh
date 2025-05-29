#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to test an endpoint
test_endpoint() {
    local port=$1
    local endpoint=$2
    local method=${3:-GET}
    local data=$4
    
    echo -e "\n${GREEN}Testing ${endpoint} on port ${port}${NC}"
    echo "----------------------------------------"
    
    if [ "$method" = "POST" ]; then
        response=$(curl -s -X POST -H "Content-Type: application/json" -d "$data" "http://localhost:${port}${endpoint}")
    else
        response=$(curl -s "http://localhost:${port}${endpoint}")
    fi
    
    if [ $? -eq 0 ]; then
        echo -e "${BLUE}Response:${NC}"
        echo "$response" | python3 -m json.tool
    else
        echo -e "${RED}Error: Failed to connect to ${endpoint}${NC}"
    fi
}

# Function to test both versions
test_both_versions() {
    local endpoint=$1
    local method=${2:-GET}
    local data=$3
    
    echo -e "\n${BLUE}Testing ${endpoint} on both versions${NC}"
    echo "========================================"
    
    # Test Gunicorn version
    test_endpoint "5000" "$endpoint" "$method" "$data"
    
    # Test Uvicorn version
    test_endpoint "5001" "$endpoint" "$method" "$data"
}

# Test regular endpoints
test_both_versions "/api/hello"
test_both_versions "/api/params?name=John&age=30"
test_both_versions "/api/echo" "POST" '{"message":"test"}'

# Test async endpoints
test_both_versions "/api/async/hello"
test_both_versions "/api/async/delayed?delay=2"
test_both_versions "/api/async/parallel"

echo -e "\n${GREEN}All tests completed!${NC}" 