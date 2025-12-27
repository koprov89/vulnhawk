"""API routes for VulnHawk"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db
from app.scanner.port_scanner import PortScanner
from app.scanner.vuln_detector import VulnerabilityDetector
from app.scanner.risk_calculator import RiskCalculator
from datetime import datetime

router = APIRouter()


@router.post("/scans", response_model=schemas.ScanResponse)
async def create_scan(scan: schemas.ScanCreate, db: Session = Depends(get_db)):
    """
    Create and execute a new scan
    
    Args:
        scan: Scan creation data
        db: Database session
        
    Returns:
        Created scan object
    """
    # Create scan record
    db_scan = models.Scan(target=scan.target, scan_type=scan.scan_type, status="running")
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    
    # Execute scan
    scanner = PortScanner()
    scan_results = await scanner.scan(scan.target, scan.scan_type)
    
    if scan_results["status"] == "error":
        db_scan.status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail=scan_results["message"])
    
    # Process results
    vuln_detector = VulnerabilityDetector()
    
    for host_data in scan_results["hosts"]:
        db_host = models.Host(
            scan_id=db_scan.id,
            ip_address=host_data["ip"],
            hostname=host_data.get("hostname", "")
        )
        db.add(db_host)
        db.commit()
        db.refresh(db_host)
        
        for port_data in host_data["ports"]:
            if port_data["state"] == "open":
                db_port = models.Port(
                    host_id=db_host.id,
                    port_number=port_data["port"],
                    protocol=port_data["protocol"],
                    service=port_data["service"],
                    version=port_data.get("version", "")
                )
                db.add(db_port)
                db.commit()
                db.refresh(db_port)
                
                # Check for vulnerabilities
                vulns = vuln_detector.detect_vulnerabilities(
                    port_data["service"],
                    port_data.get("version", "")
                )
                
                for vuln in vulns:
                    db_vuln = models.Vulnerability(
                        port_id=db_port.id,
                        cve_id=vuln["cve"],
                        severity=vuln["severity"],
                        cvss_score=vuln["cvss"],
                        description=vuln["description"],
                        remediation=vuln["remediation"]
                    )
                    db.add(db_vuln)
    
    db_scan.status = "completed"
    db_scan.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(db_scan)
    
    return db_scan


@router.get("/scans", response_model=List[schemas.ScanResponse])
def list_scans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all scans
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of scans
    """
    scans = db.query(models.Scan).offset(skip).limit(limit).all()
    return scans


@router.get("/scans/{scan_id}", response_model=schemas.ScanDetail)
def get_scan(scan_id: int, db: Session = Depends(get_db)):
    """
    Get scan details
    
    Args:
        scan_id: Scan ID
        db: Database session
        
    Returns:
        Scan details with hosts and vulnerabilities
    """
    scan = db.query(models.Scan).filter(models.Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan


@router.get("/scans/{scan_id}/vulnerabilities")
def get_vulnerabilities(scan_id: int, db: Session = Depends(get_db)):
    """
    Get all vulnerabilities for a scan
    
    Args:
        scan_id: Scan ID
        db: Database session
        
    Returns:
        List of vulnerabilities with host and port information
    """
    scan = db.query(models.Scan).filter(models.Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    vulnerabilities = []
    for host in scan.hosts:
        for port in host.ports:
            for vuln in port.vulnerabilities:
                vulnerabilities.append({
                    "id": vuln.id,
                    "host": host.ip_address,
                    "port": port.port_number,
                    "service": port.service,
                    "cve_id": vuln.cve_id,
                    "severity": vuln.severity,
                    "cvss_score": vuln.cvss_score,
                    "description": vuln.description,
                    "remediation": vuln.remediation
                })
    
    return {"vulnerabilities": vulnerabilities, "total": len(vulnerabilities)}


@router.delete("/scans/{scan_id}")
def delete_scan(scan_id: int, db: Session = Depends(get_db)):
    """
    Delete a scan
    
    Args:
        scan_id: Scan ID
        db: Database session
        
    Returns:
        Success message
    """
    scan = db.query(models.Scan).filter(models.Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    db.delete(scan)
    db.commit()
    
    return {"message": "Scan deleted successfully"}


@router.get("/scans/{scan_id}/risk")
def get_scan_risk(scan_id: int, db: Session = Depends(get_db)):
    """
    Calculate risk assessment for a scan
    
    Args:
        scan_id: Scan ID
        db: Database session
        
    Returns:
        Risk assessment data
    """
    scan = db.query(models.Scan).filter(models.Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    calculator = RiskCalculator()
    
    # Collect all vulnerabilities
    all_vulns = []
    for host in scan.hosts:
        for port in host.ports:
            for vuln in port.vulnerabilities:
                all_vulns.append({
                    "severity": vuln.severity,
                    "cvss_score": vuln.cvss_score
                })
    
    risk_assessment = calculator.calculate_host_risk(all_vulns)
    
    return risk_assessment
