# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.db.base import Base

from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"

    # primary key
    id = Column(Integer, primary_key=True, index=True)

    # authentication fields
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # user role system
    role = Column(String, default="user")  # user | admin

    # account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()   
    )

    documents = relationship("Document", backref="owner")