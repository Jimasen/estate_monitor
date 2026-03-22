#!/data/data/com.termux/files/usr/bin/bash
# ========================================
# FastAPI + MariaDB Dev Setup for Termux
# ========================================

# 1️⃣ Start MariaDB safely
echo "Starting MariaDB..."
mysqld_safe --datadir=$PREFIX/var/lib/mysql --skip-grant-tables &
sleep 5  # wait for DB to start

# 2️⃣ Ensure Base and Session in SQLAlchemy are set
cat > app/database/base.py <<'EOF'
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# -------------------------
# Declarative base for ORM
# -------------------------
Base = declarative_base()

# -------------------------
# SQLAlchemy engine
# -------------------------
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=True
)

# -------------------------
# Session factory
# -------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
EOF

echo "✅ Database base.py is ready"

# 3️⃣ Start FastAPI backend
echo "Starting FastAPI backend..."
uvicorn app.main:app --host 127.0.0.1 --port 8000 &
sleep 2

echo "✅ FastAPI backend running at http://127.0.0.1:8000"
echo "Use this URL in Flutter for dev"
