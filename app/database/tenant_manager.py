from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


def create_tenant_engine(db_name: str):

    if settings.APP_ENV == "production":
        base = settings.DATABASE_URL_POSTGRES
    else:
        base = settings.DATABASE_URL_MYSQL

    tenant_url = base.replace("estate_monitor", db_name)

    engine = create_engine(tenant_url, pool_pre_ping=True)

    return engine


def get_tenant_session(db_name: str):

    engine = create_tenant_engine(db_name)

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    return SessionLocal()
