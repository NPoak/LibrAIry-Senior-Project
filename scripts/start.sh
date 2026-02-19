#!/bin/bash
# use for starting the entire system from scratch or after a complete shutdown

echo "Initializing LibrAIry System..."

# 1. เช็กและสร้าง External Network ถ้ายังไม่มี
if ! docker network ls | grep -q "librairy-net"; then
    echo "External network 'librairy-net' not found. Creating it now..."
    docker network create librairy-net
else
    echo "Network 'librairy-net' already exists."
fi

# 2. รันระบบทั้งหมดพร้อม Profile GPU
echo "Starting all services..."
docker compose --profile gpu-nvidia up -d

echo "All services are successfully started!"

# 3. (Optional) โชว์สถานะ Container ทั้งหมดให้ดูหลังรันเสร็จ
docker compose ps