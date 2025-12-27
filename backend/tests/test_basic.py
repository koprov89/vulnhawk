"""Basic tests for VulnHawk backend"""
import pytest
from app import main
from app.scanner.vuln_detector import VulnerabilityDetector
from app.scanner.risk_calculator import RiskCalculator


def test_app_creation():
    """Test that the FastAPI app is created successfully"""
    assert main.app is not None
    assert main.app.title == "VulnHawk API"
    assert main.app.version == "0.1.0"


def test_vulnerability_detector():
    """Test vulnerability detection"""
    detector = VulnerabilityDetector()
    
    # Test SSH vulnerability detection
    vulns = detector.detect_vulnerabilities("ssh", "7.2")
    assert len(vulns) > 0
    assert any(v["cve"] == "CVE-2016-10012" for v in vulns)
    
    # Test no vulnerabilities for newer version
    vulns = detector.detect_vulnerabilities("ssh", "9.0")
    assert len(vulns) == 0


def test_risk_calculator():
    """Test risk calculation"""
    calculator = RiskCalculator()
    
    # Test with critical vulnerabilities
    vulns = [
        {"severity": "critical", "cvss_score": 10.0},
        {"severity": "high", "cvss_score": 7.5}
    ]
    risk = calculator.calculate_host_risk(vulns)
    
    assert risk["risk_level"] == "critical"
    assert risk["critical_count"] == 1
    assert risk["high_count"] == 1
    assert risk["total_vulnerabilities"] == 2
    
    # Test with no vulnerabilities
    risk = calculator.calculate_host_risk([])
    assert risk["risk_level"] == "low"
    assert risk["risk_score"] == 0.0


def test_cve_database_coverage():
    """Test CVE database has expected services"""
    from app.scanner.vuln_detector import CVE_DATABASE
    
    expected_services = ["openssh", "apache", "nginx", "mysql", "vsftpd"]
    for service in expected_services:
        assert service in CVE_DATABASE
        assert len(CVE_DATABASE[service]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
