# TESTING.md - Ars0n Framework Testing Strategy

## Testing Approach

The Ars0n Framework employs a multi-layered testing strategy that combines manual testing with automated tests. Due to the nature of the application, which interacts with external systems and security tools, testing requires a balance of:

1. **Unit Testing**: For core functions and utilities
2. **Integration Testing**: For component interactions
3. **End-to-End Testing**: For complete workflows
4. **Security Testing**: To ensure secure operation

## Test Environments

| Environment | Purpose | Configuration |
|-------------|---------|---------------|
| **Development** | Local testing during development | Docker containers on developer machines |
| **Testing** | Automated test execution | Dedicated test server or CI/CD pipeline |
| **Staging** | Pre-release validation | Mirror of production environment |
| **Production** | Live environment | Deployment target |

## Test Categories

### Unit Tests

**Approach**: Jest for JavaScript components, pytest for Python modules  
**Coverage Goal**: 70% code coverage for critical utility functions

**Key Areas**:
- Data processing utilities
- API endpoint logic
- Database query construction
- Tool result parsing

### Integration Tests

**Approach**: Component-to-component tests with mock external dependencies  
**Coverage Goal**: Test all critical integration points

**Key Areas**:
- Client-server communication
- Server-toolkit service interaction
- Database operations
- API contract validation

### End-to-End Tests

**Approach**: Cypress for UI workflows, custom scripts for CLI  
**Coverage Goal**: Cover all primary user workflows

**Key Areas**:
- Complete scan workflows
- Report generation
- User authentication flows
- Configuration management

### Security Tests

**Approach**: Static analysis, dependency scanning, and penetration testing  
**Coverage Goal**: Address all high and medium severity findings

**Key Areas**:
- API security
- Input validation
- Dependency vulnerabilities
- Access control

## Test Case Templates

### Unit Test Template

```javascript
describe('Component: [Component Name]', () => {
  describe('Function: [Function Name]', () => {
    it('should [expected behavior] when [condition]', () => {
      // Arrange
      const input = [test input];
      const expected = [expected output];
      
      // Act
      const result = functionUnderTest(input);
      
      // Assert
      expect(result).toEqual(expected);
    });
    
    it('should handle errors when [error condition]', () => {
      // Test error handling
    });
  });
});
```

### Integration Test Template

```javascript
describe('Integration: [Component A] with [Component B]', () => {
  beforeEach(() => {
    // Setup test environment
  });
  
  afterEach(() => {
    // Cleanup
  });
  
  it('should successfully [operation] when [condition]', async () => {
    // Arrange
    const testData = [test data];
    
    // Act
    const result = await integratedOperation(testData);
    
    // Assert
    expect(result).toHaveProperty('[expected property]');
  });
});
```

### End-to-End Test Template

```javascript
describe('Workflow: [Workflow Name]', () => {
  before(() => {
    // Setup test environment
  });
  
  it('completes [workflow] successfully', () => {
    // User journey steps
    cy.visit('/starting-page');
    cy.get('[data-test-id="element"]').click();
    // Additional steps...
    
    // Final assertion
    cy.get('[data-test-id="result"]').should('contain', 'Expected Result');
  });
});
```

## Mock Data Strategy

1. **Static Fixtures**: JSON files containing representative data for unit tests
2. **Factory Functions**: For generating test data with controlled variations
3. **Recorded Responses**: From actual tools for integration testing
4. **In-memory Database**: For database integration tests

## Test Data Examples

### Sample Subdomain Data
```json
{
  "fqdn": "example.com",
  "recon": {
    "subdomains": {
      "amass": ["sub1.example.com", "sub2.example.com"],
      "subfinder": ["sub2.example.com", "sub3.example.com"],
      "assetfinder": ["sub1.example.com", "sub4.example.com"],
      "httprobe": ["https://sub1.example.com", "https://sub2.example.com"]
    }
  }
}
```

### Sample Scan Result
```json
{
  "scan_id": "scan-12345",
  "target": "example.com",
  "findings": [
    {
      "severity": "high",
      "title": "SQL Injection",
      "location": "https://sub1.example.com/search?q=test",
      "details": "Parameter 'q' is vulnerable to SQL injection"
    }
  ]
}
```

## Test Automation

### CI/CD Pipeline Integration
- Run unit tests on every PR
- Run integration tests on merge to main branch
- Run full E2E suite before releases

### Automated Test Running
```bash
# Run unit tests
npm test

# Run integration tests
npm run test:integration

# Run E2E tests
npm run test:e2e
```

## Test Coverage Tracking

Coverage reports will be generated for:
- JavaScript code (client and server)
- Python modules (toolkit)

Reports will be archived with each build and tracked over time to ensure maintenance or improvement of coverage.

## Validation Rules

### Input Validation
- All user inputs must be validated at both client and server
- API parameters must conform to defined schemas
- File uploads must be validated for type and size

### Output Validation
- API responses must match defined schemas
- UI components must handle all response states
- Error messages must be consistent and helpful

## Edge Cases and Failure Testing

| Category | Edge Cases |
|----------|------------|
| **Network** | Timeout, connection loss, partial data |
| **Resources** | Low memory, high CPU usage, disk full |
| **Input** | Very large inputs, empty inputs, malformed data |
| **State** | Interrupted operations, concurrent modifications |
| **External Tools** | Tool failure, unexpected output format |

## Test Dependencies

- Jest (JavaScript testing)
- pytest (Python testing)
- Cypress (E2E testing)
- Mock service worker (API mocking)
- Docker (containerized testing)

## Future Testing Improvements

1. Property-based testing for data processing functions
2. Snapshot testing for UI components
3. Performance testing framework
4. Chaos testing for resilience verification
5. Automated security scanning integration 