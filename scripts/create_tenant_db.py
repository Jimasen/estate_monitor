import sys
import os

# allow script to see project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine, text
from app.core.config import settings


def create_tenant_database(company_slug: str):

    db_name = f"tenant_{company_slug}"

    engine = create_engine(settings.DATABASE_URL)

    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE {db_name}"))

    print("Tenant database created:", db_name)


if __name__ == "__main__":

    create_tenant_database("demo_company")
