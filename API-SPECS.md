# API-SPECS.md - Ars0n Framework API Specifications

## Base URLs and Versioning

- **Server API**: `http://localhost:8000/api`
- **Toolkit Service**: `http://localhost:5000`

Currently, the API does not use explicit versioning in the URL. Future implementations will use the format `/api/v1/...` to support versioning.

## Authentication Methods

The current implementation does not include authentication. Future versions will implement:

- JWT-based authentication
- Token-based API access

## Server API Endpoints

### FQDN Management

#### GET `/api/fqdn/all`

Retrieves all FQDNs (Fully Qualified Domain Names) in the database.

**Response Format**:
```json
[
  {
    "_id": "60f1a7b3e6b3f32a4c9b4d7e",
    "fqdn": "example.com",
    "recon": {
      "subdomains": {
        "amass": ["sub1.example.com", "sub2.example.com"],
        "subfinder": ["sub2.example.com", "sub3.example.com"],
        "assetfinder": ["sub1.example.com", "sub4.example.com"],
        "httprobe": ["https://sub1.example.com", "https://sub2.example.com"]
      }
    },
    "createdAt": "2023-01-15T12:00:00.000Z",
    "updatedAt": "2023-01-16T14:30:00.000Z"
  }
]
```

**Status Codes**:
- 200: Success
- 500: Server error

#### POST `/api/fqdn/new`

Adds a new FQDN to the database.

**Request Parameters**:
```json
{
  "fqdn": "example.com"
}
```

**Response Format**:
```json
{
  "_id": "60f1a7b3e6b3f32a4c9b4d7e",
  "fqdn": "example.com",
  "recon": {
    "subdomains": {
      "amass": [],
      "subfinder": [],
      "assetfinder": [],
      "httprobe": []
    }
  },
  "createdAt": "2023-07-01T12:00:00.000Z",
  "updatedAt": "2023-07-01T12:00:00.000Z"
}
```

**Status Codes**:
- 200: Success
- 400: Bad request
- 500: Server error

#### POST `/api/fqdn/update/:id`

Updates an existing FQDN with new data.

**URL Parameters**:
- `id`: MongoDB ID of the FQDN to update

**Request Parameters**:
```json
{
  "recon": {
    "subdomains": {
      "amass": ["sub1.example.com", "sub2.example.com"]
    }
  }
}
```

**Response Format**:
```json
{
  "acknowledged": true,
  "modifiedCount": 1,
  "upsertedId": null,
  "upsertedCount": 0,
  "matchedCount": 1
}
```

**Status Codes**:
- 200: Success
- 400: Bad request
- 404: FQDN not found
- 500: Server error

### Log Management

#### POST `/api/log/new`

Adds a new log entry to the database.

**Request Parameters**:
```json
{
  "scan": "Wildfire.py -- 2023-07-01T12:00:00.000Z",
  "logFile": [
    "[MSG] 2023-07-01T12:00:00.000Z | Wildfire.py -- Running Fire-Starter.py -> example.com",
    "[MSG] 2023-07-01T12:05:00.000Z | Wildfire.py -- Running Fire-Cloud.py -> example.com"
  ]
}
```

**Response Format**:
```json
{
  "_id": "60f1a7b3e6b3f32a4c9b4d7f",
  "scan": "Wildfire.py -- 2023-07-01T12:00:00.000Z",
  "logFile": [
    "[MSG] 2023-07-01T12:00:00.000Z | Wildfire.py -- Running Fire-Starter.py -> example.com",
    "[MSG] 2023-07-01T12:05:00.000Z | Wildfire.py -- Running Fire-Cloud.py -> example.com"
  ],
  "createdAt": "2023-07-01T12:10:00.000Z",
  "updatedAt": "2023-07-01T12:10:00.000Z"
}
```

**Status Codes**:
- 200: Success
- 400: Bad request
- 500: Server error

#### GET `/api/log/all`

Retrieves all log entries from the database.

