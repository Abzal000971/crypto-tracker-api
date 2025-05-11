from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .crypto_updater import update_crypto_prices

def init_scheduler():
    """Initialize the background scheduler for updating crypto prices"""
    scheduler = BackgroundScheduler()
    
    def update_prices_job():
        db = SessionLocal()
        try:
            update_crypto_prices(db)
        finally:
            db.close()
    
    # Schedule the job to run every 5 minutes
    scheduler.add_job(
        update_prices_job,
        trigger=IntervalTrigger(minutes=5),
        id='update_crypto_prices',
        name='Update cryptocurrency prices every 5 minutes',
        replace_existing=True
    )
    
    scheduler.start()
    return scheduler 