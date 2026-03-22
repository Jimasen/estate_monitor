import secrets
from fastapi import Request, HTTPException

def generate_csrf(request: Request):
    token = secrets.token_urlsafe(32)
    request.session["csrf"] = token
    return token

def verify_csrf(request: Request, token: str):
    if not token or token != request.session.get("csrf"):
        raise HTTPException(status_code=403, detail="CSRF validation failed")
