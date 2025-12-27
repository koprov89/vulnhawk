# VulnHawk Deployment Guide

## Prerequisites

- Docker (20.10+)
- Docker Compose (2.0+)
- Git
- 4GB RAM minimum
- 10GB disk space

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/koprov89/vulnhawk.git
cd vulnhawk
```

### 2. Start with Docker Compose

```bash
docker-compose up -d
```

This will:
- Build the backend and frontend Docker images
- Start all services
- Initialize the database

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 4. Stop the Application

```bash
docker-compose down
```

## Manual Deployment

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database:**
```bash
python ../scripts/init_db.py
```

6. **Start the server:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Set up environment:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Start development server:**
```bash
npm start
```

5. **Build for production:**
```bash
npm run build
```

## Production Deployment

### Using Docker

1. **Build production images:**
```bash
docker build -t vulnhawk-backend:prod ./backend
docker build -t vulnhawk-frontend:prod ./frontend
```

2. **Run containers:**
```bash
# Backend
docker run -d \
  --name vulnhawk-backend \
  -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./vulnhawk.db \
  -v $(pwd)/data:/app/data \
  --privileged \
  vulnhawk-backend:prod

# Frontend
docker run -d \
  --name vulnhawk-frontend \
  -p 80:80 \
  -e REACT_APP_API_URL=http://your-api-domain.com/api \
  vulnhawk-frontend:prod
```

### Using Kubernetes

Create deployment files:

**backend-deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vulnhawk-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: vulnhawk-backend
  template:
    metadata:
      labels:
        app: vulnhawk-backend
    spec:
      containers:
      - name: backend
        image: vulnhawk-backend:prod
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          value: "postgresql://user:pass@db:5432/vulnhawk"
        securityContext:
          privileged: true
---
apiVersion: v1
kind: Service
metadata:
  name: vulnhawk-backend
spec:
  selector:
    app: vulnhawk-backend
  ports:
  - port: 8000
    targetPort: 8000
```

**frontend-deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vulnhawk-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: vulnhawk-frontend
  template:
    metadata:
      labels:
        app: vulnhawk-frontend
    spec:
      containers:
      - name: frontend
        image: vulnhawk-frontend:prod
        ports:
        - containerPort: 80
        env:
        - name: REACT_APP_API_URL
          value: "http://backend-service/api"
---
apiVersion: v1
kind: Service
metadata:
  name: vulnhawk-frontend
spec:
  type: LoadBalancer
  selector:
    app: vulnhawk-frontend
  ports:
  - port: 80
    targetPort: 80
```

Deploy:
```bash
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml
```

## Environment Configuration

### Backend Environment Variables

```bash
# Database
DATABASE_URL=sqlite:///./vulnhawk.db  # or postgresql://user:pass@host/db

# CORS
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# Application
APP_NAME=VulnHawk API
APP_VERSION=0.1.0
```

### Frontend Environment Variables

```bash
# API Configuration
REACT_APP_API_URL=http://localhost:8000/api
```

## Database Migration

For production, use PostgreSQL:

1. **Install PostgreSQL:**
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# Or use Docker
docker run -d \
  --name vulnhawk-postgres \
  -e POSTGRES_PASSWORD=secretpass \
  -e POSTGRES_DB=vulnhawk \
  -p 5432:5432 \
  postgres:15
```

2. **Update environment:**
```bash
DATABASE_URL=postgresql://postgres:secretpass@localhost:5432/vulnhawk
```

3. **Install PostgreSQL driver:**
```bash
pip install psycopg2-binary
```

## Monitoring Setup

### Using Prometheus

**prometheus.yml:**
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'vulnhawk-backend'
    static_configs:
      - targets: ['backend:8000']
```

### Using Grafana

```bash
docker run -d \
  --name grafana \
  -p 3001:3000 \
  grafana/grafana
```

## Backup and Restore

### Database Backup

**SQLite:**
```bash
# Backup
sqlite3 vulnhawk.db ".backup vulnhawk_backup.db"

# Restore
sqlite3 vulnhawk.db ".restore vulnhawk_backup.db"
```

**PostgreSQL:**
```bash
# Backup
pg_dump vulnhawk > vulnhawk_backup.sql

# Restore
psql vulnhawk < vulnhawk_backup.sql
```

## Troubleshooting

### Backend Issues

**Issue: Nmap not found**
```bash
# Install nmap in container
apt-get update && apt-get install -y nmap
```

**Issue: Database connection failed**
```bash
# Check database URL
echo $DATABASE_URL

# Initialize database
python scripts/init_db.py
```

**Issue: Permission denied for nmap**
```bash
# Run container with privileged flag
docker run --privileged ...
```

### Frontend Issues

**Issue: Cannot connect to API**
```bash
# Check API URL
echo $REACT_APP_API_URL

# Verify backend is running
curl http://localhost:8000/health
```

**Issue: Build fails**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Security Hardening

### SSL/TLS Setup

Using Let's Encrypt with Certbot:

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Nginx Configuration

**nginx.conf:**
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://frontend:80;
    }

    location /api {
        proxy_pass http://backend:8000;
    }
}
```

## Performance Tuning

### Backend Optimization

1. **Use Gunicorn with multiple workers:**
```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

2. **Enable database connection pooling:**
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=0
)
```

### Frontend Optimization

1. **Enable compression in Nginx:**
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

2. **Add caching headers:**
```nginx
location /static {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## Health Checks

### Backend Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "service": "VulnHawk"}
```

### Docker Health Checks

Add to docker-compose.yml:
```yaml
services:
  backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## Maintenance

### Update CVE Database

```bash
python scripts/update_cve_db.py
```

### Clean Up Old Scans

```bash
# Delete scans older than 30 days
sqlite3 vulnhawk.db "DELETE FROM scans WHERE created_at < datetime('now', '-30 days');"
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/koprov89/vulnhawk/issues
- Documentation: https://github.com/koprov89/vulnhawk/docs
