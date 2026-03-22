# app/services/status_service.py
from datetime import date
from app.models.user import User
from app.models.payment import RentPayment

def _classify(days_left: int, paid: bool = False):
    if paid:
        return "paid"
    if days_left < 0:
        return "overdue"
    if days_left <= 5:
        return "ready"
    return "paid"

def subscription_status(user: User):
    # ✅ Safe default if subscription_end missing
    subscription_end = getattr(user, "subscription_end", None)
    if not subscription_end:
        return {
            "status": "no_activity",
            "color": "grey",
            "blink": "none",
            "progress": 0.0
        }

    today = date.today()
    days_left = (subscription_end - today).days
    total_days = 30

    status = _classify(days_left)

    color_map = {
        "paid": "green",
        "ready": "yellow",
        "overdue": "red"
    }

    return {
        "status": status,
        "color": color_map.get(status, "grey"),
        "blink": "blink" if status in ["overdue", "ready"] else "none",  
        "progress": max(0.0, min(1.0, days_left / total_days))
    }

def rent_status(rent: RentPayment):
    if not rent:
        return {
            "status": "no_activity",
            "color": "grey",
            "blink": "none",
            "progress": 0.0
        }

    today = date.today()
    days_left = (rent.due_date - today).days
    total_days = 30

    status = _classify(days_left, paid=rent.paid)

    color_map = {
        "paid": "green",
        "ready": "yellow",
        "overdue": "red"
    }

    return {
        "status": status,
        "color": color_map.get(status, "grey"),
        "blink": "blink" if status in ["overdue", "ready"] else "none",  
        "progress": 1.0 if rent.paid else max(0.0, min(1.0, days_left / total_days))
    }
