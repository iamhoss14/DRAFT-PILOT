from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    generations = relationship("Generation", back_populates="owner")
    usage_records = relationship("Usage", back_populates="owner")

class Generation(Base):
    __tablename__ = "generations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content_type = Column(String)
    prompt = Column(Text)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship back to User
    owner = relationship("User", back_populates="generations")

class Usage(Base):
    __tablename__ = "usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    requests = Column(Integer, default=0)
    date = Column(Date)

    # Relationship back to User
    owner = relationship("User", back_populates="usage_records")