**Response Format**:
```json
[
  {
    "_id": "60f1a7b3e6b3f32a4c9b4d7f",
    "scan": "Wildfire.py -- 2023-07-01T12:00:00.000Z",
    "logFile": [
      "[MSG] 2023-07-01T12:00:00.000Z | Wildfire.py -- Running Fire-Starter.py -> example.com",
      "[MSG] 2023-07-01T12:05:00.000Z | Wildfire.py -- Running Fire-Cloud.py -> example.com"
    ],
    "createdAt": "2023-07-01T12:10:00.000Z",
    "updatedAt": "2023-07-01T12:10:00.000Z"
  }
]
```

**Status Codes**:
- 200: Success
- 500: Server error

## Toolkit Service API

### GET `/ping`

Health check endpoint for the toolkit service.

**Response Format**:
```json
{
  "message": "pong!"
}
```

**Status Codes**:
- 200: Service is running

### GET `/status`

Returns the current status of any running scan.

**Response Format**:
```json
{
  "scan_running": true,
  "scan_step": 5,
  "scan_complete": 34,
  "scan_step_name": "Running Nuclei Basic",
  "scan_target": "example.com",
  "core_module": "Wildfire.py"
}
```

**Status Codes**:
- 200: Success

### POST `/update-scan`

Updates the status of a currently running scan.

**Request Parameters**:
```json
{
  "stepName": "Running Nuclei Basic",
  "target_domain": "example.com"
}
```

**Response Format**:
```json
{
  "scan_running": true,
  "scan_step": 6,
  "scan_step_name": "Running Nuclei Basic",
  "target_domain": "example.com"
}
```

**Status Codes**:
- 200: Success
- 400: Bad request (no scan running)

### POST `/wildfire`

Starts a Wildfire scan with the specified parameters.

**Request Parameters**:
```json
{
  "fireStarter": true,
  "fireCloud": true,
  "fireScanner": false,
  "fqdn": "example.com",
  "scanSingleDomain": true,
  "domainCount": 1
}
```

**Response Format**:
```json
{
  "message": "Done!"
}
```

**Status Codes**:
- 200: Success
- 400: Bad request (scan already running)

### GET `/terminate-subprocesses`

Terminates all running subprocesses.

**Response Format**:
```json
{
  "message": "Subprocesses terminated successfully"
}
```

**Status Codes**:
- 200: Success
- 500: Server error

### POST `/collect_sceenshots`

Triggers the collection of screenshots for discovered domains.

**Response Format**:
```
"Done!"
```

**Status Codes**:
- 200: Success

## Rate Limiting

Currently, no rate limiting is implemented. Future versions will include rate limiting to prevent abuse.

## Example Requests and Responses

### Adding a New FQDN

**Request:**
```bash
curl -X POST http://localhost:8000/api/fqdn/new \
  -H "Content-Type: application/json" \
  -d '{"fqdn":"example.com"}'
```

**Response:**
```json
{
  "_id": "60f1a7b3e6b3f32a4c9b4d7e",
  "fqdn": "example.com",
  "recon": {
    "subdomains": {
      "amass": [],
      "subfinder": [],
      "assetfinder": [],
      "httprobe": []
    }
  },
  "createdAt": "2023-07-01T12:00:00.000Z",
  "updatedAt": "2023-07-01T12:00:00.000Z"
}
```

### Starting a Wildfire Scan

**Request:**
```bash
curl -X POST http://localhost:5000/wildfire \
  -H "Content-Type: application/json" \
  -d '{
    "fireStarter": true,
    "fireCloud": true,
    "fireScanner": false,
    "fqdn": "example.com",
    "scanSingleDomain": true,
    "domainCount": 1
  }'
```

**Response:**
```json
{
  "message": "Done!"
}
```

### Checking Scan Status

**Request:**
```bash
curl -X GET http://localhost:5000/status
```

**Response:**
```json
{
  "scan_running": true,
  "scan_step": 3,
  "scan_complete": 34,
  "scan_step_name": "Running Amass",
  "scan_target": "example.com",
  "core_module": "Wildfire.py"
}
```

## Future API Enhancements

1. Authentication and authorization
2. API versioning
3. Rate limiting
4. Pagination for large result sets
5. Improved error reporting
6. WebSocket support for real-time updates 