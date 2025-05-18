# SUBTASK-T004.md - Unified Logging System

## Parent Task
**T004**: Implement unified logging system

## Specific Goal
Create a consistent, centralized logging system across all components of the Ars0n Framework to improve debugging, monitoring, and troubleshooting capabilities.

## Dependencies
None

## Implementation Approach

The unified logging approach will follow these key principles:
1. Consistent log format across all components (client, server, toolkit)
2. Centralized log storage with appropriate rotation
3. Log levels to control verbosity
4. Structured logging for better parsing and analysis
5. Correlation IDs to track operations across components

## Progress Status: 0%

## Validation Criteria
- All components use the same logging format
- Logs include timestamp, component, level, and message at minimum
- Logs are stored in a predictable location
- Log levels can be configured per component
- Critical errors are easily identifiable
- Long-running processes provide appropriate progress indicators

## Files to Modify

### Primary Files
- `toolkit/toolkit-service.py` - Main toolkit service
- `toolkit/wildfire.py` - Wildfire scanning module
- `toolkit/slowburn.py` - Slowburn scanning module
- `server/server.js` - Node.js backend
- `client/src/utils/` - Add client-side logging utilities

### Supporting Files
- Create `toolkit/utils/logger.py` - Python logging utilities
- Create `server/utils/logger.js` - Server logging utilities
- Create `client/src/utils/logger.js` - Client logging utilities

## Implementation Details

### 1. Python Logging Utility (Toolkit Component)

```python
# toolkit/utils/logger.py
import logging
import os
import json
import sys
from datetime import datetime

class CustomFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    COLORS = {
        'DEBUG': '\033[94m',  # Blue
        'INFO': '\033[92m',   # Green
        'WARNING': '\033[93m', # Yellow
        'ERROR': '\033[91m',  # Red
        'CRITICAL': '\033[91m\033[1m', # Bold Red
        'RESET': '\033[0m'    # Reset
    }
    
    def format(self, record):
        log_fmt = f"{self.COLORS.get(record.levelname, self.COLORS['RESET'])}"
        log_fmt += f"[{record.levelname}] {self.COLORS['RESET']}"
        log_fmt += f"[{record.name}] {record.getMessage()}"
        
        if record.exc_info:
            log_fmt += f"\n{self.formatException(record.exc_info)}"
            
        return log_fmt

def setup_logger(name, log_file=None, level=logging.INFO):
    """
    Setup a logger with both file and console handlers
    
    Args:
        name (str): Logger name, typically the module name
        log_file (str, optional): Path to log file. If None, only console logging is setup
        level (int, optional): Logging level. Defaults to INFO.
        
    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers if any
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)
    
    # Create file handler if log file is specified
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_format = logging.Formatter(
            '%(asctime)s [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger

def log_execution(logger, command, process_id=None):
    """
    Log command execution with standardized format
    
    Args:
        logger (logging.Logger): Logger to use
        command (str): Command being executed
        process_id (int, optional): Process ID if available
    """
    if process_id:
        logger.info(f"Executing command [PID:{process_id}]: {command}")
    else:
        logger.info(f"Executing command: {command}")

def log_scan_start(logger, target, scan_type, scan_id):
    """
    Log scan start with standardized format
    
    Args:
        logger (logging.Logger): Logger to use
        target (str): Target being scanned
        scan_type (str): Type of scan
        scan_id (str): Unique scan identifier
    """
    logger.info(f"Scan started - Type: {scan_type}, Target: {target}, ID: {scan_id}")

def log_scan_complete(logger, target, scan_type, scan_id, duration_seconds, findings_count):
    """
    Log scan completion with standardized format
    
    Args:
        logger (logging.Logger): Logger to use
        target (str): Target being scanned
        scan_type (str): Type of scan
        scan_id (str): Unique scan identifier
        duration_seconds (float): Scan duration in seconds
        findings_count (int): Number of findings
    """
    logger.info(
        f"Scan completed - Type: {scan_type}, Target: {target}, ID: {scan_id}, "
        f"Duration: {duration_seconds:.2f}s, Findings: {findings_count}"
    )

def log_error(logger, error_message, error=None, context=None):
    """
    Log error with standardized format
    
    Args:
        logger (logging.Logger): Logger to use
        error_message (str): Error message
        error (Exception, optional): Exception object if available
        context (dict, optional): Additional context information
    """
    if context:
        context_str = ", ".join(f"{k}={v}" for k, v in context.items())
        logger.error(f"{error_message} - Context: {context_str}")
    else:
        logger.error(error_message)
        
    if error:
        logger.exception(error)
```

### 2. Node.js Logging Utility (Server Component)

