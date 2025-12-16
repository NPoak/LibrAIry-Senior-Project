#!/bin/bash
# when starting the system after deploying or updating

echo "Starting services..."

# รัน Docker Compose ในโหมด GPU Nvidia แบบ Background (-d)
docker compose --profile gpu-nvidia up -d

echo "✅ All services started!"