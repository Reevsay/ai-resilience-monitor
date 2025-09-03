@echo off
echo 🔄 Restarting AI proxy with updated configuration...
cd "C:\Users\yashv\OneDrive - BML MUNJAL UNIVERSITY\Documents\Work\Projects\AI related Projects\DevOps Project"

echo 📋 Stopping containers...
docker-compose down

echo 🚀 Starting with new configuration...
docker-compose up -d

echo ⏳ Waiting for services...
timeout /t 10 /nobreak >nul

echo ✅ Testing real API integration...
npm run openai-test-small

echo 📊 Check your dashboard: http://localhost:3000/dashboard
