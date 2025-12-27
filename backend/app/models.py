"""SQLAlchemy database models"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Scan(Base):
    """Scan model representing a network scan"""
    __tablename__ = "scans"
    
    id = Column(Integer, primary_key=True, index=True)
    target = Column(String, nullable=False)
    scan_type = Column(String, default="quick")
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    hosts = relationship("Host", back_populates="scan", cascade="all, delete-orphan")


class Host(Base):
    """Host model representing a discovered host"""
    __tablename__ = "hosts"
    
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"))
    ip_address = Column(String, nullable=False)
    hostname = Column(String, nullable=True)
    os_info = Column(String, nullable=True)
    
    scan = relationship("Scan", back_populates="hosts")
    ports = relationship("Port", back_populates="host", cascade="all, delete-orphan")


class Port(Base):
    """Port model representing an open port on a host"""
    __tablename__ = "ports"
    
    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("hosts.id"))
    port_number = Column(Integer, nullable=False)
    protocol = Column(String, default="tcp")
    service = Column(String, nullable=True)
    version = Column(String, nullable=True)
    
    host = relationship("Host", back_populates="ports")
    vulnerabilities = relationship("Vulnerability", back_populates="port", cascade="all, delete-orphan")


class Vulnerability(Base):
    """Vulnerability model representing a discovered vulnerability"""
    __tablename__ = "vulnerabilities"
    
    id = Column(Integer, primary_key=True, index=True)
    port_id = Column(Integer, ForeignKey("ports.id"))
    cve_id = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    cvss_score = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    remediation = Column(Text, nullable=True)
    
    port = relationship("Port", back_populates="vulnerabilities")
