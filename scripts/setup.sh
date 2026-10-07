#!/bin/bash
# Setup script for Holocron Career AI

set -e

echo "Setting up Holocron Career AI..."

# Create directories
mkdir -p apps/api/src
mkdir -p apps/web
mkdir -p packages/core
mkdir -p packages/agents
mkdir -p packages/rag

# Setup Python environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r apps/api/requirements.txt

# Install development tools
pip install pytest pytest-cov black ruff

echo "Setup complete!"
echo ""
echo "To run:"
echo "  cd apps/api && uvicorn src.main:app --reload"
echo ""
echo "Or use Docker:"
echo "  docker-compose up -d"