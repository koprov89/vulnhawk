# VulnHawk API Documentation

## Overview

VulnHawk provides a RESTful API for managing network vulnerability scans. The API is built with FastAPI and follows REST principles.

**Base URL:** `http://localhost:8000/api`

**API Documentation:** `http://localhost:8000/docs` (Swagger UI)

## Authentication

Currently, the MVP version does not require authentication. Future versions will include API key or JWT-based authentication.

## Endpoints

### Health Check

Check the API health status.

```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "VulnHawk"
}
```

---

### Create Scan

Create and execute a new vulnerability scan.

```
POST /api/scans
```

**Request Body:**
```json
{
  "target": "192.168.1.1",
  "scan_type": "quick"
}
```

**Parameters:**
- `target` (string, required): IP address or hostname to scan
- `scan_type` (string, optional): Type of scan - "quick" (default) or "full"

**Response:**
```json
{
  "id": 1,
  "target": "192.168.1.1",
  "scan_type": "quick",
  "status": "completed",
  "created_at": "2024-01-15T10:30:00",
  "completed_at": "2024-01-15T10:35:00"
}
```

**Status Codes:**
- `200 OK`: Scan created and completed successfully
- `500 Internal Server Error`: Scan failed

---

### List Scans

Retrieve a list of all scans.

```
GET /api/scans
```

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "target": "192.168.1.1",
    "scan_type": "quick",
    "status": "completed",
    "created_at": "2024-01-15T10:30:00",
    "completed_at": "2024-01-15T10:35:00"
  }
]
```

---

### Get Scan Details

Get detailed information about a specific scan.

```
GET /api/scans/{scan_id}
```

**Path Parameters:**
- `scan_id` (integer, required): Scan ID

**Response:**
```json
{
  "id": 1,
  "target": "192.168.1.1",
  "scan_type": "quick",
  "status": "completed",
  "created_at": "2024-01-15T10:30:00",
  "completed_at": "2024-01-15T10:35:00",
  "hosts": [
    {
      "id": 1,
      "scan_id": 1,
      "ip_address": "192.168.1.1",
      "hostname": "router.local",
      "os_info": null,
      "ports": [
        {
          "id": 1,
          "host_id": 1,
          "port_number": 22,
          "protocol": "tcp",
          "service": "ssh",
          "version": "7.2",
          "vulnerabilities": []
        }
      ]
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Scan found
- `404 Not Found`: Scan not found

---

### Get Vulnerabilities

Get all vulnerabilities discovered in a scan.

```
GET /api/scans/{scan_id}/vulnerabilities
```

**Path Parameters:**
- `scan_id` (integer, required): Scan ID

**Response:**
```json
{
  "vulnerabilities": [
    {
      "id": 1,
      "host": "192.168.1.1",
      "port": 22,
      "service": "ssh",
      "cve_id": "CVE-2016-10012",
      "severity": "high",
      "cvss_score": 7.8,
      "description": "Shared memory manager vulnerability",
      "remediation": "Upgrade to OpenSSH 7.4 or later"
    }
  ],
  "total": 1
}
```

**Status Codes:**
- `200 OK`: Vulnerabilities retrieved
- `404 Not Found`: Scan not found

---

### Get Risk Assessment

Get risk assessment for a scan.

```
GET /api/scans/{scan_id}/risk
```

**Path Parameters:**
- `scan_id` (integer, required): Scan ID

**Response:**
```json
{
  "risk_score": 47.5,
  "risk_level": "high",
  "average_cvss": 7.8,
  "critical_count": 0,
  "high_count": 2,
  "medium_count": 1,
  "low_count": 0,
  "total_vulnerabilities": 3
}
```

**Status Codes:**
- `200 OK`: Risk assessment calculated
- `404 Not Found`: Scan not found

---

### Delete Scan

Delete a scan and all associated data.

```
DELETE /api/scans/{scan_id}
```

**Path Parameters:**
- `scan_id` (integer, required): Scan ID

**Response:**
```json
{
  "message": "Scan deleted successfully"
}
```

**Status Codes:**
- `200 OK`: Scan deleted
- `404 Not Found`: Scan not found

---

## Data Models

### Scan
- `id`: Integer (primary key)
- `target`: String (IP or hostname)
- `scan_type`: String (quick/full)
- `status`: String (pending/running/completed/failed)
- `created_at`: DateTime
- `completed_at`: DateTime (nullable)

### Host
- `id`: Integer (primary key)
- `scan_id`: Integer (foreign key)
- `ip_address`: String
- `hostname`: String (nullable)
- `os_info`: String (nullable)

### Port
- `id`: Integer (primary key)
- `host_id`: Integer (foreign key)
- `port_number`: Integer
- `protocol`: String
- `service`: String (nullable)
- `version`: String (nullable)

### Vulnerability
- `id`: Integer (primary key)
- `port_id`: Integer (foreign key)
- `cve_id`: String
- `severity`: String (critical/high/medium/low)
- `cvss_score`: Float
- `description`: Text
- `remediation`: Text

---

## Error Handling

All endpoints return standard HTTP status codes:
- `200 OK`: Request successful
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

Error responses include a detail message:
```json
{
  "detail": "Error message"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented in the MVP. Future versions will include rate limiting.

---

## Examples

### Complete Workflow

1. **Create a scan:**
```bash
curl -X POST http://localhost:8000/api/scans \
  -H "Content-Type: application/json" \
  -d '{"target": "scanme.nmap.org", "scan_type": "quick"}'
```

2. **Check scan status:**
```bash
curl http://localhost:8000/api/scans/1
```

3. **Get vulnerabilities:**
```bash
curl http://localhost:8000/api/scans/1/vulnerabilities
```

4. **Get risk assessment:**
```bash
curl http://localhost:8000/api/scans/1/risk
```

---

## WebSocket Support

WebSocket support for real-time scan updates is planned for future releases.
