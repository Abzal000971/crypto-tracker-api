from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import CryptoCurrency
from ..schemas import CryptoCurrency as CryptoSchema
from .user import get_current_user
from ..models import User

router = APIRouter(prefix="/cryptos", tags=["crypto"])

@router.get("/", response_model=List[CryptoSchema])
def get_cryptocurrencies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cryptocurrencies = db.query(CryptoCurrency).offset(skip).limit(limit).all()
    return cryptocurrencies

@router.get("/{symbol}", response_model=CryptoSchema)
def get_cryptocurrency(
    symbol: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cryptocurrency = db.query(CryptoCurrency).filter(CryptoCurrency.symbol == symbol.upper()).first()
    if cryptocurrency is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cryptocurrency not found"
        )
    return cryptocurrency 