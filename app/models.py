from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    watchlist = relationship("UserWatchlist", back_populates="user")

class CryptoCurrency(Base):
    __tablename__ = "cryptocurrencies"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    current_price = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    watchlist = relationship("UserWatchlist", back_populates="crypto")

class UserWatchlist(Base):
    __tablename__ = "user_watchlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    crypto_id = Column(Integer, ForeignKey("cryptocurrencies.id"))
    
    user = relationship("User", back_populates="watchlist")
    crypto = relationship("CryptoCurrency", back_populates="watchlist") 