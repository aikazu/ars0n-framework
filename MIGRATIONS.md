# MIGRATIONS.md - Ars0n Framework Database Migrations

This document tracks database schema migrations for the Ars0n Framework. Each migration is documented with steps for both applying and rolling back changes.

## Migration Process

The Ars0n Framework currently uses MongoDB as its primary database. Because MongoDB is schema-less, migrations typically involve:

1. Data structure changes in the application models
2. Data transformation for existing records
3. Validation updates to ensure data integrity

## Planned Migrations

### M001: Standardize Scan Results Schema

**Description:** Restructure scan results collection to follow a consistent schema and improve query performance.

**Current State:**
- Scan results are stored with varying structures depending on the scan type
- Limited indexing on common query fields
- Inconsistent naming conventions for similar data points

**Target State:**
- Unified schema with consistent field naming
- Proper indexing on frequently queried fields
- Normalized references to domains and subdomains

**Migration Procedure:**
1. Create a backup of the current scan_results collection
```
mongodump --db ars0n_framework --collection scan_results --out ./backup
```

2. Create a new collection with the updated schema
```
db.createCollection("scan_results_new")
```

3. Transform and copy existing data to the new schema
```javascript
db.scan_results.find().forEach(function(doc) {
  // Transform document to new schema
  let newDoc = {
    scanId: doc.scanId || doc.scan_id || generateId(),
    timestamp: doc.timestamp || doc.created_at || new Date(),
    domainId: doc.domainId || doc.domain_id,
    targetUrl: doc.targetUrl || doc.target_url || doc.url,
    scanType: doc.scanType || doc.scan_type || "unknown",
    findings: Array.isArray(doc.findings) ? doc.findings : [],
    metadata: {
      toolVersion: doc.toolVersion || doc.tool_version,
      scanDuration: doc.scanDuration || doc.duration,
      parameters: doc.parameters || {}
    },
    status: doc.status || "completed"
  };
  
  db.scan_results_new.insertOne(newDoc);
});
```

4. Create indexes on the new collection
```
db.scan_results_new.createIndex({ "scanId": 1 })
db.scan_results_new.createIndex({ "domainId": 1 })
db.scan_results_new.createIndex({ "timestamp": -1 })
db.scan_results_new.createIndex({ "targetUrl": 1 })
db.scan_results_new.createIndex({ "scanType": 1 })
```

5. Rename collections to swap old with new
```
db.scan_results.renameCollection("scan_results_old")
db.scan_results_new.renameCollection("scan_results")
```

**Rollback Procedure:**
1. Drop the new scan_results collection
```
db.scan_results.drop()
```

2. Rename the backup collection back to the original name
```
db.scan_results_old.renameCollection("scan_results")
```

**Verification Steps:**
1. Verify count of documents matches between old and new collections
```
db.scan_results.count() === db.scan_results_old.count()
```

2. Run sample queries to ensure data can be accessed correctly
```
db.scan_results.find({ scanType: "nuclei" }).limit(10)
```

3. Verify application functionality with the new schema

**Estimated Downtime:** 5-10 minutes depending on data volume

**Pre-migration Checklist:**
- [ ] Full database backup
- [ ] Test migration on development environment
- [ ] Update application code to use new schema
- [ ] Schedule maintenance window
- [ ] Notify users of scheduled downtime

**Post-migration Validation:**
- [ ] Verify document count matches pre-migration
- [ ] Verify indexes are created correctly
- [ ] Test all application features that use scan results
- [ ] Monitor application logs for errors
- [ ] Monitor query performance

## Completed Migrations

No migrations have been completed yet.

## Migration ID Reference

| Migration ID | Description | Date Applied | Applied By |
|--------------|-------------|--------------|------------|
| M001 | Standardize Scan Results Schema | Pending | - | 