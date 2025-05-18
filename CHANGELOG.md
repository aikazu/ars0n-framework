# CHANGELOG.md - Ars0n Framework

All notable changes to the Ars0n Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Docker Compose setup for containerized deployment
  - Docker Compose configuration for orchestrating all components
  - Dockerfile for Node.js server
  - Multi-stage build Dockerfile for React client
  - Kali Linux-based Dockerfile for toolkit services
  - Custom nginx configuration for client
  - `docker-run.sh` and `docker-run.ps1` scripts for cross-platform container management
- Improved process management in toolkit service
- Comprehensive documentation structure following standardized format
- REFACTORING.md document for tracking code refactoring initiatives
- MIGRATIONS.md document for tracking database schema changes

### Changed
- Refactored toolkit service for better stability and process management
- Updated documentation structure to follow project requirements
- Improved SESSION.md and STATE.md tracking format
- Enhanced TASK.md with new documentation-related tasks

### Fixed
- Process orphaning issues in toolkit services
- Process cleanup on toolkit service restart

### Security
- Fixed potential security vulnerabilities in process management

## [0.0.2-alpha] - 2023-06-15

### Added
- Initial alpha release available for download
- Core scanning functionality with Wildfire module
- Fire-Starter, Fire-Cloud, and Fire-Scanner sub-modules
- Basic web application interface with React frontend
- Node.js backend API
- MongoDB integration for data storage
- Installation script for Kali Linux

### Known Issues
- Installation issues on some systems
- MongoDB setup complications
- Process management problems in long-running scans

## Migration Instructions
For users upgrading from v0.0.1 (internal) to v0.0.2-alpha:
- A complete reinstallation is recommended
- No data migration is supported between versions
- Follow the Quick Start guide in README.md

## Future Plans
Upcoming major features planned for v0.1.0:
- User authentication system
- Enhanced reporting capabilities
- Improved scan visualization
- Cross-platform support improvements 