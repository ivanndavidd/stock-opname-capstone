# Stock Monitoring System - Quick Setup Script
# Run this to setup and launch the Streamlit app

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Stock Opname Monitoring System - Setup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.10+ from python.org" -ForegroundColor Red
    exit 1
}
Write-Host "OK: Python found" -ForegroundColor Green
Write-Host ""

# Check if in correct directory
if (-not (Test-Path "streamlit_app.py")) {
    Write-Host "ERROR: streamlit_app.py not found!" -ForegroundColor Red
    Write-Host "Please run this script from D:\files\" -ForegroundColor Red
    exit 1
}

# Create directories
Write-Host "Creating directories..." -ForegroundColor Yellow
$dirs = @("models", "timeseries_data", "uploads", "results")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "  Exists: $dir" -ForegroundColor Gray
    }
}
Write-Host ""

# Check models
Write-Host "Checking models..." -ForegroundColor Yellow
$yolo_exists = Test-Path "models\best.pt"
$lstm_exists = Test-Path "models\lstm_stock_forecasting.h5"

if ($yolo_exists) {
    Write-Host "  OK: YOLOv8 model found" -ForegroundColor Green
} else {
    Write-Host "  WARNING: YOLOv8 model not found" -ForegroundColor Red
    Write-Host "    Please place best.pt in models\" -ForegroundColor Yellow
}

if ($lstm_exists) {
    Write-Host "  OK: LSTM model found" -ForegroundColor Green
} else {
    Write-Host "  WARNING: LSTM model not found" -ForegroundColor Red
    Write-Host "    Please place lstm_stock_forecasting.h5 in models\" -ForegroundColor Yellow
}
Write-Host ""

# Install dependencies
Write-Host "Checking dependencies..." -ForegroundColor Yellow
$install_deps = Read-Host "Install/Update dependencies? (y/n)"
if ($install_deps -eq "y") {
    Write-Host "Installing packages..." -ForegroundColor Yellow
    pip install streamlit ultralytics tensorflow pandas plotly opencv-python scikit-learn --upgrade
    Write-Host "Dependencies installed!" -ForegroundColor Green
} else {
    Write-Host "Skipping dependency installation" -ForegroundColor Gray
}
Write-Host ""

# Summary
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Setup Summary" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Directories:" -ForegroundColor White
Write-Host "  models\        $(if ($yolo_exists -and $lstm_exists) {'OK'} else {'INCOMPLETE'})" -ForegroundColor $(if ($yolo_exists -and $lstm_exists) {'Green'} else {'Yellow'})
Write-Host "  timeseries_data\" -ForegroundColor White
Write-Host "  uploads\" -ForegroundColor White
Write-Host "  results\" -ForegroundColor White
Write-Host ""

Write-Host "Models:" -ForegroundColor White
Write-Host "  YOLOv8:  $(if ($yolo_exists) {'Found'} else {'Missing'})" -ForegroundColor $(if ($yolo_exists) {'Green'} else {'Red'})
Write-Host "  LSTM:    $(if ($lstm_exists) {'Found'} else {'Missing'})" -ForegroundColor $(if ($lstm_exists) {'Green'} else {'Red'})
Write-Host ""

# Launch option
Write-Host "================================================" -ForegroundColor Cyan
$launch = Read-Host "Launch Streamlit app now? (y/n)"
if ($launch -eq "y") {
    Write-Host ""
    Write-Host "Starting Streamlit..." -ForegroundColor Green
    Write-Host "URL: http://localhost:8501" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
    Write-Host ""
    streamlit run streamlit_app.py
} else {
    Write-Host ""
    Write-Host "To launch manually, run:" -ForegroundColor Green
    Write-Host "  streamlit run streamlit_app.py" -ForegroundColor Cyan
    Write-Host ""
}
