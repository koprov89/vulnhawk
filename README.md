# 🦅 VulnHawk

Network vulnerability scanner - Qualys-like security tool for identifying vulnerabilities in network infrastructure.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)

## 🌟 Features

- **Network Scanning**: Automated port scanning using Nmap
- **Vulnerability Detection**: CVE-based vulnerability identification
- **Risk Assessment**: CVSS-based risk scoring
- **Web Interface**: Modern React-based dashboard
- **REST API**: Comprehensive API for integration
- **Real-time Updates**: Live scan status updates
- **Report Generation**: Detailed vulnerability reports
- **Docker Support**: Easy deployment with Docker Compose

## 🏗️ Architecture

VulnHawk follows a modern microservices architecture:

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
```

## 🚀 Quick Start

### Prerequisites

- Docker (20.10+)
- Docker Compose (2.0+)
- Git

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/koprov89/vulnhawk.git
cd vulnhawk
```

2. **Start the application:**
```bash
docker-compose up -d
```

3. **Access the application:**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### First Scan

1. Navigate to http://localhost:3000
2. Enter a target IP or hostname (e.g., `scanme.nmap.org`)
3. Select scan type (Quick or Full)
4. Click "Start Scan"
5. View results and vulnerabilities

## 📖 Documentation

- [API Documentation](docs/API.md) - Complete API reference
- [Architecture](docs/ARCHITECTURE.md) - System architecture details
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment instructions
- [Contributing](CONTRIBUTING.md) - Contribution guidelines
- [Security Policy](SECURITY.md) - Security best practices

## 🛠️ Manual Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python ../scripts/init_db.py

# Start server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## 📊 Technology Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Language**: Python 3.11
- **Database**: SQLite (PostgreSQL for production)
- **ORM**: SQLAlchemy 2.0.23
- **Scanner**: Nmap via python-nmap
- **Server**: Uvicorn

### Frontend
- **Framework**: React 18.2.0
- **HTTP Client**: Axios 1.6.2
- **Styling**: CSS3
- **Build Tool**: React Scripts 5.0.1

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Web Server**: Nginx (Alpine)

## 🔍 API Usage

### Create a Scan

```bash
curl -X POST http://localhost:8000/api/scans \
  -H "Content-Type: application/json" \
  -d '{"target": "scanme.nmap.org", "scan_type": "quick"}'
```

### Get Scan Results

```bash
curl http://localhost:8000/api/scans/1
```

### Get Vulnerabilities

```bash
curl http://localhost:8000/api/scans/1/vulnerabilities
```

### Get Risk Assessment

```bash
curl http://localhost:8000/api/scans/1/risk
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pip install pytest pytest-cov
pytest tests/ -v --cov=app
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📦 Project Structure

```
vulnhawk/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes and dependencies
│   │   ├── scanner/     # Scanning modules
│   │   ├── reports/     # Report generation
│   │   ├── models.py    # Database models
│   │   ├── schemas.py   # Pydantic schemas
│   │   └── main.py      # Application entry point
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API client
│   │   └── styles/      # CSS styles
│   ├── package.json
│   └── Dockerfile
├── docs/                # Documentation
├── scripts/             # Utility scripts
├── .github/             # CI/CD workflows
└── docker-compose.yml   # Docker Compose config
```

## 🔐 Security

⚠️ **Important**: This is an MVP version with limited security features.

**Current Limitations:**
- No authentication
- No authorization
- CORS enabled for all origins
- Privileged Docker containers

**Production Recommendations:**
- Implement JWT authentication
- Add role-based access control
- Restrict CORS origins
- Use PostgreSQL instead of SQLite
- Enable HTTPS/TLS
- Implement rate limiting
- Add input validation and sanitization

See [SECURITY.md](SECURITY.md) for detailed security guidelines.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Roadmap

- [ ] User authentication and authorization
- [ ] Scheduled scans
- [ ] Email notifications
- [ ] PDF report export
- [ ] Network discovery
- [ ] Plugin system
- [ ] Multi-tenancy support
- [ ] WebSocket real-time updates
- [ ] Advanced reporting dashboard

## 🐛 Known Issues

- Docker builds may have SSL certificate issues in some environments (use `--trusted-host` flag)
- Nmap requires privileged container mode
- SQLite is not suitable for concurrent scans (use PostgreSQL in production)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Nmap](https://nmap.org/) - Network scanner
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [React](https://react.dev/) - UI library
- [CVE Database](https://cve.mitre.org/) - Vulnerability data

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/koprov89/vulnhawk/issues)
- **Documentation**: [docs/](docs/)
- **Security**: See [SECURITY.md](SECURITY.md)

## ⭐ Star History

If you find VulnHawk useful, please consider giving it a star! ⭐

---

**Made with ❤️ by the VulnHawk Team**
