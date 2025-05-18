# SUBTASK-T001.md - Docker Compose Setup

## Parent Task
**T001**: Create Docker Compose setup for the entire stack

## Specific Goal
Create a complete containerized environment for the Ars0n Framework that can run on both Linux and Windows platforms.

## Dependencies
None

## Implementation Approach

The containerization approach follows these key principles:
1. Each component (client, server, toolkit, database) in its own container
2. Data persistence through Docker volumes
3. Inter-container communication through Docker network
4. Easy startup through helper scripts

## Progress Status: 90%

## Validation Criteria
- All containers start successfully with a single command
- Client can communicate with server
- Server can communicate with database
- Server can communicate with toolkit service
- Toolkit service can perform scans
- Data persists between container restarts
- Scripts work on both Linux/Mac and Windows environments

## Files to Modify

### Primary Files
- `docker-compose.yml` - Main orchestration file
- `client/Dockerfile` - Client container setup
- `server/Dockerfile` - Server container setup
- `toolkit/Dockerfile` - Toolkit container setup
- `docker-run.sh` - Linux/Mac startup script
- `docker-run.ps1` - Windows startup script
- `client/nginx.conf` - Nginx configuration for client

### Supporting Files
- `toolkit/requirements.txt` - Python dependencies for toolkit container

## Implementation Details

### 1. Docker Compose Configuration (Complete)
```yaml
version: '3.8'

services:
  # MongoDB service
  mongodb:
    image: mongo:5.0
    container_name: ars0n-mongodb
    restart: unless-stopped
    volumes:
      - mongodb-data:/data/db
    networks:
      - ars0n-network
    ports:
      - "27017:27017"

  # Node.js backend service
  server:
    build: ./server
    container_name: ars0n-server
    restart: unless-stopped
    depends_on:
      - mongodb
    environment:
      - MONGO_URI=mongodb://mongodb:27017/ars0n
      - PORT=5000
    networks:
      - ars0n-network
    ports:
      - "5000:5000"

  # React frontend service
  client:
    build: ./client
    container_name: ars0n-client
    restart: unless-stopped
    depends_on:
      - server
    ports:
      - "3000:80"
    networks:
      - ars0n-network

  # Toolkit service
  toolkit:
    build: ./toolkit
    container_name: ars0n-toolkit
    restart: unless-stopped
    depends_on:
      - server
    volumes:
      - toolkit-logs:/app/logs
      - toolkit-wordlists:/app/wordlists
      - toolkit-screenshots:/app/screenshots
      - toolkit-reports:/app/reports
    environment:
      - API_URL=http://server:5000/api
    networks:
      - ars0n-network

networks:
  ars0n-network:
    driver: bridge

volumes:
  mongodb-data:
  toolkit-logs:
  toolkit-wordlists:
  toolkit-screenshots:
  toolkit-reports:
```

### 2. Client Dockerfile (Complete)
```dockerfile
# Build stage
FROM node:16 as build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 3. Server Dockerfile (Complete)
```dockerfile
FROM node:16

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5000

CMD ["node", "server.js"]
```

### 4. Toolkit Dockerfile (Complete)
```dockerfile
FROM kalilinux/kali-rolling

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get -y upgrade && apt-get install -y \
    python3 \
    python3-pip \
    git \
    curl \
    wget \
    netcat-traditional \
    dnsutils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs screenshots reports wordlists temp

# Keep container running and start service
CMD ["python3", "toolkit-service.py"]
```

### 5. Linux/Mac Run Script (Complete)
```bash
#!/bin/bash

# Docker run script for Ars0n Framework
echo "Starting Ars0n Framework Docker containers..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "Error: docker-compose.yml not found in current directory."
    exit 1
fi

# Stop any existing containers
echo "Stopping existing containers if running..."
docker-compose down

# Start containers
echo "Starting containers..."
docker-compose up -d

# Check if all containers are running
sleep 5
RUNNING_CONTAINERS=$(docker-compose ps -q | wc -l)
if [ "$RUNNING_CONTAINERS" -eq 4 ]; then
    echo "All containers started successfully!"
    echo "Ars0n Framework is now running at: http://localhost:3000"
else
    echo "Some containers failed to start. Please check with 'docker-compose ps'"
fi

# Display container status
echo "Container status:"
docker-compose ps
```

### 6. Windows Run Script (Complete)
```powershell
# PowerShell script for running Ars0n Framework on Windows
Write-Host "Starting Ars0n Framework Docker containers..." -ForegroundColor Green

# Check if Docker is installed
try {
    docker --version | Out-Null
} catch {
    Write-Host "Docker is not installed or not in PATH. Please install Docker Desktop for Windows and try again." -ForegroundColor Red
    exit 1
}

# Check if docker-compose.yml exists
if (-not (Test-Path "docker-compose.yml")) {
    Write-Host "Error: docker-compose.yml not found in current directory." -ForegroundColor Red
    exit 1
}

# Stop any existing containers
Write-Host "Stopping existing containers if running..." -ForegroundColor Yellow
docker-compose down

# Start containers
Write-Host "Starting containers..." -ForegroundColor Yellow
docker-compose up -d

# Check if all containers are running
Start-Sleep -Seconds 5
$runningContainers = (docker-compose ps -q).Count
if ($runningContainers -eq 4) {
    Write-Host "All containers started successfully!" -ForegroundColor Green
    Write-Host "Ars0n Framework is now running at: http://localhost:3000" -ForegroundColor Cyan
} else {
    Write-Host "Some containers failed to start. Please check with 'docker-compose ps'" -ForegroundColor Red
}

# Display container status
Write-Host "Container status:" -ForegroundColor Yellow
docker-compose ps
```

### 7. Nginx Configuration (Complete)
```nginx
server {
    listen 80;
    
    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
    }
    
    # Proxy API requests to the backend server
    location /api {
        proxy_pass http://server:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
    
    # Enable CORS
    add_header 'Access-Control-Allow-Origin' '*' always;
    add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE' always;
    add_header 'Access-Control-Allow-Headers' 'X-Requested-With,Content-Type,Authorization' always;
}
```

## Remaining Tasks

1. Test containers on Linux environment
   - Verify all services start correctly
   - Test full scan workflow
   - Verify data persistence
   - Status: Not Started

2. Test containers on Windows environment
   - Verify all services start correctly on Windows with Docker Desktop
   - Test full scan workflow
   - Verify data persistence
   - Status: Not Started

3. Document Docker usage in README.md
   - Add detailed instructions for Docker installation
   - Include troubleshooting section
   - Status: Complete

4. Add health checks to Docker Compose
   - Implement proper health checks for each service
   - Status: Not Started

5. Optimize container size
   - Review and optimize Dockerfiles for smaller image size
   - Status: Not Started 