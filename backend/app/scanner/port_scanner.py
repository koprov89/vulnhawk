"""Port scanner using nmap"""
import nmap
from typing import Dict, List


class PortScanner:
    """Port scanner using python-nmap wrapper"""
    
    def __init__(self):
        self.nm = nmap.PortScanner()
    
    async def scan(self, target: str, scan_type: str = "quick") -> Dict:
        """
        Scan target for open ports and services
        
        Args:
            target: IP address or hostname to scan
            scan_type: Type of scan (quick or full)
            
        Returns:
            Dictionary with scan results
        """
        arguments = "-sV -sC" if scan_type == "full" else "-sV --top-ports 100"
        
        try:
            self.nm.scan(hosts=target, arguments=arguments)
            results = []
            
            for host in self.nm.all_hosts():
                host_data = {
                    "ip": host,
                    "hostname": self.nm[host].hostname(),
                    "state": self.nm[host].state(),
                    "ports": []
                }
                
                for proto in self.nm[host].all_protocols():
                    ports = self.nm[host][proto].keys()
                    for port in ports:
                        port_info = self.nm[host][proto][port]
                        host_data["ports"].append({
                            "port": port,
                            "protocol": proto,
                            "state": port_info.get("state", "unknown"),
                            "service": port_info.get("name", "unknown"),
                            "version": port_info.get("version", ""),
                            "product": port_info.get("product", "")
                        })
                
                results.append(host_data)
            
            return {"status": "success", "hosts": results}
        except Exception as e:
            return {"status": "error", "message": str(e)}
