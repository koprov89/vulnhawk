"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ScanCreate(BaseModel):
    """Schema for creating a new scan"""
    target: str
    scan_type: str = "quick"


class ScanResponse(BaseModel):
    """Schema for scan response"""
    id: int
    target: str
    scan_type: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class VulnerabilityBase(BaseModel):
    """Base vulnerability schema"""
    cve_id: str
    severity: str
    cvss_score: float
    description: Optional[str] = None
    remediation: Optional[str] = None


class VulnerabilityResponse(VulnerabilityBase):
    """Schema for vulnerability response"""
    id: int
    port_id: int
    
    class Config:
        from_attributes = True


class PortBase(BaseModel):
    """Base port schema"""
    port_number: int
    protocol: str
    service: Optional[str] = None
    version: Optional[str] = None


class PortResponse(PortBase):
    """Schema for port response"""
    id: int
    host_id: int
    vulnerabilities: List[VulnerabilityResponse] = []
    
    class Config:
        from_attributes = True


class HostBase(BaseModel):
    """Base host schema"""
    ip_address: str
    hostname: Optional[str] = None
    os_info: Optional[str] = None


class HostResponse(HostBase):
    """Schema for host response"""
    id: int
    scan_id: int
    ports: List[PortResponse] = []
    
    class Config:
        from_attributes = True


class ScanDetail(ScanResponse):
    """Schema for detailed scan response"""
    hosts: List[HostResponse] = []
    
    class Config:
        from_attributes = True
