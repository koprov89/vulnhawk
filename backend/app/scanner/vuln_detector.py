"""Vulnerability detection using CVE database"""
from typing import List, Dict


# Hardcoded CVE database for MVP
CVE_DATABASE = {
    "openssh": [
        {
            "version_range": "< 7.4",
            "cve": "CVE-2016-10012",
            "cvss": 7.8,
            "severity": "high",
            "description": "Shared memory manager vulnerability in OpenSSH allowing unauthorized access",
            "remediation": "Upgrade to OpenSSH 7.4 or later"
        },
    ],
    "apache": [
        {
            "version_range": "< 2.4.49",
            "cve": "CVE-2021-41773",
            "cvss": 9.8,
            "severity": "critical",
            "description": "Path traversal and RCE vulnerability in Apache HTTP Server",
            "remediation": "Upgrade to Apache 2.4.51 or later"
        },
    ],
    "nginx": [
        {
            "version_range": "< 1.20.1",
            "cve": "CVE-2021-23017",
            "cvss": 9.8,
            "severity": "critical",
            "description": "DNS resolver off-by-one heap write vulnerability",
            "remediation": "Upgrade to nginx 1.20.1 or later"
        },
    ],
    "mysql": [
        {
            "version_range": "< 5.7.17",
            "cve": "CVE-2016-6662",
            "cvss": 9.0,
            "severity": "critical",
            "description": "Remote root code execution vulnerability in MySQL",
            "remediation": "Upgrade to MySQL 5.7.17 or later"
        },
    ],
    "vsftpd": [
        {
            "version_range": "2.3.4",
            "cve": "CVE-2011-2523",
            "cvss": 10.0,
            "severity": "critical",
            "description": "Backdoor command execution in vsftpd",
            "remediation": "Upgrade to vsftpd 3.0.0 or later"
        },
    ],
    "ssh": [
        {
            "version_range": "< 7.4",
            "cve": "CVE-2016-10012",
            "cvss": 7.8,
            "severity": "high",
            "description": "Shared memory manager vulnerability allowing unauthorized access",
            "remediation": "Upgrade to OpenSSH 7.4 or later"
        },
    ],
    "ftp": [
        {
            "version_range": "< 3.0.0",
            "cve": "CVE-2011-2523",
            "cvss": 10.0,
            "severity": "critical",
            "description": "Potential backdoor in older FTP server versions",
            "remediation": "Upgrade to latest stable FTP server version"
        },
    ]
}


class VulnerabilityDetector:
    """Vulnerability detector for matching services against CVE database"""
    
    def detect_vulnerabilities(self, service: str, version: str) -> List[Dict]:
        """
        Match service and version against CVE database
        
        Args:
            service: Service name
            version: Service version
            
        Returns:
            List of matching vulnerabilities
        """
        service_lower = service.lower()
        vulnerabilities = []
        
        for service_name, cves in CVE_DATABASE.items():
            if service_name in service_lower:
                for cve in cves:
                    # Simple version matching for MVP
                    if self._version_matches(version, cve["version_range"]):
                        vulnerabilities.append(cve)
        
        return vulnerabilities
    
    def _version_matches(self, version: str, version_range: str) -> bool:
        """
        Simple version matching logic
        
        Args:
            version: Version string to check
            version_range: Version range expression
            
        Returns:
            True if version matches the range
        """
        # This is simplified for MVP - in production use proper semver comparison
        if not version:
            return False
        
        if version_range.startswith("<"):
            target = version_range.replace("<", "").strip()
            return version < target
        elif version_range == version:
            return True
        
        return False
    
    def get_vulnerability_by_cve(self, cve_id: str) -> Dict:
        """
        Get vulnerability details by CVE ID
        
        Args:
            cve_id: CVE identifier
            
        Returns:
            Vulnerability details or empty dict
        """
        for service_cves in CVE_DATABASE.values():
            for cve in service_cves:
                if cve["cve"] == cve_id:
                    return cve
        return {}
