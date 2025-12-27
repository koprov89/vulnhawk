# Security Policy

## Supported Versions

Currently, VulnHawk is in MVP (Minimum Viable Product) stage. Security updates will be provided for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods:

### Email

Send an email to: **security@vulnhawk-project.com** (if available) or the repository maintainer.

Include the following information:
- Type of vulnerability
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### Response Timeline

- **Initial Response**: Within 48 hours
- **Confirmation**: Within 5 business days
- **Fix Timeline**: Depends on severity
  - Critical: 1-7 days
  - High: 7-14 days
  - Medium: 14-30 days
  - Low: 30-90 days

## Security Considerations

### Known Limitations (MVP)

The current MVP version has the following security limitations:

1. **No Authentication**: API endpoints are publicly accessible
2. **No Authorization**: No user roles or permissions
3. **CORS Wide Open**: Accepts requests from any origin
4. **Privileged Containers**: Docker containers run with elevated privileges for nmap
5. **SQLite Database**: Not suitable for production multi-user scenarios
6. **No Rate Limiting**: Susceptible to abuse
7. **No Input Sanitization**: Limited validation on target inputs
8. **No Encryption**: Data stored in plaintext
9. **No Audit Logging**: No tracking of user actions
10. **Hardcoded CVE Database**: No automatic updates

### Production Recommendations

Before deploying to production, address these security concerns:

#### 1. Authentication & Authorization

Implement proper authentication:
```python
# Example: Add JWT authentication
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/scans")
async def get_scans(token: str = Depends(oauth2_scheme)):
    # Verify token and proceed
    pass
```

#### 2. Input Validation

Validate and sanitize all inputs:
```python
import ipaddress
import re

def validate_target(target: str) -> bool:
    # Validate IP address
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        pass
    
    # Validate hostname
    hostname_pattern = r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63})*$'
    return bool(re.match(hostname_pattern, target))
```

#### 3. CORS Configuration

Restrict CORS to specific origins:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
```

#### 4. Rate Limiting

Implement rate limiting:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/api/scans")
@limiter.limit("10/minute")
async def get_scans(request: Request):
    pass
```

#### 5. Database Security

Use PostgreSQL with proper credentials:
```python
DATABASE_URL = "postgresql://user:strong_password@localhost/vulnhawk"

# Use environment variables
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    
    class Config:
        env_file = ".env"
```

#### 6. HTTPS/TLS

Always use HTTPS in production:
```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
}
```

#### 7. Docker Security

Run containers with minimal privileges:
```yaml
services:
  backend:
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_RAW  # Only for nmap
      - NET_ADMIN
```

#### 8. Secrets Management

Never commit secrets to version control:
```bash
# Use environment variables
export DATABASE_PASSWORD="strong_password"
export SECRET_KEY="random_secret_key"

# Or use secret management tools
# - HashiCorp Vault
# - AWS Secrets Manager
# - Azure Key Vault
```

## Vulnerability Categories

### Critical
- Remote code execution
- SQL injection
- Authentication bypass
- Privilege escalation

### High
- Cross-site scripting (XSS)
- Sensitive data exposure
- Broken access control

### Medium
- Cross-site request forgery (CSRF)
- Information disclosure
- Improper error handling

### Low
- Lack of logging
- Missing security headers
- Weak encryption

## Security Best Practices

### For Developers

1. **Never commit sensitive data**
   - API keys, passwords, tokens
   - Use .gitignore for environment files

2. **Validate all inputs**
   - Use Pydantic schemas
   - Sanitize user inputs

3. **Use parameterized queries**
   - SQLAlchemy ORM handles this
   - Never concatenate SQL strings

4. **Keep dependencies updated**
   ```bash
   pip list --outdated
   npm outdated
   ```

5. **Run security scans**
   ```bash
   # Python
   pip install safety
   safety check
   
   # Node.js
   npm audit
   ```

### For Operators

1. **Regular updates**
   - Keep OS patched
   - Update Docker images
   - Update dependencies

2. **Network segmentation**
   - Isolate scanning network
   - Use firewalls
   - Restrict outbound connections

3. **Monitoring and logging**
   - Log all access attempts
   - Monitor for suspicious activity
   - Set up alerts

4. **Backup regularly**
   - Database backups
   - Configuration backups
   - Test restore procedures

5. **Principle of least privilege**
   - Run services with minimal permissions
   - Use separate accounts
   - Avoid root/administrator

## Compliance

For compliance with security standards:

### OWASP Top 10

VulnHawk should address:
1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable Components
7. Authentication Failures
8. Software and Data Integrity Failures
9. Security Logging Failures
10. Server-Side Request Forgery

### CVE Scanning

VulnHawk scans for vulnerabilities but should also be scanned:
```bash
# Scan Docker images
docker scan vulnhawk-backend:latest
docker scan vulnhawk-frontend:latest

# Scan Python dependencies
pip install pip-audit
pip-audit

# Scan Node dependencies
npm audit
```

## Security Updates

Security updates will be:
- Released as soon as possible
- Announced via GitHub Security Advisories
- Documented in CHANGELOG.md
- Tagged with security labels

## Disclosure Policy

We follow responsible disclosure:
1. Security researcher reports vulnerability privately
2. We confirm and develop a fix
3. We release a patch
4. Public disclosure after 90 days or patch release

## Hall of Fame

We recognize security researchers who help improve VulnHawk:
- (List of contributors who reported security issues)

## Resources

- [OWASP Top 10](https://owasp.org/Top10/)
- [CVE Database](https://cve.mitre.org/)
- [National Vulnerability Database](https://nvd.nist.gov/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

## Contact

For security concerns:
- **Email**: security@vulnhawk-project.com
- **PGP Key**: [Link to PGP key if available]
- **GitHub**: Create a security advisory

---

Thank you for helping keep VulnHawk and its users safe! 🔒
