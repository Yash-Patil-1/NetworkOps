#!/bin/bash
set -e
echo "🌐 NetworkOps Setup"
cd backend && python3 -m venv venv 2>/dev/null || true && ./venv/bin/pip install -r requirements.txt -q && echo "✅ Backend" && cd ..
cd frontend && npm install --silent && echo "✅ Frontend" && cd ..
echo "Run: cd backend && ./venv/bin/uvicorn main:app --port 8002"
echo "Run: cd frontend && npm run dev"
echo "Open: http://localhost:5175"
