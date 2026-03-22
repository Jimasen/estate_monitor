# app/database/async_session.py

from contextlib import asynccontextmanager
from app.database.session import SessionLocal
import asyncio
import logging

logger = logging.getLogger("db")

@asynccontextmanager
async def async_db_session():
    """
    Async-safe context manager for SQLAlchemy SessionLocal.
    Runs blocking session operations in a thread to avoid blocking the event loop.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        raise
    finally:
        # Close session in a thread to prevent blocking
        await asyncio.to_thread(db.close)
