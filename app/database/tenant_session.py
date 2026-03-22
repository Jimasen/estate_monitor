# app/database/tenant_session.py

from fastapi import Request


def get_tenant_session(request: Request):

    db = request.state.tenant_db

    try:
        yield db
    finally:
        db.close()
