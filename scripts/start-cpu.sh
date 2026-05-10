#!/bin/bash
# use for starting the entire system from scratch or after a complete shutdown

echo "Initializing LibrAIry System (CPU Mode)..."

# 1. เช็กและสร้าง External Network ถ้ายังไม่มี
if ! docker network ls | grep -q "librairy-net"; then
    echo "External network 'librairy-net' not found. Creating it now..."
    docker network create librairy-net
else
    echo "Network 'librairy-net' already exists."
fi

# 2. รันระบบทั้งหมดพร้อม Profile CPU
echo "Starting all services in CPU mode..."
# เปลี่ยนจาก --profile gpu-nvidia เป็น --profile cpu
docker compose --profile cpu up -d

echo "All services are successfully started!"

# 3. โชว์สถานะ Container ทั้งหมด
docker compose --profile cpu ps