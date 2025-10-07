cp .env.example .env

docker compose --profile gpu-nvidia up -d

#For ngrok tunnel to n8n
ngrok http --url=subtle-aphid-virtually.ngrok-free.app 5678 (n8n port)

ssh -L 8888:127.0.0.1:11434 -L 5433:127.0.0.1:5432 llmadmin@10.13.229.6

psql -h 127.0.0.1 -p 5433 -U admin -d n8n
