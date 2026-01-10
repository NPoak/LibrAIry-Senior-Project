#!/bin/bash
# when starting the system for the first time or after a full update

echo "🚀 Starting Full Update..."

# 1. ดึง Image สำเร็จรูป (Ollama, Postgres, etc.) ให้เป็นล่าสุด
echo "⬇️  Pulling latest images..."
docker compose --profile gpu-nvidia pull

# 2. Build Image ของเราเอง (n8n, Python) โดยเช็ค Base Image ใหม่ด้วย
echo "🏗️  Building custom images..."
docker compose --profile gpu-nvidia build --pull

# 3. เริ่มต้น Container ใหม่ (Recreate)
echo "🔥 Recreating containers..."
docker compose --profile gpu-nvidia up -d --remove-orphans

# 4. ล้าง Image เก่าๆ ที่ไม่ใช้แล้ว (เพื่อไม่ให้หนักเครื่อง)
echo "🧹 Cleaning up old images..."
docker image prune -f

echo "✅ Update Complete! System is running."