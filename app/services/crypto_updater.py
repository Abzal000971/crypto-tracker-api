import requests
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import CryptoCurrency
from ..core.config import settings

def fetch_crypto_prices():
    """Fetch cryptocurrency prices from CoinGecko API"""
    try:
        response = requests.get(f"{settings.COINGECKO_API_URL}/simple/price", params={
            "ids": "bitcoin,ethereum,ripple,dogecoin",
            "vs_currencies": "usd"
        })
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching crypto prices: {e}")
        return None

def update_crypto_prices(db: Session):
    """Update cryptocurrency prices in the database"""
    prices = fetch_crypto_prices()
    if not prices:
        return
    
    # Map of CoinGecko IDs to our symbols
    crypto_map = {
        "bitcoin": "BTC",
        "ethereum": "ETH",
        "ripple": "XRP",
        "dogecoin": "DOGE"
    }
    
    for coin_id, price_data in prices.items():
        symbol = crypto_map.get(coin_id)
        if not symbol:
            continue
            
        crypto = db.query(CryptoCurrency).filter(CryptoCurrency.symbol == symbol).first()
        if not crypto:
            # Create new cryptocurrency entry
            crypto = CryptoCurrency(
                symbol=symbol,
                name=coin_id.capitalize(),
                current_price=price_data["usd"],
                last_updated=datetime.utcnow()
            )
            db.add(crypto)
        else:
            # Update existing cryptocurrency
            crypto.current_price = price_data["usd"]
            crypto.last_updated = datetime.utcnow()
    
    db.commit() 