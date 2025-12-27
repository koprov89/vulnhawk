# VulnHawk Architecture

## System Overview

VulnHawk is a network vulnerability scanner built with a modern microservices architecture. The system consists of three main components:

1. **Backend API** (FastAPI/Python)
2. **Frontend Web Application** (React)
3. **Database** (SQLite)

## High-Level Architecture

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Browser   │ ◄─────► │   Nginx     │ ◄─────► │   Backend   │
│  (React)    │         │  (Reverse   │         │  (FastAPI)  │
│             │         │   Proxy)    │         │             │
└─────────────┘         └─────────────┘         └──────┬──────┘
                                                       │
                                                       ▼
                                                ┌─────────────┐
                                                │   SQLite    │
                                                │  Database   │
                                                └─────────────┘
                                                       ▲
                                                       │
                                                ┌──────┴──────┐
                                                │    Nmap     │
                                                │   Scanner   │
                                                └─────────────┘
```

## Component Architecture

### Backend (FastAPI)

The backend is organized in a layered architecture:

```
backend/
├── app/
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection & session
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── api/
│   │   ├── routes.py        # API endpoint definitions
│   │   └── dependencies.py  # Shared dependencies
│   ├── scanner/
│   │   ├── port_scanner.py  # Nmap integration
│   │   ├── service_detector.py
│   │   ├── vuln_detector.py # CVE matching logic
│   │   └── risk_calculator.py
│   └── reports/
│       └── generator.py     # Report generation
```

**Key Technologies:**
- FastAPI: Modern web framework
- SQLAlchemy: ORM for database access
- Pydantic: Data validation
- Python-nmap: Port scanning
- Uvicorn: ASGI server

### Frontend (React)

The frontend follows a component-based architecture:

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── App.js               # Main application component
│   ├── index.js             # Application entry point
│   ├── components/
│   │   ├── Dashboard.js     # Statistics dashboard
│   │   ├── ScanForm.js      # Scan creation form
│   │   ├── ResultsTable.js  # Scan results display
│   │   └── VulnerabilityCard.js
│   ├── services/
│   │   └── api.js           # API client
│   └── styles/
│       └── App.css          # Global styles
```

**Key Technologies:**
- React 18: UI framework
- Axios: HTTP client
- CSS3: Styling

### Database Schema

```sql
┌─────────────┐
│    Scans    │
├─────────────┤
│ id (PK)     │
│ target      │
│ scan_type   │
│ status      │
│ created_at  │
│ completed_at│
└──────┬──────┘
       │ 1:N
       ▼
┌─────────────┐
│    Hosts    │
├─────────────┤
│ id (PK)     │
│ scan_id (FK)│
│ ip_address  │
│ hostname    │
│ os_info     │
└──────┬──────┘
       │ 1:N
       ▼
┌─────────────┐
│    Ports    │
├─────────────┤
│ id (PK)     │
│ host_id (FK)│
│ port_number │
│ protocol    │
│ service     │
│ version     │
└──────┬──────┘
       │ 1:N
       ▼
┌──────────────────┐
│ Vulnerabilities  │
├──────────────────┤
│ id (PK)          │
│ port_id (FK)     │
│ cve_id           │
│ severity         │
│ cvss_score       │
│ description      │
│ remediation      │
└──────────────────┘
```

## Data Flow

### Scan Creation Flow

1. User submits scan request via frontend
2. Frontend sends POST to `/api/scans`
3. Backend creates scan record in database
4. Backend initiates nmap scan
5. Nmap results are parsed
6. For each discovered service:
   - Check version against CVE database
   - Create vulnerability records if matches found
7. Update scan status to "completed"
8. Return scan results to frontend
9. Frontend displays results and vulnerabilities

### Vulnerability Detection Flow

```
Input: Service Name + Version
        ↓
    CVE Database Lookup
        ↓
    Version Comparison
        ↓
    Match Found?
    ↙        ↘
  Yes         No
   ↓           ↓
Create      Continue
Vuln Record
```

## Security Considerations

### Current Implementation
- No authentication (MVP only)
- CORS enabled for all origins
- SQLite database (single file)
- Privileged Docker container (required for nmap)

### Production Recommendations
1. **Authentication**: Implement JWT or API key authentication
2. **Authorization**: Role-based access control
3. **Database**: Migrate to PostgreSQL or MySQL
4. **CORS**: Restrict to specific origins
5. **Rate Limiting**: Implement request throttling
6. **Input Validation**: Enhanced validation for targets
7. **Network Isolation**: Separate scanning network
8. **Encryption**: TLS/SSL for API communication
9. **Secrets Management**: Use environment variables or vault
10. **Audit Logging**: Track all scan activities

## Scalability

### Current Limitations
- Synchronous scan execution
- Single-threaded scanning
- In-memory CVE database
- SQLite limitations

### Scaling Strategies

**Horizontal Scaling:**
- Queue-based scan processing (RabbitMQ/Redis)
- Multiple worker instances
- Load balancer for API

**Vertical Scaling:**
- Optimize nmap scan parameters
- Parallel host scanning
- Caching layer (Redis)

**Database Scaling:**
- PostgreSQL with connection pooling
- Read replicas
- Partitioning by date

## Monitoring & Observability

Recommended additions:
- **Logging**: Structured logging with ELK stack
- **Metrics**: Prometheus + Grafana
- **Tracing**: OpenTelemetry
- **Alerting**: Alert on scan failures
- **Health Checks**: Liveness and readiness probes

## Technology Stack Summary

| Component | Technology | Version |
|-----------|------------|---------|
| Backend Framework | FastAPI | 0.104.1 |
| Backend Language | Python | 3.11 |
| Database | SQLite | 3.x |
| ORM | SQLAlchemy | 2.0.23 |
| Port Scanner | Nmap | Latest |
| Frontend Framework | React | 18.2.0 |
| HTTP Client | Axios | 1.6.2 |
| Web Server | Nginx | Alpine |
| Container Runtime | Docker | Latest |
| Orchestration | Docker Compose | 3.8 |

## Future Enhancements

1. **Scheduled Scans**: Cron-like scheduling
2. **Scan Templates**: Predefined scan configurations
3. **Export Reports**: PDF/CSV/JSON exports
4. **Webhook Notifications**: Alert on scan completion
5. **Network Discovery**: Auto-discover network ranges
6. **Custom CVE Database**: User-defined vulnerabilities
7. **Plugin System**: Extensible scanner modules
8. **Multi-tenancy**: Support for multiple organizations
9. **API Versioning**: v1, v2 API versions
10. **WebSocket Support**: Real-time scan updates
