"""Report generator for vulnerability scans"""
from typing import Dict, List
from datetime import datetime


class ReportGenerator:
    """Generate reports from scan results"""
    
    def generate_text_report(self, scan_data: Dict) -> str:
        """
        Generate a text-based report
        
        Args:
            scan_data: Scan data with hosts and vulnerabilities
            
        Returns:
            Formatted text report
        """
        report = []
        report.append("=" * 80)
        report.append("VulnHawk Vulnerability Scan Report")
        report.append("=" * 80)
        report.append(f"Target: {scan_data.get('target', 'N/A')}")
        report.append(f"Scan Type: {scan_data.get('scan_type', 'N/A')}")
        report.append(f"Status: {scan_data.get('status', 'N/A')}")
        report.append(f"Created: {scan_data.get('created_at', 'N/A')}")
        report.append(f"Completed: {scan_data.get('completed_at', 'N/A')}")
        report.append("=" * 80)
        report.append("")
        
        hosts = scan_data.get('hosts', [])
        if not hosts:
            report.append("No hosts discovered.")
            return "\n".join(report)
        
        for host in hosts:
            report.append(f"Host: {host.get('ip_address', 'N/A')}")
            if host.get('hostname'):
                report.append(f"  Hostname: {host['hostname']}")
            
            ports = host.get('ports', [])
            if ports:
                report.append(f"  Open Ports: {len(ports)}")
                for port in ports:
                    report.append(f"    Port {port['port_number']}/{port['protocol']}: {port.get('service', 'unknown')}")
                    
                    vulns = port.get('vulnerabilities', [])
                    if vulns:
                        for vuln in vulns:
                            report.append(f"      [!] {vuln['cve_id']} - {vuln['severity'].upper()} (CVSS: {vuln['cvss_score']})")
                            report.append(f"          {vuln.get('description', 'No description')}")
            report.append("")
        
        report.append("=" * 80)
        report.append("End of Report")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def generate_json_report(self, scan_data: Dict) -> Dict:
        """
        Generate a JSON-formatted report
        
        Args:
            scan_data: Scan data
            
        Returns:
            JSON-formatted report
        """
        return {
            "report_generated_at": datetime.utcnow().isoformat(),
            "scan": scan_data,
            "summary": self._generate_summary(scan_data)
        }
    
    def _generate_summary(self, scan_data: Dict) -> Dict:
        """
        Generate summary statistics
        
        Args:
            scan_data: Scan data
            
        Returns:
            Summary statistics
        """
        hosts = scan_data.get('hosts', [])
        total_hosts = len(hosts)
        total_ports = sum(len(host.get('ports', [])) for host in hosts)
        
        severity_counts = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        for host in hosts:
            for port in host.get('ports', []):
                for vuln in port.get('vulnerabilities', []):
                    severity = vuln.get('severity', 'low').lower()
                    if severity in severity_counts:
                        severity_counts[severity] += 1
        
        total_vulnerabilities = sum(severity_counts.values())
        
        return {
            "total_hosts": total_hosts,
            "total_ports": total_ports,
            "total_vulnerabilities": total_vulnerabilities,
            "critical_vulnerabilities": severity_counts["critical"],
            "high_vulnerabilities": severity_counts["high"],
            "medium_vulnerabilities": severity_counts["medium"],
            "low_vulnerabilities": severity_counts["low"]
        }
