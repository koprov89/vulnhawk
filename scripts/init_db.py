#!/usr/bin/env python3
"""Database initialization script for VulnHawk"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import engine, Base
from app.models import Scan, Host, Port, Vulnerability


def init_database():
    """Initialize the database with tables"""
    print("Initializing VulnHawk database...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Print table names
        print("\nCreated tables:")
        for table in Base.metadata.sorted_tables:
            print(f"  - {table.name}")
        
        print("\n🎉 Database initialization complete!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    init_database()
