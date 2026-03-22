#!/data/data/com.termux/files/usr/bin/bash

# Phone's local IP
PHONE_IP=$(ip addr show wlan0 | grep "inet " | awk '{print $2}' | cut -d/ -f1)

# CORS: allow PC (localhost:3000) and phone IP for web access
export CORS_ORIGINS="http://localhost:3000,http://$PHONE_IP:3000"

# Kill old uvicorn if running
pkill -f uvicorn

# Start backend
echo "🚀 Starting backend on 0.0.0.0:8000 (Phone IP: $PHONE_IP)..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

