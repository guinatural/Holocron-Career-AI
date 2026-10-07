# PowerShell setup script for Holocron Career AI

Write-Host "Setting up Holocron Career AI..." -ForegroundColor Cyan

# Create directories
New-Item -ItemType Directory -Path "apps\api\src" -Force | Out-Null
New-Item -ItemType Directory -Path "apps\web" -Force | Out-Null
New-Item -ItemType Directory -Path "packages\core" -Force | Out-Null
New-Item -ItemType Directory -Path "packages\agents" -Force | Out-Null
New-Item -ItemType Directory -Path "packages\rag" -Force | Out-Null

# Setup Python environment
Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
python -m venv .venv

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
. .venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r apps\api\requirements.txt

# Install development tools
Write-Host "Installing development tools..." -ForegroundColor Yellow
pip install pytest pytest-cov black ruff

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To run:"
Write-Host "  cd apps\api"
Write-Host "  uvicorn src.main:app --reload"
Write-Host ""
Write-Host "Or use Docker:"
Write-Host "  docker-compose up -d"