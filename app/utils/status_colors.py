def get_status_color(status):
    return {
        "paid": "green",
        "pending": "yellow",
        "overdue": "red"
    }.get(status, "gray")
