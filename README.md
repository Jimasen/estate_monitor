# Estate Monitor SaaS

A **FastAPI-based property and business management system** designed to run on **Termux (Android), Windows laptop, or VPS servers**.

Supported databases:

* **MariaDB / MySQL** (Termux)
* **PostgreSQL** (Laptop / VPS)

---

# 1. Project Setup

Navigate to the project directory:

```
cd ~/estate_monitor
```

---

# 2. Virtual Environment Setup

The project uses a Python virtual environment located at:

```
estate_monitor/.venv
```

## Activate Virtual Environment

### Windows (PowerShell / VS Code)

```
.\.venv\Scripts\Activate.ps1
```
### Windows (Command Prompt)

```
.venv\Scripts\activate
```

### Git Bash
e
```source .venv/Scripts/activat

```

### Termux / Linux

```
source .venv/bin/activate
```

After activation you should see:

```
(.venv)
```

Example:

```
(.venv) user@device ~/estate_monitor
```

---

# 3. Install Dependencies

Once the virtual environment is active:

```
pip install -r requirements.txt
```

---

# 4. Start MariaDB (Termux)

Start MariaDB so the database socket becomes available.

```
mariadbd --datadir=/data/data/com.termux/files/usr/var/lib/mysql &
```

Wait **3–5 seconds** for the socket to initialize.

Optional check:

```
ps aux | grep mariadbd
```

Login to database:

```
mariadb -u estate -p
```

---

# 5. Start the FastAPI Application

Navigate to the project folder:

```
cd ~/estate_monitor
```

Activate virtual environment:

```
source .venv/bin/activate
```

Start the API server:

```

```

The API will run at:

```
http://127.0.0.1:8000
```

---

# 6. Optional Helper Script

If you created **startdb.sh**, startup becomes easier.

```
./startdb.sh
cd ~/estate_monitor
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

# 7. Environment Configuration (.env)

Example `.env` file.

```
APP_ENV=production
APP_NAME=Estate Monitor SaaS
APP_HOST=http://YOUR_SERVER_IP
```

---

# 8. Database Configuration

## MySQL (Termux)

```
DATABASE_URL=mysql+pymysql://estate:YourPassword@localhost/estate_monitor?unix_socket=/data/data/com.termux/files/usr/var/run/mysqld.sock
```

## PostgreSQL (Laptop / VPS)

```
DATABASE_URL=postgresql+psycopg2://estate:YourPostgresPassword@localhost/estate_monitor
```

---

# 9. Email Configuration

```
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_email_password
EMAIL_ENABLED=true
```

---

# 10. SMS Configuration

```
SMS_API_KEY=your_sms_api_key
SMS_SENDER=EstateMgmt
SMS_ENABLED=true
```

---

# 11. Security (JWT)

```
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

---

# 12. WhatsApp Integration (Optional)

```
WHATSAPP_PHONE_ID=
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_VERIFY_TOKEN=
WHATSAPP_ENABLED=false
```

---

# 13. Laptop Deployment (PostgreSQL)

Install PostgreSQL driver:

```
pip install psycopg2-binary
```

Create database:

```
createdb estate_monitor
```

Run migrations:

```
PYTHONPATH=. alembic upgrade head
```

Start server:

```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

# 14. VPS Deployment

Recommended VPS providers:

* DigitalOcean
* Hetzner

Minimum requirements:

* Ubuntu 22.04
* 2 GB RAM

Install dependencies:

```
sudo apt update
sudo apt install python3 python3-venv nginx
```

Create virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate
```

Run the application:

```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

# 15. Nginx Reverse Proxy

Example configuration:

`/etc/nginx/sites-enabled/estate`

```
server {
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Restart Nginx:

```
sudo systemctl restart nginx
```

---

# 16. Enable SSL

Install SSL using Certbot.

```
sudo certbot --nginx -d yourdomain.com
```

---

# 17. Database Migration

Run migrations whenever the database schema changes.

```
PYTHONPATH=. alembic upgrade head
```

This migration system works with both **MySQL** and **PostgreSQL**.

---

# 18. Development vs Production

## Termux Development

```
APP_ENV=development
```

## Laptop / VPS Production

```
APP_ENV=production
```

Run migrations:

```
alembic upgrade head
```

Start the application normally with **uvicorn**.

---
#19.Project Goal

Estate Monitor is designed to be a **multi-tenant SaaS platform** for:

* Property management
* Tenant dashboards
* Payment tracking
* SMS notifications
* Email reminders
*WhatsApp integrations

Built for **mobile-first development** using:
*FastAPI
*Flutter
*Termux
*PostgreSQL / MySQL
# Estate Monitor Backend - Database Setup & Migration Guide

This guide explains how to **reset your database** and run Alembic migrations safely.

## 1. Prerequisites

- Python virtual environment (`.venv`) activated
- Alembic installed (`pip install alembic`)
- MySQL / MariaDB server running
- `.env` configured with database credentials

---

## 2. Full Database Reset Workflow

> Use this workflow in **development only**. It will drop all data.

```bash
# Step 1: Drop and recreate database
mysql -u <username> -p
DROP DATABASE estate_monitor;
CREATE DATABASE estate_monitor;
EXIT;

# Step 2: Stamp the DB at the latest Alembic revision (without applying SQL)
alembic stamp head

# Step 3: Run migrations to create all tables
alembic upgrade head# Step 1: Generate a new migration file
alembic revision --autogenerate -m "describe your change"

# Step 2: Apply the migration
alembic upgrade head