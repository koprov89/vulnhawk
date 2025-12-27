"""Risk calculation and scoring"""
from typing import List, Dict


class RiskCalculator:
    """Calculate risk scores for hosts and scans"""
    
    def calculate_host_risk(self, vulnerabilities: List[Dict]) -> Dict:
        """
        Calculate overall risk score for a host
        
        Args:
            vulnerabilities: List of vulnerabilities
            
        Returns:
            Risk assessment dictionary
        """
        if not vulnerabilities:
            return {
                "risk_score": 0.0,
                "risk_level": "low",
                "critical_count": 0,
                "high_count": 0,
                "medium_count": 0,
                "low_count": 0
            }
        
        severity_counts = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        total_cvss = 0.0
        
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "low").lower()
            if severity in severity_counts:
                severity_counts[severity] += 1
            total_cvss += vuln.get("cvss_score", 0.0)
        
        avg_cvss = total_cvss / len(vulnerabilities) if vulnerabilities else 0.0
        
        # Calculate weighted risk score
        risk_score = (
            severity_counts["critical"] * 10.0 +
            severity_counts["high"] * 7.5 +
            severity_counts["medium"] * 5.0 +
            severity_counts["low"] * 2.5
        )
        
        # Determine risk level
        if risk_score >= 50 or severity_counts["critical"] > 0:
            risk_level = "critical"
        elif risk_score >= 30 or severity_counts["high"] > 0:
            risk_level = "high"
        elif risk_score >= 15 or severity_counts["medium"] > 0:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "average_cvss": round(avg_cvss, 2),
            "critical_count": severity_counts["critical"],
            "high_count": severity_counts["high"],
            "medium_count": severity_counts["medium"],
            "low_count": severity_counts["low"],
            "total_vulnerabilities": len(vulnerabilities)
        }
    
    def calculate_scan_risk(self, hosts: List[Dict]) -> Dict:
        """
        Calculate overall risk for entire scan
        
        Args:
            hosts: List of host data with vulnerabilities
            
        Returns:
            Scan risk assessment
        """
        all_vulnerabilities = []
        for host in hosts:
            all_vulnerabilities.extend(host.get("vulnerabilities", []))
        
        return self.calculate_host_risk(all_vulnerabilities)
