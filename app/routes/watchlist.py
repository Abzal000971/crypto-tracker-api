from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User, CryptoCurrency, UserWatchlist
from ..schemas import WatchlistItem, WatchlistCreate
from .user import get_current_user

router = APIRouter(prefix="/watchlist", tags=["watchlist"])

@router.get("/", response_model=List[WatchlistItem])
def get_watchlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    watchlist = db.query(UserWatchlist).filter(UserWatchlist.user_id == current_user.id).all()
    return watchlist

@router.post("/", response_model=WatchlistItem)
def add_to_watchlist(
    item: WatchlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    crypto = db.query(CryptoCurrency).filter(CryptoCurrency.symbol == item.symbol.upper()).first()
    if not crypto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cryptocurrency not found"
        )
    
    existing = db.query(UserWatchlist).filter(
        UserWatchlist.user_id == current_user.id,
        UserWatchlist.crypto_id == crypto.id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cryptocurrency already in watchlist"
        )
    
    watchlist_item = UserWatchlist(user_id=current_user.id, crypto_id=crypto.id)
    db.add(watchlist_item)
    db.commit()
    db.refresh(watchlist_item)
    return watchlist_item

@router.delete("/{symbol}")
def remove_from_watchlist(
    symbol: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    crypto = db.query(CryptoCurrency).filter(CryptoCurrency.symbol == symbol.upper()).first()
    if not crypto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cryptocurrency not found"
        )
    
    watchlist_item = db.query(UserWatchlist).filter(
        UserWatchlist.user_id == current_user.id,
        UserWatchlist.crypto_id == crypto.id
    ).first()
    
    if not watchlist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cryptocurrency not in watchlist"
        )
    
    db.delete(watchlist_item)
    db.commit()
    return {"message": "Removed from watchlist"} 