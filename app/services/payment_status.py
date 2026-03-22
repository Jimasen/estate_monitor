def get_rent_status(tenant):

    if tenant.last_payment:
        return "paid"

    if tenant.rent_due_date < today:
        return "overdue"

    if tenant.rent_due_date - today <= 5:
        return "ready"

    return "no_activity"
