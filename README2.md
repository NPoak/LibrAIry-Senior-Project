cp .env.example .env

docker compose --profile gpu-nvidia up -d

#For ngrok tunnel to n8n
ngrok http --url=subtle-aphid-virtually.ngrok-free.app 5678 (n8n port)
