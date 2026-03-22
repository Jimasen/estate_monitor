# app/main.py

import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.routes import home, utility

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware  

from slowapi.middleware import SlowAPIMiddleware
from app.core.rate_limit import limiter

# Load environment variables
load_dotenv()

# App settings
from app.core.config import settings

# Database & Scheduler
from app.database.init_db import init_db
from app.services.cron_jobs import start_scheduler

# Notifications
from app.utils.notifications import send_whatsapp, send_sms  

# Middleware
from app.middleware.tenant_middleware import TenantMiddleware

# Routers
from app.api.auth.routes import router as auth_api_router
from app.api.auth.register_routes import router as auth_web_router       
from app.api.dashboard.routes import router as dashboard_router
from app.api.properties.routes import router as properties_router        
from app.api.tenant.routes import router as tenant_router
from app.api.owner.routes import router as owner_router
from app.api.payments.routes import router as payments_router
from app.api.profile.routes import router as profile_router
from app.api.admin import user_routes
from app.api.admin.dashboard_routes import router as admin_router        
from app.api.admin.admin_analytics_router import router as analytics_router
from app.api.admin.scheduler_routes import router as scheduler_admin_router
from app.api.marketplace_routes import router as marketplace_router      
from app.api.investment_pool_routes import router as investment_pool_router
from app.api.websocket_routes import router as websocket_router
from app.api.public_files import router as public_files_router
from app.api.pages import router as pages_router
from app.api.home import router as home_router
from app.api.public.homepage_routes import router as homepage_router     
from app.api.public.homepage_builder_routes import router as homepage_builder_router
from app.api.billing.webhook_routes import router as webhook_router  # <<< Added

# Models & Event Handlers
import app.models
import app.core.event_handlers

# ----------------------------------------
# FastAPI App
# ----------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    description="Multi-tenant SaaS for property, estate, and business management",
    version="1.0.0",
)

# ----------------------------------------
# Logging
# ----------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",       
)

# ----------------------------------------
# Middleware
# ----------------------------------------

# SessionMiddleware must come first for request.session
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

# Tenant Middleware
app.add_middleware(TenantMiddleware)

# Rate limiting
app.add_middleware(SlowAPIMiddleware)
app.state.limiter = limiter

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------
# Static Files
# ----------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")   

# ----------------------------------------
# Custom Middleware: App Identity
# ----------------------------------------
@app.middleware("http")
async def add_app_identity(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = settings.APP_NAME
    response.headers["X-SaaS-Type"] = "Multi-Tenant"
    return response

# ----------------------------------------
# Startup Event
# ----------------------------------------
@app.on_event("startup")
async def startup_event():
    logging.info("Initializing database...")
    init_db()

    logging.info("Starting unified scheduler...")
    start_scheduler()

    logging.info("Application startup complete.")

    # Optional notifications
    owner_phone = getattr(settings, "OWNER_PHONE_NUMBER", None)

    if owner_phone:
        message = f"{settings.APP_NAME} backend started successfully!"

        if getattr(settings, "WHATSAPP_ENABLED", False):
            try:
                await send_whatsapp(owner_phone, message)
            except Exception as e:
                logging.error(f"WhatsApp failed: {e}")

        if getattr(settings, "SMS_ENABLED", False):
            try:
                await send_sms(owner_phone, message)
            except Exception as e:
                logging.error(f"SMS failed: {e}")

# ----------------------------------------
# Include Routers
# ----------------------------------------

# Auth
app.include_router(auth_api_router)
app.include_router(auth_web_router)

# Core SaaS APIs
app.include_router(dashboard_router)
app.include_router(properties_router)
app.include_router(tenant_router)
app.include_router(owner_router)
app.include_router(payments_router)
app.include_router(profile_router)
app.include_router(user_routes.router)
app.include_router(utility.router)

# Admin
app.include_router(admin_router)
app.include_router(analytics_router)
app.include_router(scheduler_admin_router)
app.include_router(homepage_builder_router)

# Investments & Marketplace
app.include_router(investment_pool_router)
app.include_router(marketplace_router)

# CMS / Website
app.include_router(pages_router, prefix="/api")

# Public files
app.include_router(public_files_router)
app.include_router(homepage_router)

# Webhooks
app.include_router(webhook_router)

# WebSocket (always last)
app.include_router(websocket_router)

# ----------------------------------------
# Health Check
# ----------------------------------------
@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "status": "running",
        "mode": "Global SaaS (UTC Scheduler)",
    }
