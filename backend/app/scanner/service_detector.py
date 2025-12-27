"""Service detection and identification"""
from typing import Dict, Optional


class ServiceDetector:
    """Service detector for identifying services on open ports"""
    
    def detect_service(self, port: int, banner: str = "") -> Dict[str, str]:
        """
        Detect service running on a port
        
        Args:
            port: Port number
            banner: Service banner (if available)
            
        Returns:
            Dictionary with service information
        """
        # Common port mappings
        common_ports = {
            21: "ftp",
            22: "ssh",
            23: "telnet",
            25: "smtp",
            53: "dns",
            80: "http",
            110: "pop3",
            143: "imap",
            443: "https",
            445: "smb",
            3306: "mysql",
            3389: "rdp",
            5432: "postgresql",
            6379: "redis",
            8080: "http-proxy",
            27017: "mongodb"
        }
        
        service = common_ports.get(port, "unknown")
        
        return {
            "service": service,
            "port": port,
            "banner": banner
        }
    
    def get_service_info(self, service: str, version: str = "") -> Optional[Dict]:
        """
        Get detailed information about a service
        
        Args:
            service: Service name
            version: Service version
            
        Returns:
            Service information dictionary
        """
        return {
            "name": service,
            "version": version,
            "description": f"{service} service"
        }
