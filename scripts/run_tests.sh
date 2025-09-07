#!/bin/bash

# Test runner script for EzyagoTrading
set -e

echo "🧪 Running EzyagoTrading Tests..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    echo -e "${RED}❌ Error: Please run this script from the project root directory${NC}"
    exit 1
fi

# Install test dependencies if not already installed
echo -e "${BLUE}📦 Installing test dependencies...${NC}"
pip install pytest pytest-asyncio pytest-cov pytest-mock --quiet

# Create test reports directory
mkdir -p reports

# Run tests with coverage
echo -e "${BLUE}🔍 Running tests with coverage...${NC}"
pytest tests/ \
    --cov=app \
    --cov-report=html:reports/coverage \
    --cov-report=term-missing \
    --cov-report=xml:reports/coverage.xml \
    --junit-xml=reports/test-results.xml \
    --cov-fail-under=70 \
    -v \
    --tb=short

# Check if tests passed
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed successfully!${NC}"
    echo -e "${BLUE}📊 Coverage report generated in reports/coverage/index.html${NC}"
    echo -e "${BLUE}📋 Test results saved in reports/test-results.xml${NC}"
else
    echo -e "${RED}❌ Some tests failed. Check the output above.${NC}"
    exit 1
fi

# Optional: Open coverage report (uncomment if needed)
# if command -v xdg-open > /dev/null; then
#     xdg-open reports/coverage/index.html
# elif command -v open > /dev/null; then
#     open reports/coverage/index.html
# fi

echo -e "${GREEN}🎉 Test run completed!${NC}"