from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, timezone
from sqlalchemy import delete
from .config import database, urls

async def clean_old_urls():
    two_months_ago = datetime.now(timezone.utc) - timedelta(days=60)
    query = delete(urls).where(urls.c.created_at < two_months_ago)
    await database.execute(query)
    print("Old URLs cleaned successfully.")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(clean_old_urls, "cron", hour=0)
    scheduler.start()
