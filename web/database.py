from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

# Get database URL from environment variable or use SQLite as fallback
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///useragents.db')

# Fix Render's Postgres URL if needed
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

class AndroidDevice(Base):
    __tablename__ = "android_devices"
    id = Column(Integer, primary_key=True)
    manufacturer = Column(String)
    model = Column(String)
    android_version = Column(String)

class IOSDevice(Base):
    __tablename__ = "ios_devices"
    id = Column(Integer, primary_key=True)
    model = Column(String)
    ios_version = Column(String)

class ChromeVersion(Base):
    __tablename__ = "chrome_versions"
    id = Column(Integer, primary_key=True)
    version = Column(String)
    build = Column(String)

class SafariVersion(Base):
    __tablename__ = "safari_versions"
    id = Column(Integer, primary_key=True)
    version = Column(String)
    build = Column(String)

class GeneratedAgent(Base):
    __tablename__ = "generated_agents"
    id = Column(Integer, primary_key=True)
    user_agent = Column(String, unique=True)
    device_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    """Initialize the database"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
