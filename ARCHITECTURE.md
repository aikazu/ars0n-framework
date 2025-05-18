# ARCHITECTURE.md - Ars0n Framework System Architecture

## Architectural Overview

The Ars0n Framework follows a multi-tier architecture composed of the following major components:

1. **Client Application**: React-based frontend for user interaction
2. **API Server**: Node.js/Express backend for data management
3. **Toolkit Service**: Python-based service for running security tools
4. **Database**: MongoDB for storing scan results and configuration

## System Diagrams

```
┌────────────────┐          ┌────────────────┐          ┌────────────────┐
│                │          │                │          │                │
│     Client     │◄────────►│  API Server    │◄────────►│    MongoDB     │
│   (React.js)   │          │  (Express.js)  │          │   Database     │
│                │          │                │          │                │
└────────────────┘          └───────┬────────┘          └────────────────┘
                                    │
                                    │
                                    ▼
                            ┌────────────────┐
                            │                │
                            │ Toolkit Service│
                            │   (Python)     │
                            │                │
                            └───────┬────────┘
                                    │
                                    │
                                    ▼
                            ┌────────────────┐
                            │                │
                            │ Security Tools │
                            │ (Various)      │
                            │                │
                            └────────────────┘
```

## Component Responsibilities

### Client Application (ID: ARCH-CLIENT-001)
- Provides user interface for configuring scans
- Displays scan results and reports
- Manages user interaction with the system
- Visualizes data through charts and tables
- Implements real-time progress updates

### API Server (ID: ARCH-SERVER-001)
- Provides RESTful API endpoints for client interaction
- Manages database connections and queries
- Handles authentication and authorization
- Communicates with the Toolkit Service
- Processes and formats data for client consumption

### Toolkit Service (ID: ARCH-TOOLKIT-001)
- Executes security scanning tools
- Manages long-running processes
- Collects and processes tool output
- Updates scan status in real-time
- Handles error conditions and recovery

### MongoDB Database (ID: ARCH-DB-001)
- Stores scan configurations and targets
- Persists scan results and findings
- Maintains user settings and preferences
- Provides historical data for trend analysis
- Enables efficient querying of security findings

## Data Flow

1. **User Initiates Scan**:
   - Client sends scan configuration to API Server
   - API Server validates and stores configuration
   - API Server triggers Toolkit Service

2. **Scan Execution**:
   - Toolkit Service runs appropriate tools
   - Progress updates sent to API Server
   - API Server forwards updates to Client

3. **Result Processing**:
   - Tools generate results in various formats
   - Toolkit Service normalizes results
   - Results stored in MongoDB
   - Summary data sent to Client

4. **Reporting**:
   - Client requests report generation
   - API Server queries MongoDB for data
   - Report formatted and returned to Client

## Design Patterns Employed

| Pattern | Application | Purpose |
|---------|-------------|---------|
| MVC | Server components | Separate data, presentation, and control logic |
| Observer | Scan monitoring | Real-time updates of scan progress |
| Factory | Tool execution | Dynamic creation of scan processes |
| Facade | Toolkit service | Simplified interface to various security tools |
| Repository | Data access | Abstraction of database operations |

## Technical Constraints

1. **Process Management**:
   - Python subprocess handling limitations
   - Need for proper process cleanup on termination

2. **Resource Limitations**:
   - High memory usage during large scans
   - CPU-intensive operations during scanning

3. **Network Dependencies**:
   - External tools require network access
   - Rate limiting by target systems

4. **Storage Constraints**:
   - Large dataset handling in MongoDB
   - Efficient storage of scan results

## Architectural Decisions and Reasoning

### AD-001: Use of MongoDB
**Decision**: Use MongoDB as the primary database.  
**Context**: Need to store varied and dynamic scan results.  
**Alternatives Considered**:
- SQLite: Too limited for concurrent access
- PostgreSQL: Requires more rigid schema
- MySQL: Similar limitations to PostgreSQL

**Reasoning**: MongoDB's flexible schema allows for storing diverse scan results without predefined structure.

### AD-002: Toolkit Service Separation
**Decision**: Implement security tools execution in a separate Python service.  
**Context**: Need to execute various command-line tools efficiently.  
**Alternatives Considered**:
- Direct execution from Node.js: Limited process control
- WebAssembly tools: Limited availability of security tools

**Reasoning**: Python provides better libraries for process control and is commonly used in security tools.

### AD-003: React Frontend
**Decision**: Use React for the client application.  
**Context**: Need for interactive, real-time UI.  
**Alternatives Considered**:
- Vue.js: Good alternative but less community support
- Angular: More complex for the needs of this application

**Reasoning**: React's component model and state management work well for displaying dynamic scan data.

## Performance Considerations

1. **Scan Execution**:
   - Parallel execution where possible
   - Resource throttling for intensive scans

2. **Database Queries**:
   - Indexing critical fields
   - Pagination for large result sets

3. **Client Performance**:
   - Lazy loading of scan results
   - Virtualized lists for large datasets

## Security Architecture

1. **API Security**:
   - Future implementation of JWT authentication
   - Input validation on all endpoints

2. **Tool Execution**:
   - Isolation of running tools
   - Validation of tool input

3. **Data Protection**:
   - Secure storage of API keys
   - Sanitization of stored scan data

4. **Network Security**:
   - HTTPS for all communications
   - Proper handling of sensitive URLs 