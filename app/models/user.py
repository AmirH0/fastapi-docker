from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashpassword = Column(String, nullable=True)
    display_name = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False, nullable=False)
    createdat = Column(DateTime(timezone=True), server_default=func.now())
    
    posts = relationship("Post", back_populates="author")
    comment = relationship("Comment" , back_populates="author")