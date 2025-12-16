#!/bin/bash
# use when editing config simple changes or code changes in n8n or python-worker

echo "🚀 Deploying new code..."

# 1. Build เฉพาะตัวที่มีการแก้โค้ด (ตัด --pull ออกเพื่อให้ build เร็วขึ้น ถ้า base image เดิมยังดีอยู่)
echo "🏗️  Building n8n and Python Worker..."
docker compose --profile gpu-nvidia build n8n python-worker

# 2. บังคับเริ่มใหม่เฉพาะ 2 ตัวนี้
echo "🔥 Restarting services..."
docker compose --profile gpu-nvidia up -d --force-recreate n8n python-worker

echo "✅ Code Deployed!"