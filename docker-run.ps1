# PowerShell Script for Running Ars0n Framework Docker Containers on Windows

# Colors for better output
$Green = [ConsoleColor]::Green
$Yellow = [ConsoleColor]::Yellow
$Red = [ConsoleColor]::Red

Write-Host "Starting Ars0n Framework Containers..." -ForegroundColor $Green

# Check if Docker is installed
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker is not installed. Please install Docker Desktop for Windows first." -ForegroundColor $Red
    exit 1
}

# Check if Docker is running
try {
    docker info *> $null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker is not running"
    }
} catch {
    Write-Host "Docker is not running. Please start Docker Desktop and try again." -ForegroundColor $Red
    exit 1
}

# Create .keys directory if it doesn't exist
$keysPath = "$env:USERPROFILE\.keys"
if (-not (Test-Path $keysPath)) {
    New-Item -Path $keysPath -ItemType Directory | Out-Null
}
Write-Host "Checking for API keys directory at $keysPath" -ForegroundColor $Yellow
Write-Host "You can add your API keys to this directory later if needed." -ForegroundColor $Yellow

# Check if containers already exist and are running
$containersRunning = docker ps | Select-String "ars0n-"
if ($containersRunning) {
    Write-Host "Ars0n Framework containers are already running." -ForegroundColor $Yellow
    $answer = Read-Host "Do you want to restart them? (y/n)"
    if ($answer -eq "y" -or $answer -eq "Y") {
        Write-Host "Stopping existing containers..." -ForegroundColor $Yellow
        docker-compose down
    } else {
        Write-Host "Exiting without changes." -ForegroundColor $Green
        exit 0
    }
}

# Build and start the containers
Write-Host "Building and starting containers..." -ForegroundColor $Green
docker-compose up -d --build

# Check if all containers started successfully
if ($LASTEXITCODE -eq 0) {
    Write-Host "=======================================" -ForegroundColor $Green
    Write-Host "Ars0n Framework started successfully!" -ForegroundColor $Green
    Write-Host "=======================================" -ForegroundColor $Green
    Write-Host "Access the application at:" -ForegroundColor $Yellow
    Write-Host "http://localhost:3000" -ForegroundColor $Green
    Write-Host "To stop the application, run:" -ForegroundColor $Yellow
    Write-Host "docker-compose down" -ForegroundColor $Green
} else {
    Write-Host "Failed to start Ars0n Framework containers." -ForegroundColor $Red
    Write-Host "Please check the logs for more information:" -ForegroundColor $Red
    Write-Host "docker-compose logs" -ForegroundColor $Green
} 