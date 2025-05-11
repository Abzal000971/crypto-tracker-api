from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class CryptoCurrencyBase(BaseModel):
    symbol: str
    name: str

class CryptoCurrencyCreate(CryptoCurrencyBase):
    current_price: float

class CryptoCurrency(CryptoCurrencyBase):
    id: int
    current_price: float
    last_updated: datetime

    class Config:
        from_attributes = True

class WatchlistItem(BaseModel):
    id: int
    crypto: CryptoCurrency

    class Config:
        from_attributes = True

class WatchlistCreate(BaseModel):
    symbol: str 