```javascript
// server/utils/logger.js
const winston = require('winston');
const path = require('path');
const fs = require('fs');

// Ensure logs directory exists
const logDir = path.join(__dirname, '../logs');
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir, { recursive: true });
}

// Define log format
const logFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.errors({ stack: true }),
  winston.format.splat(),
  winston.format.json()
);

// Create the logger
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: logFormat,
  defaultMeta: { service: 'ars0n-server' },
  transports: [
    // Console transport
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.printf(({ timestamp, level, message, service, ...meta }) => {
          return `${timestamp} [${level}] [${service}]: ${message} ${
            Object.keys(meta).length ? JSON.stringify(meta) : ''
          }`;
        })
      ),
    }),
    // File transport - Error logs
    new winston.transports.File({ 
      filename: path.join(logDir, 'error.log'),
      level: 'error'
    }),
    // File transport - Combined logs
    new winston.transports.File({ 
      filename: path.join(logDir, 'combined.log')
    }),
  ],
});

// Helper function for API requests
logger.logApiRequest = (req, res, responseTime) => {
  const { method, originalUrl, ip, body } = req;
  
  logger.info(`API Request`, {
    method,
    url: originalUrl,
    ip,
    statusCode: res.statusCode,
    responseTime: `${responseTime}ms`,
    requestBody: process.env.NODE_ENV !== 'production' ? body : undefined,
  });
};

// Helper function for API errors
logger.logApiError = (req, err) => {
  const { method, originalUrl, ip, body } = req;
  
  logger.error(`API Error`, {
    method,
    url: originalUrl,
    ip,
    error: err.message,
    stack: process.env.NODE_ENV !== 'production' ? err.stack : undefined,
    requestBody: process.env.NODE_ENV !== 'production' ? body : undefined,
  });
};

// Helper function for database operations
logger.logDbOperation = (operation, collection, query, duration) => {
  logger.debug(`Database Operation`, {
    operation,
    collection,
    query: JSON.stringify(query),
    duration: `${duration}ms`,
  });
};

// Helper function for toolkit interactions
logger.logToolkitInteraction = (action, params, result) => {
  logger.info(`Toolkit Interaction`, {
    action,
    params,
    result: result ? 'Success' : 'Failed',
  });
};

module.exports = logger;
```

### 3. React Client Logging Utility

```javascript
// client/src/utils/logger.js
// Simple logging utility for React client

// Log levels
const LOG_LEVELS = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3,
};

// Current log level (can be set via localStorage or environment)
const getCurrentLogLevel = () => {
  // Check localStorage first
  const storedLevel = localStorage.getItem('logLevel');
  if (storedLevel && LOG_LEVELS[storedLevel] !== undefined) {
    return LOG_LEVELS[storedLevel];
  }
  
  // Default to INFO in production, DEBUG in development
  return process.env.NODE_ENV === 'production' ? LOG_LEVELS.INFO : LOG_LEVELS.DEBUG;
};

// Format log messages
const formatMessage = (level, message, data) => {
  const timestamp = new Date().toISOString();
  let formattedMessage = `[${timestamp}] [${level}] ${message}`;
  
  if (data) {
    try {
      formattedMessage += ` ${JSON.stringify(data)}`;
    } catch (e) {
      formattedMessage += ` [Data could not be stringified]`;
    }
  }
  
  return formattedMessage;
};

// Send logs to server (for critical errors)
const sendToServer = async (level, message, data) => {
  if (level !== 'ERROR') return;
  
  try {
    const payload = {
      level,
      message,
      timestamp: new Date().toISOString(),
      data,
      userAgent: navigator.userAgent,
      url: window.location.href,
    };
    
    // Send error to server endpoint
    await fetch('/api/logs', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });
  } catch (e) {
    // Cannot log the error about error logging
    console.error('Failed to send log to server:', e);
  }
};

// Main logger object
const logger = {
  debug: (message, data) => {
    if (getCurrentLogLevel() <= LOG_LEVELS.DEBUG) {
      console.debug(formatMessage('DEBUG', message, data));
    }
  },
  
  info: (message, data) => {
    if (getCurrentLogLevel() <= LOG_LEVELS.INFO) {
      console.info(formatMessage('INFO', message, data));
    }
  },
  
  warn: (message, data) => {
    if (getCurrentLogLevel() <= LOG_LEVELS.WARN) {
      console.warn(formatMessage('WARN', message, data));
    }
  },
  
  error: (message, error, data) => {
    if (getCurrentLogLevel() <= LOG_LEVELS.ERROR) {
      console.error(formatMessage('ERROR', message, data));
      if (error && error.stack) {
        console.error(error.stack);
      }
      sendToServer('ERROR', message, { ...data, error: error?.toString(), stack: error?.stack });
    }
  },
  
  // Log API requests
  logApiRequest: (method, endpoint, params) => {
    logger.debug(`API Request: ${method} ${endpoint}`, params);
  },
  
  // Log API responses
  logApiResponse: (method, endpoint, status, data) => {
    const level = status >= 400 ? 'error' : 'debug';
    logger[level](`API Response: ${method} ${endpoint} (${status})`, data);
  },
  
  // Log user actions
  logUserAction: (action, details) => {
    logger.info(`User Action: ${action}`, details);
  },
  
  // Set log level programmatically
  setLogLevel: (level) => {
    if (LOG_LEVELS[level] !== undefined) {
      localStorage.setItem('logLevel', level);
    }
  },
};

export default logger;
```

### 4. Integration Plan

1. **Toolkit Integration**
   - Create utils/logger.py module
   - Update toolkit-service.py to use the new logger
   - Update wildfire.py and slowburn.py to use the new logger
   - Standardize process execution logging
   - Add scan progress logging

2. **Server Integration**
   - Add winston dependency to package.json
   - Create utils/logger.js module
   - Update server.js to use the new logger
   - Add request logging middleware
   - Update API routes to use structured logging

3. **Client Integration**
   - Create src/utils/logger.js module
   - Add error boundary with logging
   - Update API service to log requests/responses
   - Log user interactions where appropriate

## Remaining Tasks

1. Create Python logging utility
   - Implement logger.py module
   - Status: Not Started

2. Create Node.js logging utility
   - Add winston dependency
   - Implement logger.js module
   - Status: Not Started

3. Create React client logging utility
   - Implement logger.js module
   - Status: Not Started

4. Update toolkit components
   - Modify toolkit-service.py
   - Modify wildfire.py and slowburn.py
   - Status: Not Started

5. Update server components
   - Add request logging middleware
   - Update API routes
   - Status: Not Started

6. Update client components
   - Add error boundaries
   - Update API service
   - Status: Not Started

7. Testing
   - Verify logs are generated in the expected format
   - Verify logs are stored in the expected location
   - Verify error logging works correctly
   - Status: Not Started 