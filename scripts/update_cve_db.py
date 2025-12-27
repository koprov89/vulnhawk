#!/usr/bin/env python3
"""CVE database update script for VulnHawk"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.scanner.vuln_detector import CVE_DATABASE


def update_cve_database():
    """Update the CVE database with latest vulnerabilities"""
    print("VulnHawk CVE Database Update")
    print("=" * 50)
    
    # Count current CVEs
    total_cves = sum(len(cves) for cves in CVE_DATABASE.values())
    
    print(f"\nCurrent CVE Database Statistics:")
    print(f"  Total Services: {len(CVE_DATABASE)}")
    print(f"  Total CVEs: {total_cves}")
    
    print("\nServices covered:")
    for service, cves in CVE_DATABASE.items():
        print(f"  - {service}: {len(cves)} CVE(s)")
        for cve in cves:
            print(f"    • {cve['cve']} (CVSS: {cve['cvss']}, Severity: {cve['severity']})")
    
    # In production, this would fetch from NVD or other CVE databases
    print("\n" + "=" * 50)
    print("ℹ️  Note: This is a simplified MVP version.")
    print("ℹ️  In production, this would fetch from NVD API or other CVE feeds.")
    print("ℹ️  For now, the CVE database is hardcoded in vuln_detector.py")
    
    # Save database info to JSON
    output_file = "cve_database_info.json"
    database_info = {
        "last_updated": datetime.utcnow().isoformat(),
        "total_services": len(CVE_DATABASE),
        "total_cves": total_cves,
        "services": {
            service: {
                "count": len(cves),
                "cves": [cve['cve'] for cve in cves]
            }
            for service, cves in CVE_DATABASE.items()
        }
    }
    
    with open(output_file, 'w') as f:
        json.dump(database_info, f, indent=2)
    
    print(f"\n✅ CVE database information exported to {output_file}")


if __name__ == "__main__":
    update_cve_database()
