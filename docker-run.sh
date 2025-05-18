#!/bin/bash

# Colors for better output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Ars0n Framework Containers...${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker and Docker Compose first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Create .keys directory if it doesn't exist
mkdir -p ~/.keys
echo -e "${YELLOW}Checking for API keys directory at ~/.keys${NC}"
echo -e "${YELLOW}You can add your API keys to this directory later if needed.${NC}"

# Check if containers already exist and are running
if docker ps | grep -q "ars0n-"; then
    echo -e "${YELLOW}Ars0n Framework containers are already running.${NC}"
    echo -e "${YELLOW}Do you want to restart them? (y/n)${NC}"
    read -r answer
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        echo -e "${YELLOW}Stopping existing containers...${NC}"
        docker-compose down
    else
        echo -e "${GREEN}Exiting without changes.${NC}"
        exit 0
    fi
fi

# Build and start the containers
echo -e "${GREEN}Building and starting containers...${NC}"
docker-compose up -d --build

# Check if all containers started successfully
if [ $? -eq 0 ]; then
    echo -e "${GREEN}=======================================${NC}"
    echo -e "${GREEN}Ars0n Framework started successfully!${NC}"
    echo -e "${GREEN}=======================================${NC}"
    echo -e "${YELLOW}Access the application at:${NC}"
    echo -e "${GREEN}http://localhost:3000${NC}"
    echo -e "${YELLOW}To stop the application, run:${NC}"
    echo -e "${GREEN}docker-compose down${NC}"
else
    echo -e "${RED}Failed to start Ars0n Framework containers.${NC}"
    echo -e "${RED}Please check the logs for more information:${NC}"
    echo -e "${GREEN}docker-compose logs${NC}"
fi 