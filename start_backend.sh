#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
echo "🚀 Starting NetSage ML Backend on http://localhost:8000"
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

