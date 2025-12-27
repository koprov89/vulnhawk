# Contributing to VulnHawk

First off, thank you for considering contributing to VulnHawk! It's people like you that make VulnHawk such a great tool.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct:
- Be respectful and inclusive
- Welcome newcomers
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps to reproduce the problem**
* **Provide specific examples**
* **Describe the behavior you observed and what you expected**
* **Include screenshots if relevant**
* **Include your environment details** (OS, Python version, Docker version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a detailed description of the proposed enhancement**
* **Explain why this enhancement would be useful**
* **List any similar features in other tools**

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. Ensure the test suite passes
4. Make sure your code lints
5. Update the documentation
6. Issue that pull request!

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### Setting Up Your Development Environment

1. **Fork and clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/vulnhawk.git
cd vulnhawk
```

2. **Set up the backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install pytest pytest-cov flake8 black
```

3. **Set up the frontend:**
```bash
cd frontend
npm install
```

4. **Create environment files:**
```bash
# Backend
cp backend/.env.example backend/.env

# Frontend
cp frontend/.env.example frontend/.env
```

## Development Workflow

### Backend Development

1. **Run the development server:**
```bash
cd backend
uvicorn app.main:app --reload
```

2. **Run tests:**
```bash
pytest tests/ -v --cov=app
```

3. **Lint code:**
```bash
flake8 app/
```

4. **Format code:**
```bash
black app/
```

### Frontend Development

1. **Run the development server:**
```bash
cd frontend
npm start
```

2. **Run tests:**
```bash
npm test
```

3. **Build for production:**
```bash
npm run build
```

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where applicable
- Write docstrings for all functions and classes
- Keep functions small and focused
- Use meaningful variable names

**Example:**
```python
def calculate_risk_score(vulnerabilities: List[Dict]) -> float:
    """
    Calculate overall risk score from vulnerabilities.
    
    Args:
        vulnerabilities: List of vulnerability dictionaries
        
    Returns:
        Calculated risk score as float
    """
    # Implementation
    pass
```

### JavaScript/React (Frontend)

- Use functional components with hooks
- Follow ES6+ standards
- Use meaningful component and variable names
- Keep components small and reusable
- Add PropTypes or TypeScript types

**Example:**
```javascript
function VulnerabilityCard({ vulnerability }) {
  // Component implementation
  return (
    <div className="vulnerability-card">
      {/* JSX */}
    </div>
  );
}
```

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests

**Examples:**
```
Add CVE-2024-1234 to vulnerability database
Fix scan timeout issue (#42)
Update API documentation for new endpoints
Refactor port scanner for better performance
```

## Testing Guidelines

### Backend Tests

- Write unit tests for all business logic
- Write integration tests for API endpoints
- Aim for >80% code coverage
- Use pytest fixtures for common setup

**Example:**
```python
def test_vulnerability_detection():
    detector = VulnerabilityDetector()
    vulns = detector.detect_vulnerabilities("ssh", "7.2")
    assert len(vulns) > 0
    assert vulns[0]["cve"] == "CVE-2016-10012"
```

### Frontend Tests

- Write unit tests for utility functions
- Write component tests using React Testing Library
- Test user interactions

**Example:**
```javascript
test('renders vulnerability card', () => {
  const vuln = { cve_id: 'CVE-2024-1234', severity: 'high' };
  render(<VulnerabilityCard vulnerability={vuln} />);
  expect(screen.getByText('CVE-2024-1234')).toBeInTheDocument();
});
```

## Documentation

- Update README.md if needed
- Update API.md for API changes
- Update ARCHITECTURE.md for architectural changes
- Add inline comments for complex logic
- Update DEPLOYMENT.md for deployment changes

## Project Structure

```
vulnhawk/
├── backend/           # Python FastAPI backend
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── scanner/  # Scanning modules
│   │   └── reports/  # Report generation
│   └── tests/        # Backend tests
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   └── services/
│   └── tests/        # Frontend tests
├── docs/             # Documentation
├── scripts/          # Utility scripts
└── .github/          # GitHub workflows
```

## Adding New Features

### Backend Feature

1. Create models in `models.py` if needed
2. Add schemas in `schemas.py`
3. Implement business logic in appropriate module
4. Add API endpoints in `routes.py`
5. Write tests
6. Update API documentation

### Frontend Feature

1. Create new component in `components/`
2. Add service functions in `services/api.js` if needed
3. Update parent components
4. Add styling
5. Write tests
6. Update UI documentation

## Adding CVE Data

To add new CVE entries to the database:

1. Edit `backend/app/scanner/vuln_detector.py`
2. Add entry to `CVE_DATABASE` dictionary:
```python
"service_name": [
    {
        "version_range": "< x.x.x",
        "cve": "CVE-YYYY-XXXXX",
        "cvss": 7.5,
        "severity": "high",
        "description": "Vulnerability description",
        "remediation": "Update to version x.x.x or later"
    }
]
```
3. Run `python scripts/update_cve_db.py` to validate
4. Submit PR with clear description

## Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by at least one maintainer
3. **Testing** - all tests must pass
4. **Documentation** must be updated
5. **No merge conflicts** with main branch

## Recognition

Contributors will be recognized in:
- GitHub contributors page
- Release notes
- Special thanks in README

## Questions?

Feel free to:
- Open an issue for discussion
- Join our community chat (if available)
- Contact maintainers directly

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

---

Thank you for contributing to VulnHawk! 🦅
