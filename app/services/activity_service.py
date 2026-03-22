# app/services/activity_service.py

import logging
from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog

logger = logging.getLogger("activity_service")


def log_activity(
    db: Session,
    event_type: str,
    description: str,
    company_id: int | None = None,
    user_id: int | None = None,
    metadata: str | None = None,
):
    """
    Store activity events for dashboards and audits.
    """

    try:

        activity = ActivityLog(
            event_type=event_type,
            description=description,
            company_id=company_id,
            user_id=user_id,
            metadata=metadata,
        )

        db.add(activity)
        db.commit()

        logger.info(f"Activity logged: {event_type}")

    except Exception as e:

        db.rollback()
        logger.exception("Activity logging failed: %s", e)
