# app/database/init_db.py

import logging
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.database.session import engine

logger = logging.getLogger(__name__)

def init_db():
    """
    Initialize the database connection.
    Only tests connectivity. Alembic manages table creation/migrations.
    """
    try:
        # Use a context manager for safe connection handling
        with engine.connect() as conn:
            # Test the connection
            conn.execute(text("SELECT 1"))
            conn.commit()  # commit if necessary (some DBs require it)
        logger.info("Database connection successful.")
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {e}")
        raise
