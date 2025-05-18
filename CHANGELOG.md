# CHANGELOG.md - Ars0n Framework

All notable changes to the Ars0n Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Upcoming]

### Added
- Docker Compose setup for containerized deployment
  - Docker Compose configuration for orchestrating all components
  - Dockerfile for Node.js server
  - Multi-stage build Dockerfile for React client
  - Kali Linux-based Dockerfile for toolkit services
  - Custom nginx configuration for client
  - `docker-run.sh` script for easier container management
- Improved process management in toolkit service
- Authentication system for API access
- Comprehensive documentation structure

### Changed
- Refactored toolkit service for better stability
- Enhanced installation process with better error handling
- Improved UI for scan progress visualization
- Updated README.md with Docker installation instructions

### Fixed
- Process orphaning issues in toolkit services
- MongoDB connection handling
- Error handling during installation

## [0.0.2-alpha] - 2023

### Added
- Initial alpha release available for download
- Core scanning functionality
- Web application interface
- MongoDB integration

### Known Issues
- Installation issues on some systems
- MongoDB setup complications
- Process management problems in long-running scans 